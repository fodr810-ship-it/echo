import discord
from discord.ext import commands
import random
import asyncio
import json
import os

# قائمة تحتوي على أكثر من 120 إيموجي متنوع
EMOJIS_LIST = [
    # وجوه وتعبيرات
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "🥲", "☺️",
    "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗",
    "😙", "😚", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓",
    "😎", "🥸", "🤩", "🥳", "😏", "😒", "😞", "😔", "😟", "😕",
    "🙁", "☹️", "😣", "😖", "😫", "😩", "🥺", "😢", "😭", "😤",
    "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰",
    "😥", "😓", "🤗", "🤔", "🤭", "🤫", "🤥", "😶", "😐", "😑",
    "😬", "🙄", "😯", "😦", "😧", "😮", "😲", "🥱", "😴", "🤤",
    "😪", "😵", "🤐", "🥴", "🤢", "🤮", "🤧", "😷", "🤒", "🤕",
    "🤑", "🤠", "😈", "👿", "👹", "👺", "🤡", "💩", "👻", "💀",
    "👽", "👾", "🤖", "🎃",
    
    # حيوانات
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐻‍❄️", "🐨",
    "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🐤",
    "🦆", "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🪱",
    "🐛", "🦋", "🐌", "🐞", "🐜", "🪰", "🪲", "🪳", "🦟", "🦗",
    
    # أكل ومشروبات
    "🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐",
    "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑",
    " Broccoli", "🥬", "🥒", "🌶️", "🫑", "🌽", "🥕", "🫒", "🧄", "🧅",
    "🥔", "🍠", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🥚", "🍳",
    "Butter", "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🌭", "🍔", "🍟",
    "🍕", "🫓", "🥪", "🥙", "🧆", "🌮", "🌯", "🫔", "🥗", "🥘"
]

class EmojiGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = "global_points.json" # اسم ملف النقاط الموحد المشترك
        
        # 🟢 ربط القفل العام المشترك داخل كائن البوت لجميع الملفات
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

    # دالة قراءة النقاط وتحديثها في الملف الموحد مباشرة
    def add_score(self, user_id):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r", encoding="utf-8") as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = {}
        else:
            scores = {}
        
        user_id_str = str(user_id)
        scores[user_id_str] = scores.get(user_id_str, 0) + 1
        
        with open(self.scores_file, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)
            
        return scores[user_id_str]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # الكلمة اللي تشغل اللعبة
        if message.content.strip() == "ايموجي":
            
            # 🟢 الفحص باستخدام القفل العام المشترك لمنع التداخل
            if message.channel.id in self.bot.global_game_lock:
                await message.channel.send("⚠️ هناك لعبة جارية بالفعل في هذا الروم! انتظر حتى تنتهي.")
                return

            # قفل الروم في البوت كاملاً لمنع تشغيل أي لعبة أخرى
            self.bot.global_game_lock.add(message.channel.id)

            # اختيار إيموجي عشوائي من القائمة
            target_emoji = random.choice(EMOJIS_LIST)

            # إرسال إمبد اللعبة
            embed = discord.Embed(
                title="🎭 لعبة أسرع إيموجي",
                description=f"أسرع واحد ينسخ أو يكتب هذا الإيموجي في الشات يفوز!\n\n# {target_emoji}",
                color=discord.Color.blurple()
            )
            await message.channel.send(embed=embed)

            # دالة للتحقق من أن الرسالة مطابقة للإيموجي بالضبط
            def check(m):
                return m.channel == message.channel and m.content.strip() == target_emoji and not m.author.bot

            try:
                # انتظار الإجابة لمدة 30 ثانية
                msg = await self.bot.wait_for("message", check=check, timeout=30.0)

                # 🟢 تحديث وحفظ النقاط في ملف الجيسون الموحد المشترك
                new_score = self.add_score(msg.author.id)

                # إمبد الفوز
                win_embed = discord.Embed(
                    title="🎉 أسرع أصابع!",
                    description=f"مبروك {msg.author.mention}، أرسلت الإيموجي أول واحد! {target_emoji}",
                    color=discord.Color.green()
                )

                # زر عرض النقاط الموحد
                view = discord.ui.View()
                btn = discord.ui.Button(
                    label=f"نقاطك الإجمالية: {new_score}",
                    style=discord.ButtonStyle.success,
                    disabled=True
                )
                view.add_item(btn)

                await message.channel.send(embed=win_embed, view=view)

            except asyncio.TimeoutError:
                # إذا محد جاوب خلال الوقت
                timeout_embed = discord.Embed(
                    title="⏳ انتهى الوقت!",
                    description=f"محد قدر يرسل الإيموجي في الوقت المحدد.\nالعلامة كانت: {target_emoji}",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=timeout_embed)

            finally:
                # 🟢 فتح القفل العام المشترك فور انتهاء اللعبة أو الوقت للسماح ببدء ألعاب جديدة
                if message.channel.id in self.bot.global_game_lock:
                    self.bot.global_game_lock.remove(message.channel.id)

async def setup(bot):
    await bot.add_cog(EmojiGameCog(bot))