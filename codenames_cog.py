import discord
from discord.ext import commands
import random

# قائمة كلمات (يمكنك زيادتها)
WORD_LIST = ["قمر", "شمس", "سيارة", "طيارة", "مفتاح", "باب", "بحر", "رمل", "جبل", "ثلج", 
             "نار", "ماء", "سيف", "درع", "حصان", "فارس", "ملك", "قلعة", "ذهب", "فضة",
             "شجرة", "وردة", "عصفور", "نسر", "أسد", "قلم", "كتاب", "نجم", "غيمة", "عطر"]

class CodenamesGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command(name="start_codenames")
    async def start_codenames(self, ctx):
        self.games[ctx.channel.id] = {
            "players": [], "status": "waiting", "words": [], 
            "colors": [], "blue_score": 0, "red_score": 0
        }
        await ctx.send("لعبة كود نيمز! انضم 4 لاعبين لبدء اللعبة.", view=JoinView(self))

class JoinView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="انضم للعبة", style=discord.ButtonStyle.primary)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        game = self.cog.games[interaction.channel.id]
        if interaction.user not in game["players"]:
            game["players"].append(interaction.user)
            await interaction.response.send_message(f"تم! العدد: {len(game['players'])}/4", ephemeral=True)
            if len(game["players"]) == 4:
                await self.start_match(interaction)
        else:
            await interaction.response.send_message("أنت منضم بالفعل!", ephemeral=True)

    async def start_match(self, interaction):
        game = self.cog.games[interaction.channel.id]
        game["status"] = "playing"
        game["words"] = random.sample(WORD_LIST, 25)
        # 9 أزرق، 8 أحمر، 7 محايد، 1 أسود
        colors = ["blue"]*9 + ["red"]*8 + ["neutral"]*7 + ["black"]*1
        random.shuffle(colors)
        game["colors"] = colors
        
        # إرسال الخاص للقادة
        blue_leader, red_leader = game["players"][0], game["players"][2]
        await blue_leader.send(f"أنت قائد الفريق الأزرق! الكلمات الزرقاء هي: {game['words'][:9]}")
        await red_leader.send(f"أنت قائد الفريق الأحمر! الكلمات الحمراء هي: {game['words'][9:17]}")
        
        await interaction.channel.send("بدأت اللعبة! القادة تلقوا خريطتهم.")
        await interaction.channel.send("لوحة اللعبة:", view=GameBoardView(self.cog, interaction.channel.id))

class GameBoardView(discord.ui.View):
    def __init__(self, cog, channel_id):
        super().__init__(timeout=None)
        game = cog.games[channel_id]
        for i in range(25):
            self.add_item(WordButton(i, game["words"][i], cog, channel_id))

class WordButton(discord.ui.Button):
    def __init__(self, index, label, cog, channel_id):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.index = index
        self.cog = cog
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        game = self.cog.games[self.channel_id]
        color = game["colors"][self.index]
        self.disabled = True
        
        if color == "blue":
            self.style = discord.ButtonStyle.primary
            game["blue_score"] += 1
        elif color == "red":
            self.style = discord.ButtonStyle.danger
            game["red_score"] += 1
        elif color == "black":
            self.style = discord.ButtonStyle.secondary
            await interaction.channel.send("💀 لمستم الكلمة القاتلة! خسارة!")
            game["status"] = "finished"
        
        await interaction.response.edit_message(view=self.view)
        
        if game["blue_score"] == 9: await interaction.channel.send("🎉 فاز الفريق الأزرق!")
        elif game["red_score"] == 8: await interaction.channel.send("🎉 فاز الفريق الأحمر!")

async def setup(bot):
    await bot.add_cog(CodenamesGame(bot))