import discord
from discord.ext import commands
import asyncio
import random

# --- كلاس زر الانضمام مع العداد الديناميكي الشفاف ---
class JoinView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30.0)
        self.players = []

    @discord.ui.button(label="🎮 انضمام للعبة", style=discord.ButtonStyle.secondary) # زر شفاف
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.players:
            await interaction.response.send_message("أنت مسجل بالفعل في القائمة! 🏎️", ephemeral=True)
            return

        self.players.append(interaction.user)
        # رسالة تأكيد مخفية للاعب
        await interaction.response.send_message("✅ انضممت للعبة الكراسي بنجاح! استعد 🪑", ephemeral=True)
        
        # تحديث الـ Embed الأساسي مباشرة بالعدّاد الجديد
        updated_embed = discord.Embed(
            title="🎮 لعبة الكراسي",
            description="اضغط على الزر بالأسفل للاشتراك في اللعبة.\nتبدأ اللعبة خلال 30 ثانية (مطلوب لاعبين على الأقل).",
            color=0x2b2d31 # لون داكن فخم ومتناسق
        )
        updated_embed.add_field(name="👥 عدد المشاركين الحالي", value=f"📡 **{len(self.players)}** لاعبين", inline=False)
        await interaction.message.edit(embed=updated_embed)

# --- كلاس زر الكرسي الشفاف السريع ---
class ChairButton(discord.ui.View):
    def __init__(self, players, max_chairs):
        super().__init__(timeout=15.0)
        self.players = players
        self.max_chairs = max_chairs
        self.saved_players = []

    @discord.ui.button(label="🪑 اجلس هنا بسرعة!", style=discord.ButtonStyle.secondary) # تم تعديله ليصبح شفافاً
    async def click_chair(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            await interaction.response.send_message("عذراً، أنت لست من ضمن اللاعبين في هذه الجولة! ❌", ephemeral=True)
            return

        if interaction.user in self.saved_players:
            await interaction.response.send_message("أنت حاجز كرسي بالفعل، انتظر باقي اللاعبين! 🛋️", ephemeral=True)
            return

        if len(self.saved_players) < self.max_chairs:
            self.saved_players.append(interaction.user)
            await interaction.response.send_message(f"⚡ {interaction.user.mention} لحق على كرسي!")
            if len(self.saved_players) == self.max_chairs:
                self.stop()
        else:
            await interaction.response.send_message("للأسف امتلأت الكراسي! 😭", ephemeral=True)

# --- كلاس الـ Cog الأساسي ---
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

        # إمبيد التسجيل الأنيق الأول للعبة
        start_embed = discord.Embed(
            title="🎮 لعبة الكراسي",
            description="اضغط على الزر بالأسفل للاشتراك في اللعبة.\nتبدأ اللعبة خلال 30 ثانية (مطلوب لاعبين على الأقل).",
            color=0x2b2d31
        )
        start_embed.add_field(name="👥 عدد المشاركين الحالي", value="📡 **0** لاعبين", inline=False)

        join_view = JoinView()
        init_msg = await ctx.send(embed=start_embed, view=join_view)

        await asyncio.sleep(30)
        
        # تعديل الإمبيد فور انتهاء وقت التسجيل لغلق الأزرار
        end_embed = discord.Embed(
            title="🎮 لعبة الكراسي",
            description="⌛ **انتهى وقت التسجيل!**",
            color=0x2b2d31
        )
        end_embed.add_field(name="👥 إجمالي المشاركين", value=f"🏆 **{len(join_view.players)}** لاعبين", inline=False)
        await init_msg.edit(embed=end_embed, view=None)

        players = join_view.players

        if len(players) < 2:
            await ctx.send("❌ تم إلغاء اللعبة لعدم وجود عدد كافٍ من اللاعبين.")
            self.active_games.pop(ctx.channel.id, None)
            return

        round_num = 1
        while len(players) > 1:
            await asyncio.sleep(2)
            
            # رسالة الاستعداد البسيطة والجميلة داخل إمبيد بدون حشو الموسيقى
            round_embed = discord.Embed(
                title=f"✨ الجولة {round_num}",
                description="**استعدوا... ⏳**",
                color=0x2b2d31
            )
            round_msg = await ctx.send(embed=round_embed)

            # وقت عشوائي سريع قبل ظهور الكرسي
            await asyncio.sleep(random.randint(4, 9))

            max_chairs = len(players) - 1
            chair_view = ChairButton(players, max_chairs)

            # إمبيد ظهور الكراسي السريع للضغط
            chair_embed = discord.Embed(
                title="🛑 إلحق الكرسي!!!",
                description=f"اضغط على الزر بالأسفل فوراً!\nالكراسي المتبقية: **{max_chairs}** فقط! 🏃‍♂️",
                color=0x2b2d31
            )
            
            alert_msg = await ctx.send(embed=chair_embed, view=chair_view)
            await round_msg.delete() # حذف رسالة "استعدوا" السابقة لجعل الشات نظيفاً تماماً وعصرياً

            await chair_view.wait()

            # حصر الخاسرين
            eliminated = [p for p in players if p not in chair_view.saved_players]

            for p in eliminated:
                players.remove(p)
                await ctx.send(f"💀 للأسف {p.mention} ما لحق وتم إقصاؤه!")

            await alert_msg.edit(view=None)
            round_num += 1

        # إعلان الفائز النهائي بإمبيد ذهبي خاص بالفوز
        winner = players[0]
        winner_embed = discord.Embed(
            title="🏆 مبرووووووك 🏆",
            description=f"ملك الكراسي المحترف في هذه اللعبة هو:\n👑 {winner.mention} 👑",
            color=0xfadb14 # لون ذهبي مخصص للفائز لإعطاء مظهر متناسق وجذاب
        )
        await ctx.send(embed=winner_embed)
        self.active_games.pop(ctx.channel.id, None)

async def setup(bot):
    await bot.add_cog(KrasiCog(bot))