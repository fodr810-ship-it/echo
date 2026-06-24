import discord
from discord.ext import commands
import random

# قائمة كلمات تجريبية
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
        # هنا يتم التحقق من لون الكلمة
        await interaction.response.send_message(f"ضغطت على الكلمة: {interaction.data['custom_id'] or interaction.data['component_type']}", ephemeral=True)

class Codenames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="start_codenames")
    async def start_codenames(self, ctx):
        if len(WORD_LIST) < 25:
            await ctx.send("تحتاج على الأقل 25 كلمة في القائمة!")
            return
        
        # اختيار 25 كلمة عشوائية
        game_words = random.sample(WORD_LIST, 25)
        
        view = CodenamesBoard(game_words)
        await ctx.send("بدأت لعبة كود نيمز! 🕵️‍♂️", view=view)

# دالة setup المطلوبة ليتمكن البوت من تحميل الملف كـ Cog
async def setup(bot):
    await bot.add_cog(Codenames(bot))