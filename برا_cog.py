import discord
from discord.ext import commands
import random
from collections import Counter

WORDS_BANK = {
    "حيوانات": ["أسد", "فيل", "زرافة", "نمر", "قرد", "حصان", "كلب", "قطة", "دب", "ثعلب"],
    "ملابس": ["قميص", "بنطال", "فستان", "حذاء", "قبعة", "معطف", "جورب", "شال", "قفاز", "نظارة"],
    "دول": ["السعودية", "مصر", "اليابان", "البرازيل", "فرنسا", "كندا", "الصين", "الهند", "إيطاليا", "إسبانيا"],
    "مدن": ["الرياض", "دبي", "باريس", "لندن", "نيويورك", "طوكيو", "القاهرة", "روما", "مدريد", "برلين"],
    "أكلات": ["بيتزا", "برجر", "سوشي", "شاورما", "كبسة", "باستا", "ستيك", "سلطة", "كيك", "ايسكريم"],
    "كورة": ["ملعب", "مدرجات", "كأس", "صافرة", "حذاء", "مرمى", "شباك", "راية", "مدافع", "مدرب"]
}

class GameSession:
    def __init__(self, channel, host, players):
        self.channel = channel
        self.host = host
        self.players = players
        self.imposter = random.choice(players)
        self.category = None
        self.topic = None
        self.guess_options = []
        self.turn_index = 0
        self.votes = {} 
        self.is_active = True

    def start(self, category):
        self.category = category
        self.topic = random.choice(WORDS_BANK[category])
        other = [w for w in WORDS_BANK[category] if w != self.topic]
        self.guess_options = random.sample(other, 7) + [self.topic]
        random.shuffle(self.guess_options)

class GuessButtons(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        for word in game.guess_options:
            btn = discord.ui.Button(label=word, style=discord.ButtonStyle.secondary)
            async def callback(i, word=word):
                if word == game.topic:
                    await i.response.send_message(f"🎉 صح! {game.imposter.mention} عرف السالفة وفاز!", ephemeral=False)
                else:
                    await i.response.send_message(f"❌ خطأ! السالفة كانت: **{game.topic}**. فاز اللاعبون!", ephemeral=False)
                self.stop()
            btn.callback = callback
            self.add_item(btn)

class GameView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label="📜 وش السالفة؟", style=discord.ButtonStyle.primary)
    async def show_topic(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.game.imposter:
            await interaction.response.send_message("🕵️ أنت برا السالفة!", ephemeral=True)
        else:
            await interaction.response.send_message(f"📖 السالفة: **{self.game.topic}**", ephemeral=True)

    @discord.ui.button(label="🗳️ تصويت", style=discord.ButtonStyle.danger)
    async def vote(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = discord.ui.View()
        options = [discord.SelectOption(label=p.display_name, value=str(p.id)) for p in self.game.players]
        select = discord.ui.Select(placeholder="اختر المشتبه به...", options=options)
        
        async def select_callback(i):
            self.game.votes[i.user.id] = int(select.values[0])
            await i.response.send_message("✅ تم التصويت", ephemeral=True)
            if len(self.game.votes) == len(self.game.players):
                await self.tally(i)
        
        select.callback = select_callback
        view.add_item(select)
        # إرسال التصويت كـ Embed
        embed = discord.Embed(title="التصويت", description="صوتوا للشخص اللي تعتقدون أنه برا السالفة:", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def tally(self, i):
        most_voted = Counter(self.game.votes.values()).most_common(1)[0][0]
        if most_voted == self.game.imposter.id:
            await i.channel.send(f"🚨 كشفتوه! هو {self.game.imposter.mention}. \nيا {self.game.imposter.mention}، اختر السالفة الصحيحة لتفوز:")
            await i.channel.send(view=GuessButtons(self.game))
        else:
            await i.channel.send(f"❌ خطأ! الفائز هو {self.game.imposter.mention} (كان برا السالفة)!")

class LobbyView(discord.ui.View):
    def __init__(self, host):
        super().__init__(timeout=30)
        self.host = host
        self.players = [host]
        self.msg = None

    @discord.ui.button(label="دخول", style=discord.ButtonStyle.success)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            self.players.append(interaction.user)
            await interaction.response.edit_message(content=f"اللاعبين المنضمين: {len(self.players)}")

    async def on_timeout(self):
        if not self.msg: return
        try:
            if len(self.players) < 3:
                await self.msg.edit(content="❌ العدد غير كافٍ.", view=None)
            else:
                game = GameSession(self.msg.channel, self.host, self.players)
                view = discord.ui.View()
                select = discord.ui.Select(placeholder="اختر تصنيف...", options=[discord.SelectOption(label=c) for c in WORDS_BANK])
                async def cat_callback(i):
                    game.start(select.values[0])
                    await i.response.edit_message(content="🎮 بدأت اللعبة!", view=GameView(game))
                select.callback = cat_callback
                view.add_item(select)
                await self.msg.edit(content="اختر التصنيف:", view=view)
        except discord.NotFound:
            pass

class SalfaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def سالفة(self, ctx):
        view = LobbyView(ctx.author)
        view.msg = await ctx.send("اضغط دخول للانضمام (30 ثانية):", view=view)

async def setup(bot):
    await bot.add_cog(SalfaCog(bot))