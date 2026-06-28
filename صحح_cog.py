import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class ssagame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "ssa_scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "صحح_1.png", "answer": "مسؤول"},
            {"image": "صحح_2.png", "answer": "هبة"},
            {"image": "صحح_3.png", "answer": "يقرؤون"},
            {"image": "صحح_4.png", "answer": "شاطئ"},
            {"image": "صحح_5.png", "answer": "عبء"},
            {"image": "صحح_6.png", "answer": "ملجأ"},
            {"image": "صحح_7.png", "answer": "دافئ"},
            {"image": "صحح_8.png", "answer": "إبراهيم"},
            {"image": "صحح_9.png", "answer": "أحمد"},
            {"image": "صحح_10.png", "answer": "إسلام"},
            {"image": "صحح_11.png", "answer": "أكل"},
            {"image": "صحح_12.png", "answer": "أمر"},
            {"image": "صحح_13.png", "answer": "إنتاج"},
            {"image": "صحح_14.png", "answer": "إيمان"},
            {"image": "صحح_15.png", "answer": "استجابة"},
            {"image": "صحح_16.png", "answer": "ارتفاع"},
            {"image": "صحح_17.png", "answer": "اقتراح"},
            {"image": "صحح_18.png", "answer": "ابتكار"},
            {"image": "صحح_19.png", "answer": "مدرسة"},
            {"image": "صحح_20.png", "answer": "شجرة"},
            {"image": "صحح_21.png", "answer": "حديقة"},
            {"image": "صحح_22.png", "answer": "مكتبة"},
            {"image": "صحح_23.png", "answer": "سيارة"},
            {"image": "صحح_24.png", "answer": "طائرة"},
            {"image": "صحح_25.png", "answer": "جامعة"},
            {"image": "صحح_26.png", "answer": "ورقة"},
            {"image": "صحح_27.png", "answer": "فكرة"},
            {"image": "صحح_28.png", "answer": "ساعة"},
            {"image": "صحح_29.png", "answer": "وجوه"},
            {"image": "صحح_30.png", "answer": "مياه"},
            {"image": "صحح_31.png", "answer": "فواكه"},
            {"image": "صحح_32.png", "answer": "له"},
            {"image": "صحح_33.png", "answer": "عنده"},
            {"image": "صحح_34.png", "answer": "وجه"},
            {"image": "صحح_35.png", "answer": "كتابة"},
            {"image": "صحح_36.png", "answer": "استمارة"},
            {"image": "صحح_37.png", "answer": "نظافة"},
            {"image": "صحح_38.png", "answer": "مستشفى"},
            {"image": "صحح_39.png", "answer": "شتاء"},
            {"image": "صحح_40.png", "answer": "قراءة"},
            {"image": "صحح_41.png", "answer": "دواء"},
            {"image": "صحح_42.png", "answer": "شيء"},
            {"image": "صحح_43.png", "answer": "إظهار"},
            {"image": "صحح_44.png", "answer": "جائزة"},
            {"image": "صحح_45.png", "answer": "دعوى"},
            {"image": "صحح_46.png", "answer": "لكن"},
            {"image": "صحح_47.png", "answer": "ذلك"},
            {"image": "صحح_48.png", "answer": "إذن"},
            {"image": "صحح_49.png", "answer": "إن شاء الله"},
            {"image": "صحح_50.png", "answer": "مئة"},
            {"image": "صحح_51.png", "answer": "قرآن"},
            {"image": "صحح_52.png", "answer": "تائبة"},
            {"image": "صحح_53.png", "answer": "بدأ"},
            {"image": "صحح_54.png", "answer": "ملء"},
            {"image": "صحح_55.png", "answer": "قرأ"},
            {"image": "صحح_56.png", "answer": "جزء"},
            {"image": "صحح_57.png", "answer": "ضوء"},
            {"image": "صحح_58.png", "answer": "بطيء"},
            {"image": "صحح_59.png", "answer": "شيء"},
            {"image": "صحح_60.png", "answer": "وضوء"},
            {"image": "صحح_61.png", "answer": "مساحة"},
            {"image": "صحح_62.png", "answer": "طاولة"},
            {"image": "صحح_63.png", "answer": "مروحة"},
            {"image": "صحح_64.png", "answer": "لوحة"},
            {"image": "صحح_65.png", "answer": "خريطة"},
            {"image": "صحح_66.png", "answer": "حقيبة"},
            {"image": "صحح_67.png", "answer": "نافذة"},
            {"image": "صحح_68.png", "answer": "قلادة"},
            {"image": "صحح_69.png", "answer": "رسالة"},
            {"image": "صحح_70.png", "answer": "سارة"},
            {"image": "صحح_71.png", "answer": "ليلى"},
            {"image": "صحح_72.png", "answer": "مصطفى"},
            {"image": "صحح_73.png", "answer": "مستشفى"},
            {"image": "صحح_74.png", "answer": "عصا"},
            {"image": "صحح_75.png", "answer": "فتى"},
            {"image": "صحح_76.png", "answer": "رمى"},
            {"image": "صحح_77.png", "answer": "سقى"},
            {"image": "صحح_78.png", "answer": "بنى"},
            {"image": "صحح_79.png", "answer": "صلاة"},
            {"image": "صحح_80.png", "answer": "زكاة"},
           
        
           
            
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

    @commands.command(name="صحح")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "صحح":
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
    await bot.add_cog(ssagame(bot))