import discord
from discord.ext import commands
import random

# قائمة كلمات مقترحة (يمكنك تعديلها وإضافة المزيد)
WORD_BANK = [
    "أسد", "قمر", "شمس", "بحر", "جبل", "سيف", "درع", "حصان", "صقر", "نار",
    "جليد", "رياح", "عاصفة", "نجم", "كوكب", "مجرة", "فضاء", "سفينة", "طائرة", "سيارة",
    "قطار", "طريق", "جسر", "برج", "قلعة", "قصر", "خيمة", "صحراء", "غابة", "نهر",
    "بحيرة", "جزيرة", "شاطئ", "رمال", "صخرة", "ذهب", "فضة", "حديد", "نحاس", "خشب",
    "ورق", "قلم", "كتاب", "رسالة", "خريطة", "بوصلة", "كنز", "مفتاح", "قفل", "باب"
]

class HintModal(discord.ui.Modal, title="تقديم تلميح"):
    word = discord.ui.TextInput(
        label="كلمة التلميح",
        placeholder="اكتب كلمة واحدة فقط ترتبط بكلمات فريقك...",
        required=True
    )
    count = discord.ui.TextInput(
        label="عدد الكلمات",
        placeholder="أدخل رقماً (مثال: 2)",
        required=True,
        max_length=1
    )

    def __init__(self, game):
        super().__init__()
        self.game = game

    async def on_submit(self, interaction: discord.Interaction):
        if not self.count.value.isdigit():
            await interaction.response.send_message("❌ الرجاء إدخال رقم صحيح لعدد الكلمات.", ephemeral=True)
            return
        
        self.game.hint_word = self.word.value
        self.game.remaining_guesses = int(self.count.value)
        self.game.hint_given = True

        team_name = "🔴 الأحمر" if self.game.current_turn == "red" else "🔵 الأزرق"
        await interaction.response.send_message(f"✅ تم إرسال التلميح لفريقك بنجاح!", ephemeral=True)
        await self.game.channel.send(f"📢 **تلميح الفريق {team_name}:** الكلمة ( **{self.word.value}** ) - العدد: **{self.count.value}**\nيمكن للأعضاء الآن اختيار الكلمات!")
        await self.game.update_control_panel()

class ControlView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label="تقديم تلميح", style=discord.ButtonStyle.success, custom_id="btn_hint")
    async def hint_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # التحقق من أن الضغاط هو قائد الفريق صاحب الدور
        is_red_turn = self.game.current_turn == "red"
        active_leader = self.game.red_leader if is_red_turn else self.game.blue_leader
        
        if interaction.user != active_leader:
            await interaction.response.send_message("❌ هذا الزر مخصص لقائد الفريق الذي عليه الدور فقط!", ephemeral=True)
            return
        
        if self.game.hint_given:
            await interaction.response.send_message("❌ لقد قمت بتقديم تلميح بالفعل، انتظر حتى ينهي فريقك اختياراته.", ephemeral=True)
            return

        await interaction.response.send_modal(HintModal(self.game))

class BoardButton(discord.ui.Button):
    def __init__(self, word, color, row, game):
        super().__init__(style=discord.ButtonStyle.secondary, label=word, row=row)
        self.word = word
        self.real_color = color
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        # 1. التحقق من أن المستخدم ليس قائداً
        if interaction.user in [self.game.red_leader, self.game.blue_leader]:
            await interaction.response.send_message("❌ القادة لا يمكنهم اختيار الكلمات! الأعضاء فقط من يضغطون الأزرار.", ephemeral=True)
            return

        # 2. التحقق من أن المستخدم عضو في الفريق صاحب الدور
        is_red_turn = self.game.current_turn == "red"
        active_members = self.game.red_members if is_red_turn else self.game.blue_members
        
        if interaction.user not in active_members:
            await interaction.response.send_message("❌ ليس دور فريقك أو أنك لست عضواً في هذا الفريق!", ephemeral=True)
            return

        # 3. التحقق من وجود تلميح ووجود محاولات متبقية
        if not self.game.hint_given:
            await interaction.response.send_message("❌ القائد لم يعطِ تلميحاً بعد!", ephemeral=True)
            return
        
        if self.game.remaining_guesses <= 0:
            await interaction.response.send_message("❌ لقد استنفدتم عدد المحاولات المتاحة لهذا التلميح!", ephemeral=True)
            return

        # كشف الزر
        self.disabled = True
        self.game.remaining_guesses -= 1

        if self.real_color == "red":
            self.style = discord.ButtonStyle.danger
            if is_red_turn:
                self.game.red_score += 1
            else:
                self.game.red_score += 1 # الفريق الأزرق ضغط أحمر بالخطأ
        elif self.real_color == "blue":
            self.style = discord.ButtonStyle.primary
            if not is_red_turn:
                self.game.blue_score += 1
            else:
                self.game.blue_score += 1 # الفريق الأحمر ضغط أزرق بالخطأ
        else:
            self.style = discord.ButtonStyle.success # اللون الأسود (اخترت أخضر كـ لون مميز للموت أو يمكنك تركه رمادي غامق)
            self.label = f"💀 {self.word}"

        await interaction.response.edit_message(view=self.view)

        # منطق الفوز والخسارة وتغيير الدور
        if self.real_color == "black":
            loser = "🔴 الأحمر" if is_red_turn else "🔵 الأزرق"
            winner = "🔵 الأزرق" if is_red_turn else "🔴 الأحمر"
            await self.game.channel.send(f"💀 **كارثة!** قام فريق {loser} باختيار الكلمة السوداء!\n🏆 **الفريق الفائز هو {winner}!**")
            await self.game.end_game()
            return

        if self.game.red_score == 11:
            await self.game.channel.send("🏆 **فاز الفريق الأحمر 🔴 بجميع كلماته!**")
            await self.game.end_game()
            return
        elif self.game.blue_score == 11:
            await self.game.channel.send("🏆 **فاز الفريق الأزرق 🔵 بجميع كلماته!**")
            await self.game.end_game()
            return

        # تغيير الدور إذا ضغط لون الفريق الخصم أو انتهت المحاولات
        if (is_red_turn and self.real_color != "red") or (not is_red_turn and self.real_color != "blue") or (self.game.remaining_guesses == 0):
            await self.game.switch_turn()

class BoardView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        row = 0
        count = 0
        for word, color in self.game.words_dict.items():
            self.add_item(BoardButton(word, color, row, game))
            count += 1
            if count % 5 == 0:
                row += 1

class GameSession:
    def __init__(self, channel, red_leader, blue_leader, red_members, blue_members):
        self.channel = channel
        self.red_leader = red_leader
        self.blue_leader = blue_leader
        self.red_members = red_members
        self.blue_members = blue_members
        
        self.red_score = 0
        self.blue_score = 0
        self.current_turn = random.choice(["red", "blue"])
        
        self.hint_word = None
        self.remaining_guesses = 0
        self.hint_given = False
        
        self.board_msg = None
        self.control_msg = None
        self.words_dict = self.generate_board()

    def generate_board(self):
        chosen_words = random.sample(WORD_BANK, 25)
        # 11 أحمر، 11 أزرق، 3 أسود
        colors = ['red']*11 + ['blue']*11 + ['black']*3
        random.shuffle(colors)
        return dict(zip(chosen_words, colors))

    async def start(self):
        # إرسال الكلمات في الخاص للقادة
        red_words = [w for w, c in self.words_dict.items() if c == "red"]
        blue_words = [w for w, c in self.words_dict.items() if c == "blue"]
        black_words = [w for w, c in self.words_dict.items() if c == "black"]

        red_msg = f"🔴 **أنت قائد الفريق الأحمر** 🔴\nكلمات فريقك (11): {', '.join(red_words)}\n💀 الكلمات السوداء (تجنبها!): {', '.join(black_words)}"
        blue_msg = f"🔵 **أنت قائد الفريق الأزرق** 🔵\nكلمات فريقك (11): {', '.join(blue_words)}\n💀 الكلمات السوداء (تجنبها!): {', '.join(black_words)}"

        try:
            await self.red_leader.send(red_msg)
            await self.blue_leader.send(blue_msg)
        except discord.Forbidden:
            await self.channel.send("⚠️ تنبيه: أحد القادة أو كلاهما مقفل رسائل الخاص! اللعبة تتطلب فتح الخاص لرؤية الكلمات.")

        # إشعار الأعضاء في الخاص
        for member in self.red_members:
            try:
                await member.send("🔴 **أنت عضو عادي في الفريق الأحمر** 🔴\nانتظر تلميح قائدك واضغط على الأزرار الصحيحة في السيرفر!")
            except discord.Forbidden:
                pass
        for member in self.blue_members:
            try:
                await member.send("🔵 **أنت عضو عادي في الفريق الأزرق** 🔵\nانتظر تلميح قائدك واضغط على الأزرار الصحيحة في السيرفر!")
            except discord.Forbidden:
                pass

        # إرسال رسالة البورد والتحكم
        turn_str = "🔴 الأحمر" if self.current_turn == "red" else "🔵 الأزرق"
        await self.channel.send(f"🎲 **بدأت اللعبة!** الدور الأول عشوائياً لفريق: **{turn_str}**")
        
        self.board_msg = await self.channel.send(view=BoardView(self))
        self.control_msg = await self.channel.send(f"🎮 لوحة تحكم القادة | الدور الحالي: {turn_str}", view=ControlView(self))

    async def switch_turn(self):
        self.current_turn = "blue" if self.current_turn == "red" else "red"
        self.hint_given = False
        self.hint_word = None
        self.remaining_guesses = 0
        turn_str = "🔴 الأحمر" if self.current_turn == "red" else "🔵 الأزرق"
        await self.channel.send(f"🔄 **انتهى الدور!** الدور الآن لفريق: **{turn_str}**\nننتظر تلميح القائد...")
        await self.update_control_panel()

    async def update_control_panel(self):
        if self.control_msg:
            turn_str = "🔴 الأحمر" if self.current_turn == "red" else "🔵 الأزرق"
            await self.control_msg.edit(content=f"🎮 لوحة تحكم القادة | الدور الحالي: {turn_str}", view=ControlView(self))

    async def end_game(self):
        if self.control_msg:
            await self.control_msg.edit(content="🏁 **انتهت اللعبة!**", view=None)

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.red_leader = None
        self.blue_leader = None
        self.red_members = set()
        self.blue_members = set()

    @discord.ui.button(label="قائد أحمر 🔴", style=discord.ButtonStyle.danger)
    async def btn_red_leader(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.red_leader = interaction.user
        if interaction.user in self.red_members: self.red_members.remove(interaction.user)
        await interaction.response.send_message("✅ أصبحت قائد الفريق الأحمر!", ephemeral=True)

    @discord.ui.button(label="عضو أحمر 🔴", style=discord.ButtonStyle.secondary)
    async def btn_red_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.red_members.add(interaction.user)
        if self.red_leader == interaction.user: self.red_leader = None
        await interaction.response.send_message("✅ انضممت كعضو للفريق الأحمر!", ephemeral=True)

    @discord.ui.button(label="قائد أزرق 🔵", style=discord.ButtonStyle.primary)
    async def btn_blue_leader(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.blue_leader = interaction.user
        if interaction.user in self.blue_members: self.blue_members.remove(interaction.user)
        await interaction.response.send_message("✅ أصبحت قائد الفريق الأزرق!", ephemeral=True)

    @discord.ui.button(label="عضو أزرق 🔵", style=discord.ButtonStyle.secondary)
    async def btn_blue_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.blue_members.add(interaction.user)
        if self.blue_leader == interaction.user: self.blue_leader = None
        await interaction.response.send_message("✅ انضممت كعضو للفريق الأزرق!", ephemeral=True)

    @discord.ui.button(label="بدء اللعبة ▶️", style=discord.ButtonStyle.success, row=1)
    async def btn_start(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.red_leader or not self.blue_leader:
            await interaction.response.send_message("❌ يجب أن يكون هناك قائد لكل فريق لبدء اللعبة!", ephemeral=True)
            return
        if not self.red_members or not self.blue_members:
            await interaction.response.send_message("❌ يجب أن يكون هناك عضو واحد على الأقل في كل فريق!", ephemeral=True)
            return

        await interaction.response.send_message("✅ جاري تجهيز اللعبة...", ephemeral=True)
        self.stop()
        game = GameSession(
            interaction.channel, 
            self.red_leader, 
            self.blue_leader, 
            list(self.red_members), 
            list(self.blue_members)
        )
        await game.start()

class CodenamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="codenames", aliases=["كودنيمز"])
    async def start_setup(self, ctx):
        embed = discord.Embed(
            title="🎯 لعبة Codenames", 
            description="اضغط على الأزرار بالأسفل للانضمام إلى الفرق. يجب وجود قائد وأعضاء لكل فريق.",
            color=discord.Color.dark_theme()
        )
        view = SetupView()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(CodenamesCog(bot))