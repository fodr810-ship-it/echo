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
    "🥦", "🥬", "🥒", "🌶️", "🫑", "🌽", "🥕", "🫒", "🧄", "🧅",
    "🥔", "🍠", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🥚", "🍳",
    "🧈", "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🌭", "🍔", "🍟",
    "🍕", "🫓", "🥪", "🥙", "🧆", "🌮", "🌯", "🫔", "🥗", "🥘"
]

class EmojiGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # حفظ الرومات النشطة لمنع تداخل الألعاب
        self.active_channels = set()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # الكلمة اللي تشغل اللعبة
        if message.content == "ايموجي":
            
            # التأكد إن ما فيه لعبة شغالة بنفس الروم
            if message.channel.id in self.active_channels:
                await message.channel.send("⏳ فيه لعبة شغالة حالياً في هذا الروم، انتظر تخلص!")
                return

            self.active_channels.add(message.channel.id)

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

                user_id = str(msg.author.id)

                # ----------------------------------------------------
                # فتح ملف النقاط الموحد وإضافة النقطة مباشرة
                try:
                    with open("points.json", "r", encoding="utf-8") as f:
                        db = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    db = {}
                    
                db[user_id] = db.get(user_id, 0) + 1
                current_points = db[user_id]
                
                with open("points.json", "w", encoding="utf-8") as f:
                    json.dump(db, f, indent=4)
                # ----------------------------------------------------

                # إمبد الفوز
                win_embed = discord.Embed(
                    title="🎉 أسرع أصابع!",
                    description=f"مبروك {msg.author.mention}، أرسلت الإيموجي أول واحد! {target_emoji}",
                    color=discord.Color.green()
                )

                # زر عرض النقاط
                view = discord.ui.View()
                btn = discord.ui.Button(
                    label=f"نقاطك: {current_points}",
                    style=discord.ButtonStyle.success,
                    disabled=True
                )
                view.add_item(btn)

                await message.channel.send(embed=win_embed, view=view)

            except asyncio.TimeoutError:
                # إذا محد جاوب خلال الوقت
                timeout_embed = discord.Embed(
                    title="⏳ انتهى الوقت!",
                    description=f"محد قدر يرسل الإيموجي في الوقت المحدد.\nالإيموجي كان: {target_emoji}",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=timeout_embed)

            finally:
                # إزالة الروم من القائمة عشان يقدرون يلعبون مرة ثانية
                self.active_channels.remove(message.channel.id)

async def setup(bot):
    await bot.add_cog(EmojiGameCog(bot))