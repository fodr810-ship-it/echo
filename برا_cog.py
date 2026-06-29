import discord
from discord.ext import commands
import random
from collections import Counter

# --- قاعدة البيانات ---
WORDS_BANK = {
    "حيوانات": ["أسد", "فيل", "زرافة", "نمر", "قرد", "حصان", "كلب", "قطة", "دب", "ثعلب"],
    "ملابس": ["قميص", "بنطال", "فستان", "حذاء", "قبعة", "معطف", "جورب", "شال", "قفاز", "نظارة"],
    "دول": ["السعودية", "مصر", "اليابان", "البرازيل", "فرنسا", "كندا", "الصين", "الهند", "إيطاليا", "إسبانيا"],
    "مدن": ["الرياض", "دبي", "باريس", "لندن", "نيويورك", "طوكيو", "القاهرة", "روما", "مدريد", "برلين"],
    "أكلات": ["بيتزا", "برجر", "سوشي", "شاورما", "كبسة", "باستا", "ستيك", "سلطة", "كيك", "ايسكريم"],
    "كورة": ["ملعب", "مدرجات", "كأس", "صافرة", "حذاء", "مرمى", "شباك", "راية", "مدافع", "مدرب"]
}

# --- كلاس اللعبة ---
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

# --- واجهات الأزرار ---
class GameView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label="📜 وش السالفة؟", style=discord.ButtonStyle.primary)
    async def show_topic(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.game.imposter:
            await interaction.response.send_message("🕵️ أنت برا السالفة! حاول تندمج.", ephemeral=True)
        else:
            await interaction.response.send_message(f"📖 السالفة: **{self.game.topic}** (التصنيف: {self.game.category})", ephemeral=True)

    @discord.ui.button(label="🗣️ الدور التالي", style=discord.ButtonStyle.secondary)
    async def next_turn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.game.turn_index = (self.game.turn_index + 1) % len(self.game.players)
        await interaction.response.send_message(f"👉 الدور على: {self.game.players[self.game.turn_index].mention}")

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
        await interaction.response.send_message(view=view, ephemeral=True)

    async def tally(self, i):
        # فرز بسيط (الأكثر تكراراً)
        most_voted = Counter(self.game.votes.values()).most_common(1)[0][0]
        if most_voted == self.game.imposter.id:
            await i.channel.send(f"🚨 كشفتوه! هو {self.game.imposter.mention}. هل يعرف السالفة؟ (انتظر خيارات التخمين)")
        else:
            await i.channel.send(f"❌ خطأ! الفائز هو {self.game.imposter.mention} (كان برا السالفة)")

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
            await interaction.response.edit_message(content=f"اللاعبين: {len(self.players)}")

    async def on_timeout(self):
        if len(self.players) < 3: return
        game = GameSession(self.msg.channel, self.host, self.players)
        view = discord.ui.View()
        select = discord.ui.Select(placeholder="اختر تصنيف...", options=[discord.SelectOption(label=c) for c in WORDS_BANK])
        async def cat_callback(i):
            game.start(select.values[0])
            await i.response.edit_message(content="🎮 بدأت اللعبة!", view=GameView(game))
        select.callback = cat_callback
        view.add_item(select)
        await self.msg.edit(content="اختر التصنيف:", view=view)

# --- الكوج ---
class SalfaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def سالفة(self, ctx):
        view = LobbyView(ctx.author)
        view.msg = await ctx.send("اضغط دخول للانضمام (30 ثانية):", view=view)

async def setup(bot):
    await bot.add_cog(SalfaCog(bot))