import discord
from discord.ext import commands
import random
import asyncio
from collections import Counter

# قاعدة بيانات الكلمات (6 تصنيفات، كل تصنيف 10 كلمات)
WORDS_BANK = {
    "حيوانات": ["أسد", "فيل", "زرافة", "نمر", "قرد", "حصان", "كلب", "قطة", "دب", "ثعلب"],
    "ملابس": ["قميص", "بنطال", "فستان", "حذاء", "قبعة", "معطف", "جورب", "شال", "قفاز", "نظارة"],
    "دول": ["السعودية", "مصر", "اليابان", "البرازيل", "فرنسا", "كندا", "الصين", "الهند", "إيطاليا", "إسبانيا"],
    "مدن": ["الرياض", "دبي", "باريس", "لندن", "نيويورك", "طوكيو", "القاهرة", "روما", "مدريد", "برلين"],
    "أكلات": ["بيتزا", "برجر", "سوشي", "شاورما", "كبسة", "باستا", "ستيك", "سلطة", "كيك", "ايسكريم"],
    "كورة": ["ملعب", "مدرجات", "كأس", "صافرة", "حذاء رياضي", "مرمى", "شباك", "راية", "مدافع", "مدرب"]
}

class GameSession:
    def __init__(self, channel, host, players):
        self.channel = channel
        self.host = host
        self.players = players
        self.imposter = None
        self.category = None
        self.topic = None
        self.guess_options = []
        self.turn_index = 0
        self.votes = {}  # {voter_user_id: voted_user_id}
        self.is_active = True

    def setup_game(self, category):
        self.category = category
        self.topic = random.choice(WORDS_BANK[category])
        self.imposter = random.choice(self.players)
        
        # تجهيز خيارات التخمين (الكلمة الصحيحة + 7 كلمات عشوائية من نفس التصنيف)
        other_words = [w for w in WORDS_BANK[category] if w != self.topic]
        self.guess_options = random.sample(other_words, 7) + [self.topic]
        random.shuffle(self.guess_options)

class ImposterGuessButton(discord.ui.Button):
    def __init__(self, word, game):
        super().__init__(style=discord.ButtonStyle.secondary, label=word)
        self.word = word
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.game.imposter:
            await interaction.response.send_message("❌ هذا الزر مخصص للي برا السالفة فقط!", ephemeral=True)
            return

        for child in self.view.children:
            child.disabled = True
        
        if self.word == self.game.topic:
            self.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self.view)
            await self.game.channel.send(f"🎉 **فاز اللي برا السالفة!**\n{self.game.imposter.mention} قدر يخمن السالفة الصح وهي: **{self.game.topic}**")
        else:
            self.style = discord.ButtonStyle.danger
            await interaction.response.edit_message(view=self.view)
            await self.game.channel.send(f"💀 **خسر اللي برا السالفة!**\n{self.game.imposter.mention} اختار ({self.word}) والسالفة الحقيقية كانت: **{self.game.topic}**\n🏆 **فاز باقي اللاعبين!**")

class ImposterGuessView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        for word in self.game.guess_options:
            self.add_item(ImposterGuessButton(word, game))

class VoteSelect(discord.ui.Select):
    def __init__(self, game):
        self.game = game
        options = [discord.SelectOption(label=p.display_name, value=str(p.id)) for p in game.players]
        super().__init__(placeholder="اختر من تعتقد أنه برا السالفة...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        voted_user_id = int(self.values[0])
        self.game.votes[interaction.user.id] = voted_user_id
        await interaction.response.send_message("✅ تم تسجيل تصويتك!", ephemeral=True)

        # التحقق إذا صوّت الجميع
        if len(self.game.votes) == len(self.game.players) and self.game.is_active:
            self.game.is_active = False
            await self.tally_votes()

    async def tally_votes(self):
        vote_counts = Counter(self.game.votes.values())
        most_common = vote_counts.most_common(2)
        
        # التحقق من التعادل
        is_tie = False
        if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
            is_tie = True

        if is_tie:
            await self.game.channel.send(f"⚖️ **تعادل في التصويت!**\nلم تتمكنوا من الإجماع على شخص واحد. **السالفة كانت:** {self.game.topic}\n🏆 **فاز اللي برا السالفة ({self.game.imposter.mention})!**")
            return

        highest_voted_id = most_common[0][0]
        
        if highest_voted_id == self.game.imposter.id:
            await self.game.channel.send(f"🚨 **كشفتوه!**\nصوت الأغلبية على {self.game.imposter.mention} وهو فعلاً اللي برا السالفة!\n\n👀 **الآن الملاذ الأخير للي برا السالفة:** قدامك 8 خيارات، حاول تختار السالفة الصحيحة لتسرق الفوز!", view=ImposterGuessView(self.game))
        else:
            wrong_person = discord.utils.get(self.game.players, id=highest_voted_id)
            await self.game.channel.send(f"❌ **صوتوا على الشخص الغلط!**\nالأغلبية اختارت {wrong_person.mention}، لكن اللي برا السالفة كان **{self.game.imposter.mention}**!\n**السالفة كانت:** {self.game.topic}\n🏆 **فاز اللي برا السالفة!**")

class ActiveGameView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label="📜 وش السالفة؟", style=discord.ButtonStyle.primary, custom_id="btn_show_topic")
    async def btn_show_topic(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.game.players:
            await interaction.response.send_message("❌ أنت لست في اللعبة!", ephemeral=True)
            return

        if interaction.user == self.game.imposter:
            await interaction.response.send_message("🕵️ **أنت برا السالفة!**\nحاول تندمج معاهم وتفهم السالفة من أسئلتهم بدون ما ينتبهون لك.", ephemeral=True)
        else:
            await interaction.response.send_message(f"📖 **السالفة هي:** ( {self.game.topic} )\nالتصنيف: {self.game.category}", ephemeral=True)

    @discord.ui.button(label="🗣️ من يسأل؟", style=discord.ButtonStyle.secondary, custom_id="btn_next_turn")
    async def btn_next_turn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.game.players:
            await interaction.response.send_message("❌ أنت لست في اللعبة!", ephemeral=True)
            return

        current_player = self.game.players[self.game.turn_index]
        self.game.turn_index = (self.game.turn_index + 1) % len(self.game.players)
        await interaction.response.send_message(f"👉 **الدور الآن على:** {current_player.mention}\nاسأل أي شخص سؤال عن السالفة!")

    @discord.ui.button(label="🗳️ بدء التصويت", style=discord.ButtonStyle.danger, custom_id="btn_vote")
    async def btn_vote(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.game.players:
            await interaction.response.send_message("❌ أنت لست في اللعبة!", ephemeral=True)
            return
        
        if not self.game.is_active:
            await interaction.response.send_message("❌ اللعبة انتهت أو جاري فرز الأصوات.", ephemeral=True)
            return

        if interaction.user.id in self.game.votes:
            await interaction.response.send_message("❌ لقد قمت بالتصويت بالفعل!", ephemeral=True)
            return

        view = discord.ui.View()
        view.add_item(VoteSelect(self.game))
        await interaction.response.send_message("🎯 **اختر من تعتقد أنه برا السالفة:**", view=view, ephemeral=True)

    @discord.ui.button(label="❌ إنهاء اللعبة", style=discord.ButtonStyle.secondary, custom_id="btn_cancel_game", row=1)
    async def btn_cancel_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.game.host:
            await interaction.response.send_message("❌ صاحب اللعبة فقط يمكنه إنهاء اللعبة!", ephemeral=True)
            return

        self.game.is_active = False
        
        for child in self.children:
            child.disabled = True
            
        await interaction.response.edit_message(content="🛑 **تم إلغاء اللعبة بواسطة صاحب اللعبة.**", embed=None, view=self)

class CategorySelectView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.select(
        placeholder="اختر تصنيف السالفة...",
        min_values=1,
        max_values=1,
        options=[discord.SelectOption(label=cat) for cat in WORDS_BANK.keys()]
    )
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user != self.game.host:
            await interaction.response.send_message("❌ صاحب اللعبة فقط يمكنه اختيار التصنيف!", ephemeral=True)
            return

        selected_category = select.values[0]
        self.game.setup_game(selected_category)

        select.disabled = True
        await interaction.response.edit_message(view=self.view)

        embed = discord.Embed(
            title="🎮 بدأت اللعبة!",
            description=f"التصنيف: **{selected_category}**\n\nاضغط على (📜 وش السالفة؟) لتعرف دورك.\nاضغط (🗣️ من يسأل؟) لمعرفة دور من في السؤال.\nاذا شكيتوا بأحد اضغطوا (🗳️ بدء التصويت).",
            color=discord.Color.green()
        )
        await self.game.channel.send(embed=embed, view=ActiveGameView(self.game))

class LobbyView(discord.ui.View):
    def __init__(self, host):
        super().__init__(timeout=30.0) 
        self.host = host
        self.players = [host]
        self.message = None

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        
        try:
            if len(self.players) < 3:
                await self.message.edit(content="⏳ **انتهى الوقت!**\nالعدد غير كافٍ لبدء اللعبة (الحد الأدنى 3 لاعبين).", view=self)
            else:
                await self.message.edit(content=f"✅ **اكتمل العدد وانتهى وقت الانضمام.**\nاللاعبين: {len(self.players)}", view=self)
                game = GameSession(self.message.channel, self.host, self.players)
                
                embed = discord.Embed(
                    title="⚙️ إعدادات اللعبة",
                    description=f"{self.host.mention}، الرجاء اختيار تصنيف الكلمات للبدء:",
                    color=discord.Color.blue()
                )
                await self.message.channel.send(embed=embed, view=CategorySelectView(game))
                
        except discord.NotFound:
            pass
        except Exception as e:
            print(f"حدث خطأ غير متوقع في on_timeout: {e}")

    @discord.ui.button(label="دخول 📥", style=discord.ButtonStyle.success)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.players:
            await interaction.response.send_message("✅ أنت منضم بالفعل!", ephemeral=True)
            return

        self.players.append(interaction.user)
        players_mentions = " - ".join([p.mention for p in self.players])
        
        embed = self.message.embeds[0]
        embed.description = f"اضغط على الزر بالأسفل للانضمام!\n⏳ **المدة:** 30 ثانية\n\n👥 **اللاعبين ({len(self.players)}):**\n{players_mentions}"
        await interaction.response.edit_message(embed=embed)

class SalfaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="سالفة")
    async def start_salfa(self, ctx):
        embed = discord.Embed(
            title="🕵️ لعبة برا السالفة",
            description=f"اضغط على الزر بالأسفل للانضمام!\n⏳ **المدة:** 30 ثانية\n\n👥 **اللاعبين (1):**\n{ctx.author.mention}",
            color=discord.Color.dark_red()
        )
        view = LobbyView(ctx.author)
        view.message = await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(SalfaCog(bot))