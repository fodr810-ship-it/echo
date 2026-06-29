import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class ashbkgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "صقر.png", "answer": "صقر"},
            {"image": "نمر.png", "answer": "نمر"},
            {"image": "أسد.png", "answer": "أسد"},
            {"image": "غزال.png", "answer": "غزال"},
            {"image": "ثعلب.png", "answer": "ثعلب"},
            {"image": "ذئب.png", "answer": "ذئب"},
            {"image": "جمل.png", "answer": "جمل"},
            {"image": "حصان.png", "answer": "حصان"},
            {"image": "أرنب.png", "answer": "أرنب"},
            {"image": "فهد.png", "answer": "فهد"},
            {"image": "تفاح.png", "answer": "تفاح"},
            {"image": "موز.png", "answer": "موز"},
            {"image": "عنب.png", "answer": "عنب"},
            {"image": "تمر.png", "answer": "تمر"},
            {"image": "خوخ.png", "answer": "خوخ"},
            {"image": "رمان.png", "answer": "رمان"},
            {"image": "ليمون.png", "answer": "ليمون"},
            {"image": "بطيخ.png", "answer": "بطيخ"},
            {"image": "كرز.png", "answer": "كرز"},
            {"image": "مانجو.png", "answer": "مانجو"},
            {"image": "كتاب.png", "answer": "كتاب"},
            {"image": "قلم.png", "answer": "قلم"},
            {"image": "دفتر.png", "answer": "دفتر"},
            {"image": "مكتب.png", "answer": "مكتب"},
            {"image": "كرسي.png", "answer": "كرسي"},
            {"image": "باب.png", "answer": "باب"},
            {"image": "نافذة.png", "answer": "نافذة"},
            {"image": "ساعة.png", "answer": "ساعة"},
            {"image": "مفتاح.png", "answer": "مفتاح"},
            {"image": "هاتف.png", "answer": "هاتف"},
            {"image": "شمس.png", "answer": "شمس"},
            {"image": "قمر.png", "answer": "قمر"},
            {"image": "نجم.png", "answer": "نجم"},
            {"image": "بحر.png", "answer": "بحر"},
            {"image": "نهر.png", "answer": "نهر"},
            {"image": "جبل.png", "answer": "جبل"},
            {"image": "سحاب.png", "answer": "سحاب"},
            {"image": "مطر.png", "answer": "مطر"},
            {"image": "شجرة.png", "answer": "شجرة"},
            {"image": "وردة.png", "answer": "وردة"},
            {"image": "الرياض.png", "answer": "الرياض"},
            {"image": "مكة.png", "answer": "مكة"},
            {"image": "جدة.png", "answer": "جدة"},
            {"image": "الدمام.png", "answer": "الدمام"},
            {"image": "أبها.png", "answer": "أبها"},
            {"image": "تبوك.png", "answer": "تبوك"},
            {"image": "حائل.png", "answer": "حائل"},
            {"image": "نجران.png", "answer": "نجران"},
            {"image": "جازان.png", "answer": "جازان"},
            {"image": "الخبر.png", "answer": "الخبر"}
        ]

    # 🟢 دالة قراءة النقاط وتحديثها في الملف الموحد مباشرة
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

    @commands.command(name="اشبك")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "اشبك":
            await self.run_game(message.channel)

    async def run_game(self, channel):
        # 🟢 الفحص باستخدام القفل العام لمنع تشغيل اللعبة إذا كانت هناك لعبة أخرى نشطة
        if channel.id in self.bot.global_game_lock:
            return await channel.send("⚠️ هناك لعبة جارية بالفعل في هذا الروم! انتظر حتى تنتهي.")

        q = random.choice(self.questions)
        # 🟢 قفل الروم في البوت كاملاً
        self.bot.global_game_lock.add(channel.id)
        
        # 📂 تحديد مسار المجلد الذي يحتوي على الصور
        image_path = os.path.join("images", q["image"])

        # ⚙️ التحقق من أن ملف الصورة موجود فعلياً في المجلد
        if os.path.exists(image_path):
            file = discord.File(image_path, filename=q["image"])
            await channel.send(file=file)
        else:
            await channel.send(f"⚠️ خطأ: لم يتم العثور على ملف الصورة في المسار: `{image_path}`")
            self.bot.global_game_lock.discard(channel.id) # إلغاء القفل عند الخطأ
            return

        def check(m):
            return m.channel == channel and not m.author.bot

        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=30.0)

                if msg.content.strip() == q["answer"]:
                    # 🟢 تحديث وحفظ النقاط في ملف الجيسون الموحد
                    new_score = self.add_score(msg.author.id)

                    embed = discord.Embed(
                        title="🎉 صحيحة!",
                        description=f"مبروك {msg.author.mention}، لقد فزت في اللعبة!",
                        color=discord.Color.green(),
                    )

                    view = discord.ui.View()
                    button = discord.ui.Button(
                        label=f"نقاطك الإجمالية: {new_score}",
                        style=discord.ButtonStyle.primary,
                        disabled=True,
                    )
                    view.add_item(button)

                    await channel.send(embed=embed, view=view)
                    break 
                else:
                    await msg.add_reaction("❌") 

        except asyncio.TimeoutError:
            await channel.send("⌛ انتهى الوقت! لم يقم أحد بالإجابة الصحيحة.")

        finally:
            # 🟢 فتح القفل العام المشترك فور انتهاء اللعبة
            self.bot.global_game_lock.discard(channel.id)


async def setup(bot):
    await bot.add_cog(ashbkgame(bot))