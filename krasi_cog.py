import discord
from discord.ext import commands
import asyncio
import random

# إعداد الصلاحيات (Intents)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# نظام لمنع تداخل الألعاب في نفس الروم
active_games = {}

# كلاس زر الانضمام للعبة
class JoinView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30.0) # وقت التسجيل 30 ثانية
        self.players = []

    @discord.ui.button(label="🎮 انضمام للعبة", style=discord.ButtonStyle.blurple)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.players:
            await interaction.response.send_message("أنت مسجل بالفعل في القائمة! 🏎️", ephemeral=True)
        else:
            self.players.append(interaction.user)
            await interaction.response.send_message(f"✅ {interaction.user.mention} انضم للعبة الكراسي!", ephemeral=False)

# كلاس زر الكرسي السريع
class ChairButton(discord.ui.View):
    def __init__(self, players, max_chairs):
        super().__init__(timeout=15.0)
        self.players = players
        self.max_chairs = max_chairs
        self.saved_players = []

    @discord.ui.button(label="🪑 اجلس هنا بسرعة!", style=discord.ButtonStyle.green)
    async def click_chair(self, interaction: discord.Interaction, button: discord.ui.Button):
        # التحقق إذا كان الشخص لاعب أساسي في الجولة الحالية
        if interaction.user not in self.players:
            await interaction.response.send_message("عذراً، أنت لست من ضمن اللاعبين في هذه الجولة! ❌", ephemeral=True)
            return

        # التحقق إذا كان قد حجز كرسياً بالفعل
        if interaction.user in self.saved_players:
            await interaction.response.send_message("أنت حاجز كرسي بالفعل، انتظر باقي اللاعبين! 🛋️", ephemeral=True)
            return

        # حجز الكرسي إذا كانت هناك كراسي شاغرة
        if len(self.saved_players) < self.max_chairs:
            self.saved_players.append(interaction.user)
            await interaction.response.send_message(f"⚡ {interaction.user.mention} لحق على كرسي وحمى نفسه!")
            
            # إذا امتلأت الكراسي تنتهي الجولة فوراً
            if len(self.saved_players) == self.max_chairs:
                self.stop()
        else:
            await interaction.response.send_message("للأسف طارت الطيور بأرزاقها.. الكراسي امتلأت! 😭", ephemeral=True)

# أمر تشغيل اللعبة
@bot.command(name="كراسي")
async def musical_chairs(ctx):
    if ctx.channel.id in active_games:
        await ctx.send("❌ هناك لعبة قائمة بالفعل في هذا الروم، انتظر حتى تنتهي!")
        return

    active_games[ctx.channel.id] = True
    await ctx.send("📢 **بدأت لعبة الكراسي الموسيقية!**\nاضغط على الزر بالأسفل للاشتراك. تبدأ اللعبة خلال 30 ثانية (مطلوب لاعبين على الأقل).")

    join_view = JoinView()
    init_msg = await ctx.send("سجل حضورك هنا 👇", view=join_view)

    # انتظار انتهاء وقت التسجيل
    await asyncio.sleep(30)
    await init_msg.edit(content="⌛ **انتهى وقت التسجيل!**", view=None)

    players = join_view.players

    if len(players) < 2:
        await ctx.send("❌ تم إلغاء اللعبة لعدم وجود عدد كافٍ من اللاعبين (مطلوب لاعبين 2 أو أكثر).")
        active_games.pop(ctx.channel.id, None)
        return

    await ctx.send(f"🎮 **اللاعبون المشاركون:** {', '.join([p.mention for p in players])}\nاستعدوا... جاري تشغيل الموسيقى! 🎶")

    round_num = 1
    while len(players) > 1:
        await asyncio.sleep(3)
        await ctx.send(f"\n--- ✨ **الجولة {round_num}** ✨ ---")
        await ctx.send("🎵 *الموسيقى شـغـالـة... والجميع يدور حول الكراسي...* 💃🕺")

        # وقت عشوائي ل توقف الموسيقى (بين 5 إلى 12 ثانية)
        await asyncio.sleep(random.randint(5, 12))

        max_chairs = len(players) - 1
        chair_view = ChairButton(players, max_chairs)

        alert_msg = await ctx.send(f"🛑 **وقفت الموسيقى!!!**\nإلحق واضغط على الكرسي بسرعة! الكراسي المتوفرة: **{max_chairs}** فقط! 🪑🏃‍♂️", view=chair_view)

        # انتظار تفاعل اللاعبين أو انتهاء الوقت
        await chair_view.wait()

        # تحديد من لم يجد كرسي
        eliminated = []
        for p in players:
            if p not in chair_view.saved_players:
                eliminated.append(p)

        # إقصاء اللاعبين الخاسرين في هذه الجولة
        for p in eliminated:
            players.remove(p)
            await ctx.send(f"💀 للأسف {p.mention} ما لحق على كرسي وتم إقصاؤه!")

        await alert_msg.edit(view=None)
        round_num += 1

    # إعلان الفائز النهائي
    winner = players[0]
    await ctx.send(f"\n🏆🎉 **مبرووووووك! الفائز بلقب ملك الكراسي هو: {winner.mention}** 👑")
    active_games.pop(ctx.channel.id, None)

@bot.event
async def on_ready():
    print(f"✅ تم تشغيل البوت بنجاح باسم: {bot.user.name}")

