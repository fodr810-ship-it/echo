import discord
from discord.ext import commands
import random
import asyncio

class CodenamesGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command(name="start_codenames")
    async def start_codenames(self, ctx):
        self.games[ctx.channel.id] = {
            "players": [], "turn": "blue", "status": "playing",
            "words": [], "colors": [], "blue_score": 0, "red_score": 0,
            "blue_team": [], "red_team": []
        }
        await ctx.send("لعبة كود نيمز بدأت! انضم 4 لاعبين:", view=JoinView(self))

class JoinView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="انضم للعبة", style=discord.ButtonStyle.primary)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        game = self.cog.games[interaction.channel.id]
        if interaction.user not in game["players"]:
            game["players"].append(interaction.user)
            await interaction.response.send_message(f"تم! {len(game['players'])}/4", ephemeral=True)
            if len(game["players"]) == 4:
                await self.start_match(interaction)

    async def start_match(self, interaction):
        game = self.cog.games[interaction.channel.id]
        random.shuffle(game["players"])
        # تقسيم الفرق: الأول قائد، الثاني لاعب
        game["blue_team"] = {"leader": game["players"][0], "player": game["players"][1]}
        game["red_team"] = {"leader": game["players"][2], "player": game["players"][3]}
        
        game["words"] = random.sample(["قمر", "شمس", "سيارة", "طيارة", "مفتاح", "باب", "بحر", "رمل", "جبل", "ثلج", "نار", "ماء", "سيف", "درع", "حصان", "فارس", "ملك", "قلعة", "ذهب", "فضة", "شجرة", "وردة", "عصفور", "نسر", "أسد"], 25)
        game["colors"] = ["blue"]*11 + ["red"]*11 + ["black"]*3
        random.shuffle(game["colors"])

        # إرسال الكلمات الخاصة بكل فريق لقادته
        blue_words = [game["words"][i] for i, c in enumerate(game["colors"]) if c == "blue"]
        red_words = [game["words"][i] for i, c in enumerate(game["colors"]) if c == "red"]
        
        await game["blue_team"]["leader"].send(f"أنت قائد الفريق الأزرق، كلماتك هي: {blue_words}")
        await game["red_team"]["leader"].send(f"أنت قائد الفريق الأحمر، كلماتك هي: {red_words}")
        
        await interaction.channel.send("بدأت اللعبة! الفريق الأزرق هو من يبدأ. (دقيقة واحدة لكل دور)")
        await interaction.channel.send("اللوحة:", view=GameBoardView(self.cog, interaction.channel.id))

class GameBoardView(discord.ui.View):
    def __init__(self, cog, channel_id):
        super().__init__(timeout=None)
        game = cog.games[channel_id]
        for i in range(25):
            self.add_item(WordButton(i, game["words"][i], cog, channel_id))

class WordButton(discord.ui.Button):
    def __init__(self, index, label, cog, channel_id):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.index, self.cog, self.channel_id = index, cog, channel_id

    async def callback(self, interaction: discord.Interaction):
        game = self.cog.games[self.channel_id]
        # التحقق من الدور
        is_blue = interaction.user in [game["blue_team"]["leader"], game["blue_team"]["player"]]
        if (game["turn"] == "blue" and not is_blue) or (game["turn"] == "red" and is_blue):
            return await interaction.response.send_message("ليس دور فريقك!", ephemeral=True)
            
        color = game["colors"][self.index]
        self.disabled = True
        
        if color == "black":
            await interaction.channel.send(f"💀 خسر الفريق {game['turn']}!")
            game["status"] = "finished"
        elif color == "blue":
            self.style = discord.ButtonStyle.primary
            game["blue_score"] += 1
            game["turn"] = "red" # تغيير الدور
        elif color == "red":
            self.style = discord.ButtonStyle.danger
            game["red_score"] += 1
            game["turn"] = "blue" # تغيير الدور

        await interaction.response.edit_message(view=self.view)
        await interaction.channel.send(f"الدور انتقل للفريق: {game['turn'].upper()}")

async def setup(bot):
    await bot.add_cog(CodenamesGame(bot))