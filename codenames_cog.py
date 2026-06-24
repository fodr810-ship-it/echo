import discord
from discord.ext import commands
import random

class CodenamesGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command(name="start_codenames")
    async def start_codenames(self, ctx):
        self.games[ctx.channel.id] = {
            "players": [], "turn": "blue", "status": "playing",
            "words": [], "colors": [], "blue_score": 0, "red_score": 0,
            "blue_team": [], "red_team": [],
            "blue_leader": None, "red_leader": None
        }
        await ctx.send("لعبة كود نيمز! بانتظار 4 لاعبين للانضمام:", view=JoinView(self))

class JoinView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="انضم للعبة", style=discord.ButtonStyle.primary)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        game = self.cog.games[interaction.channel.id]
        if interaction.user not in game["players"]:
            game["players"].append(interaction.user)
            await interaction.response.send_message(f"تم! ({len(game['players'])}/4)", ephemeral=True)
            if len(game["players"]) == 4:
                await self.start_match(interaction)

    async def start_match(self, interaction):
        game = self.cog.games[interaction.channel.id]
        random.shuffle(game["players"])
        # تحديد القادة (الأول من كل فريق)
        game["blue_team"] = [game["players"][0], game["players"][1]]
        game["red_team"] = [game["players"][2], game["players"][3]]
        game["blue_leader"] = game["players"][0]
        game["red_leader"] = game["players"][2]
        
        game["words"] = random.sample(["قمر", "شمس", "سيارة", "طيارة", "مفتاح", "باب", "بحر", "رمل", "جبل", "ثلج", "نار", "ماء", "سيف", "درع", "حصان", "فارس", "ملك", "قلعة", "ذهب", "فضة", "شجرة", "وردة", "عصفور", "نسر", "أسد"], 25)
        game["colors"] = ["blue"]*11 + ["red"]*11 + ["black"]*3
        random.shuffle(game["colors"])

        # إرسال الكلمات للقادة فقط
        blue_words = [game["words"][i] for i, c in enumerate(game["colors"]) if c == "blue"]
        red_words = [game["words"][i] for i, c in enumerate(game["colors"]) if c == "red"]
        
        await game["blue_leader"].send(f"أنت قائد الفريق الأزرق، كلماتك هي: {blue_words}")
        await game["red_leader"].send(f"أنت قائد الفريق الأحمر، كلماتك هي: {red_words}")
        
        # إرسال تنبيه للفريق (بدون كلمات)
        for member in game["blue_team"]: 
            if member != game["blue_leader"]: await member.send("أنت في الفريق الأزرق. انتظر دورك!")
        for member in game["red_team"]: 
            if member != game["red_leader"]: await member.send("أنت في الفريق الأحمر. انتظر دورك!")
        
        await interaction.channel.send("بدأت اللعبة! تم إرسال كلمات القادة في الخاص.", view=GameBoardView(self.cog, interaction.channel.id))

class GameBoardView(discord.ui.View):
    def __init__(self, cog, channel_id):
        super().__init__(timeout=None)
        self.cog = cog
        self.channel_id = channel_id
        game = cog.games[channel_id]
        for i in range(25):
            self.add_item(WordButton(i, game["words"][i], cog, channel_id))

class WordButton(discord.ui.Button):
    def __init__(self, index, label, cog, channel_id):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.index, self.cog, self.channel_id = index, cog, channel_id

    async def callback(self, interaction: discord.Interaction):
        game = self.cog.games[self.channel_id]
        color = game["colors"][self.index]
        self.disabled = True
        
        if color == "black":
            await interaction.response.edit_message(content=f"💀 خسر الفريق {game['turn'].upper()} بسبب الكلمة السوداء!", view=None)
            game["status"] = "finished"
            return
        
        if color == "blue":
            self.style = discord.ButtonStyle.primary
            game["blue_score"] += 1
            game["turn"] = "red"
        else:
            self.style = discord.ButtonStyle.danger
            game["red_score"] += 1
            game["turn"] = "blue"

        await interaction.response.edit_message(
            content=f"النتيجة: أزرق ({game['blue_score']}) - أحمر ({game['red_score']})\nالدور الحالي: {game['turn'].upper()}",
            view=self.view
        )

async def setup(bot):
    await bot.add_cog(CodenamesGame(bot))