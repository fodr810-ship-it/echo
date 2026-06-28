import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class ashbkgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "ashbk_scores.json"
        self.scores = self.load_scores()
        
        # 💡 هنا تضع اسم ملف الصورة فقط المتواجد داخل مجلد images (مثال: دراسة.png)
        self.questions = [
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
        ]
        self.lock = False

    def load_scores(self):
        return (
            json.load(open(self.scores_file, "r"))
            if os.path.exists(self.scores_file)
            else {}
        )

    def save_scores(self):
        with open(self.scores_file, "w") as f:
            json.dump(self.scores, f)

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
        if self.lock:
            return await channel.send("اللعبة جارية بالفعل!")

        q = random.choice(self.questions)
        self.lock = True
        
        # 📂 تحديد مسار المجلد الذي يحتوي على الصور
        image_path = os.path.join("images", q["image"])

        # ⚙️ التحقق من أن ملف الصورة موجود فعلياً في المجلد لتجنب كراش البوت
        if os.path.exists(image_path):
            # رفع الصورة كملف حقيقي إلى ديسكورد
            file = discord.File(image_path, filename=q["image"])
            await channel.send(file=file)
        else:
            # حل بديل ذكي في حال نسيان إضافة الصورة للمجلد
            await channel.send(f"⚠️ خطأ: لم يتم العثور على ملف الصورة في المسار: `{image_path}`")
            self.lock = False
            return

        def check(m):
            return m.channel == channel and not m.author.bot

        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=30.0)

                if msg.content.strip() == q["answer"]:
                    user_id = str(msg.author.id)
                    self.scores[user_id] = self.scores.get(user_id, 0) + 1
                    self.save_scores()

                    embed = discord.Embed(
                        title="🎉 صحيحة!",
                        description=f"مبروك {msg.author.mention}، لقد فزت في اللعبة!",
                        color=discord.Color.red(),
                    )

                    view = discord.ui.View()
                    button = discord.ui.Button(
                        label=f"نقاطك: {self.scores[user_id]}",
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

        self.lock = False


async def setup(bot):
    await bot.add_cog(ashbkgame(bot))