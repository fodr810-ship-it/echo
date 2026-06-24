import discord
from discord.ext import commands
import random

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# قائمة كلمات تجريبية (تحتاج توسعها لـ 100+ كلمة)
WORD_LIST = [
    "قمر", "شمس", "سيارة", "طيارة", "مفتاح", "باب", "بحر", "رمل", "جبل", "ثلج",
    "نار", "ماء", "سيف", "درع", "حصان", "فارس", "ملك", "قلعة", "ذهب", "فضة",
    "شجرة", "وردة", "عصفور", "نسر", "أسد"
]

class CodenamesBoard(discord.ui.View):
    def __init__(self, words):
        super().__init__(timeout=None)
        # إنشاء 25 زر (5 صفوف × 5 أعمدة)
        for i, word in enumerate(words):
            button = discord.ui.Button(label=word, style=discord.ButtonStyle.secondary, row=i//5)
            button.callback = self.button_callback
            self.add_item(button)

    async def button_callback(self, interaction: discord.Interaction):
        # هنا يتم التحقق من لون الكلمة (أحمر، أزرق، محايد، أو قاتل)
        # وتحديث لون الزر بعد الضغط عليه
        await interaction.response.send_message(f"ضغطت على الكلمة!", ephemeral=True)

@bot.command(name="start_codenames")
async def start_codenames(ctx):
    if len(WORD_LIST) < 25:
        await ctx.send("تحتاج على الأقل 25 كلمة في القائمة!")
        return
    
    # اختيار 25 كلمة عشوائية للوحة
    game_words = random.sample(WORD_LIST, 25)
    
    # هنا يتم تحديد الألوان وتخزينها (الخريطة التي ترسل للقادة فقط)
    # ...

    view = CodenamesBoard(game_words)
    await ctx.send("بدأت لعبة كود نيمز! 🕵️‍♂️", view=view)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# شغل البوت باستخدام التوكن الخاص فيك
# bot.run('YOUR_BOT_TOKEN_HERE')