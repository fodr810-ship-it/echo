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
            "blue_team": [], "red_team": [], "blue_leader": None, "red_leader": None,
            "remaining_guesses": 0
        }
        await ctx.send("لعبة كود نيمز! بانتظار 4 لاعبين:", view=JoinView(self))

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
        game["blue_team"] = [game["players"][0], game["players"][1]]
        game["red_team"] = [game["players"][2], game["players"][3]]
        game["blue_leader"], game["red_leader"] = game["players"][0], game["players"][2]
        
        game["words"] = random.sample(["قمر", "شمس", "سيارة", "طيارة", "مفتاح", "باب", "بحر", "رمل", "جبل", "ثلج", "نار", "ماء", "سيف", "درع", "حصان", "فارس", "ملك", "قلعة", "ذهب", "فضة", "شجرة", "وردة", "عصفور", "نسر", "أسد"], 25)
        game["colors"] = ["blue"]*11 + ["red"]*11 + ["black"]*3
        random.shuffle(game["colors"])

        for l in [game["blue_leader"], game["red_leader"]]:
            view = HintView(self.cog, interaction.channel.id)
            await l.send("حان دورك كقائد! اضغط لتقديم تلميح:", view=view)
        
        await interaction.channel.send("بدأت اللعبة! القادة يقدمون تلميحاتهم.", view=GameBoardView(self.cog, interaction.channel.id))

class HintView(discord.ui.View):
    def __init__(self, cog, channel_id):
        super().__init__(timeout=None)
        self.cog, self.channel_id = cog, channel_id
    
    @discord.ui.button(label="تقديم تلميح", style=discord.ButtonStyle.success)
    async def hint_btn(self, interaction: discord.Interaction, b: discord.ui.Button):
        await interaction.response.send_modal(HintModal(self.cog, self.channel_id))

class HintModal(discord.ui.Modal, title='أدخل التلميح'):
    hint = discord.ui.TextInput(label='التلميح', placeholder='كلمة واحدة...')
    count = discord.ui.TextInput(label='عدد الكلمات', placeholder='رقم...')

    def __init__(self, cog, channel_id):
        super().__init__()
        self.cog, self.channel_id = cog, channel_id

    async def on_submit(self, interaction: discord.Interaction):
        game = self.cog.games[self.channel_id]
        game["remaining_guesses"] = int(self.count.value) + 1
        await interaction.client.get_channel(self.channel_id).send(f"📢 تلميح القائد: {self.hint.value} (عدد الكلمات: {self.count.value})")
        await interaction.response.send_message("تم إرسال التلميح!", ephemeral=True)

class GameBoardView(discord.ui.View):
    def __init__(self, cog, channel_id):
        super().__init__(timeout=None)
        self.cog, self.channel_id = cog, channel_id
        for i in range(25):
            self.add_item(WordButton(i, cog.games[channel_id]["words"][i], cog, channel_id))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        game = self.cog.games[self.channel_id]
        is_blue = interaction.user in game["blue_team"]
        if (game["turn"] == "blue" and is_blue) or (game["turn"] == "red" and not is_blue):
            return True
        await interaction.response.send_message("ليس دور فريقك!", ephemeral=True)
        return False

class WordButton(discord.ui.Button):
    def __init__(self, index, label, cog, channel_id):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.index, self.cog, self.channel_id = index, cog, channel_id

    async def callback(self, interaction: discord.Interaction):
        game = self.cog.games[self.channel_id]
        color = game["colors"][self.index]
        self.disabled = True
        
        if color == "black":
            await interaction.response.edit_message(content=f"💀 خسر فريق {game['turn']}!", view=None)
            return

        self.style = discord.ButtonStyle.primary if color == "blue" else discord.ButtonStyle.danger
        game["remaining_guesses"] -= 1
        
        if game["remaining_guesses"] <= 0 or color != game["turn"]:
            game["turn"] = "red" if game["turn"] == "blue" else "blue"
            
        await interaction.response.edit_message(content=f"الدور لـ: {game['turn']}", view=self.view)

async def setup(bot):
    await bot.add_cog(CodenamesGame(bot))