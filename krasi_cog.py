import discord
from discord.ext import commands
import asyncio
import random

# --- كلاس زر الانضمام (تم التعديل ليصبح شفافاً والرسالة خاصة) ---
class JoinView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30.0)
        self.players = []

    # تغيير الستايل إلى secondary ليظهر باللون الرمادي الشفاف
    @discord.ui.button(label="🎮 انضمام للعبة", style=discord.ButtonStyle.secondary)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.players:
            await interaction.response.send_message("أنت مسجل بالفعل في القائمة! 🏎️", ephemeral=True)
        else:
            self.players.append(interaction.user)
            # تغيير ephemeral إلى True لتصبح الرسالة خاصة باللاعب فقط
            await interaction.response.send_message("✅ انضممت للعبة الكراسي بنجاح! استعد 🪑", ephemeral=True)

# --- كلاس زر الكرسي السريع (بقي كما هو باللون الأخضر للحماس) ---
class ChairButton(discord.ui.View):
    def __init__(self, players, max_chairs):
        super().__init__(timeout=15.0)
        self.players = players
        self.max_chairs = max_chairs
        self.saved_players = []

    @discord.ui.button(label="🪑 اجلس هنا بسرعة!", style=discord.ButtonStyle.green)
    async def click_chair(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            await interaction.response.send_message("عذراً، أنت لست من ضمن اللاعبين في هذه الجولة! ❌", ephemeral=True)
            return

        if interaction.user in self.saved_players:
            await interaction.response.send_message("أنت حاجز كرسي بالفعل، انتظر باقي اللاعبين! 🛋️", ephemeral=True)
            return

        if len(self.saved_players) < self.max_chairs:
            self.saved_players.append(interaction.user)
            await interaction.response.send_message(f"⚡ {interaction.user.mention} لحق على كرسي وحمى نفسه!")
            if len(self.saved_players) == self.max_chairs:
                self.stop()
        else:
            await interaction.response.send_message("للأسف امتلأت الكراسي! 😭", ephemeral=True)

# --- الكلاس الأساسي للـ Cog ---
class KrasiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @commands.command(name="كراسي")
    async def musical_chairs(self, ctx):
        if ctx.channel.id in self.active_games:
            await ctx.send("❌ هناك لعبة قائمة بالفعل في هذا الروم، انتظر حتى تنتهي!")
            return

        self.active_games[ctx.channel.id] = True
        await ctx.send("📢 **بدأت لعبة الكراسي الموسيقية!**\nاضغط على الزر بالأسفل للاشتراك. تبدأ اللعبة خلال 30 ثانية (مطلوب لاعبين على الأقل).")

        join_view = JoinView()
        init_msg = await ctx.send("سجل حضورك هنا 👇", view=join_view)

        await asyncio.sleep(30)
        await init_msg.edit(content="⌛ **انتهى وقت التسجيل!**", view=None)

        players = join_view.players

        if len(players) < 2:
            await ctx.send("❌ تم إلغاء اللعبة لعدم وجود عدد كافٍ من اللاعبين.")
            self.active_games.pop(ctx.channel.id, None)
            return

        await ctx.send(f"🎮 **اللاعبون المشاركون:** {', '.join([p.mention for p in players])}\nاستعدوا... جاري تشغيل الموسيقى! 🎶")

        round_num = 1
        while len(players) > 1:
            await asyncio.sleep(3)
            await ctx.send(f"\n--- ✨ **الجولة {round_num}** ✨ ---")
            await ctx.send("🎵 *الموسيقى شـغـالـة... والجميع يدور حول الكراسي...* 💃🕺")

            await asyncio.sleep(random.randint(5, 12))

            max_chairs = len(players) - 1
            chair_view = ChairButton(players, max_chairs)

            alert_msg = await ctx.send(f"🛑 **وقفت الموسيقى!!!**\nإلحق واضغط على الكرسي بسرعة! الكراسي المتوفرة: **{max_chairs}** فقط! 🪑🏃‍♂️", view=chair_view)

            await chair_view.wait()

            eliminated = [p for p in players if p not in chair_view.saved_players]

            for p in eliminated:
                players.remove(p)
                await ctx.send(f"💀 للأسف {p.mention} ما لحق على كرسي وتم إقصاؤه!")

            await alert_msg.edit(view=None)
            round_num += 1

        winner = players[0]
        await ctx.send(f"\n🏆🎉 **مبرووووووك! الفائز بلقب ملك الكراسي هو: {winner.mention}** 👑")
        self.active_games.pop(ctx.channel.id, None)

# دالة الربط بالبوت الأساسي
async def setup(bot):
    await bot.add_cog(KrasiCog(bot))