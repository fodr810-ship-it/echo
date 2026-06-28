import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class gmagame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "gma_scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "جمع_1.png", "answer": "أقلام"},
            {"image": "جمع_2.png", "answer": "كتب"},
            {"image": "جمع_3.png", "answer": "طاولات"},
            {"image": "جمع_4.png", "answer": "كراسي"},
            {"image": "جمع_5.png", "answer": "هواتف"},
            {"image": "جمع_6.png", "answer": "حقائب"},
            {"image": "جمع_7.png", "answer": "مفاتيح"},
            {"image": "جمع_8.png", "answer": "أبواب"},
            {"image": "جمع_9.png", "answer": "نوافذ"},
            {"image": "جمع_10.png", "answer": "سيارات"},
            {"image": "جمع_11.png", "answer": "شموس"},
            {"image": "جمع_12.png", "answer": "أقمار"},
            {"image": "جمع_13.png", "answer": "نجوم"},
            {"image": "جمع_14.png", "answer": "سماوات"},
            {"image": "جمع_15.png", "answer": "بحار"},
            {"image": "جمع_16.png", "answer": "أشجار"},
            {"image": "جمع_17.png", "answer": "ورود"},
            {"image": "جمع_18.png", "answer": "عصافير"},
            {"image": "جمع_19.png", "answer": "قطط"},
            {"image": "جمع_20.png", "answer": "كلاب"},
            {"image": "جمع_21.png", "answer": "أحباب"},
            {"image": "جمع_22.png", "answer": "سلامات"},
            {"image": "جمع_23.png", "answer": "حيوات"},
            {"image": "جمع_24.png", "answer": "أوقات"},
            {"image": "جمع_25.png", "answer": "أعمال"},
            {"image": "جمع_26.png", "answer": "علوم"},
            {"image": "جمع_27.png", "answer": "نجاحات"},
            {"image": "جمع_28.png", "answer": "أهداف"},
            {"image": "جمع_29.png", "answer": "أحلام"},
            {"image": "جمع_30.png", "answer": "أفكار"},
            {"image": "جمع_31.png", "answer": "طرق"},
            {"image": "جمع_32.png", "answer": "أنوار"},
            {"image": "جمع_33.png", "answer": "ظلال"},
            {"image": "جمع_34.png", "answer": "أصوات"},
            {"image": "جمع_35.png", "answer": "ألوان"},
            {"image": "جمع_36.png", "answer": "أشكال"},
            {"image": "جمع_37.png", "answer": "سرعات"},
            {"image": "جمع_38.png", "answer": "قوى"},
            {"image": "جمع_39.png", "answer": "حريات"},
            {"image": "جمع_40.png", "answer": "شجاعات"},
            {"image": "جمع_41.png", "answer": "أكلات"},
            {"image": "جمع_42.png", "answer": "مشروبات"},
            {"image": "جمع_43.png", "answer": "كتابات"},
            {"image": "جمع_44.png", "answer": "قراءات"},
            {"image": "جمع_45.png", "answer": "منامات"},
            {"image": "جمع_46.png", "answer": "مشيات"},
            {"image": "جمع_47.png", "answer": "جريات"},
            {"image": "جمع_48.png", "answer": "ألعاب"},
            {"image": "جمع_49.png", "answer": "رسومات"},
            {"image": "جمع_50.png", "answer": "شواهد"},
            {"image": "جمع_51.png", "answer": "استماعات"},
            {"image": "جمع_52.png", "answer": "تكلمات"},
            {"image": "جمع_53.png", "answer": "تعلمات"},
            {"image": "جمع_54.png", "answer": "سفرات"},
            {"image": "جمع_55.png", "answer": "بحوث"},
            {"image": "جمع_56.png", "answer": "وجدات"},
            {"image": "جمع_57.png", "answer": "فتوحات"},
            {"image": "جمع_58.png", "answer": "إغلاقات"},
            {"image": "جمع_59.png", "answer": "صناعات"},
            {"image": "جمع_60.png", "answer": "بنيات"},
            {"image": "جمع_61.png", "answer": "جميلات"},
            {"image": "جمع_62.png", "answer": "كبار"},
            {"image": "جمع_63.png", "answer": "صغار"},
            {"image": "جمع_64.png", "answer": "سراع"},
            {"image": "جمع_65.png", "answer": "بطيئون"},
            {"image": "جمع_66.png", "answer": "أقوياء"},
            {"image": "جمع_67.png", "answer": "ضعفاء"},
            {"image": "جمع_68.png", "answer": "أذكياء"},
            {"image": "جمع_69.png", "answer": "سعداء"},
            {"image": "جمع_70.png", "answer": "حزناء"},
            {"image": "جمع_71.png", "answer": "نظيفون"},
            {"image": "جمع_72.png", "answer": "جدد"},
            {"image": "جمع_73.png", "answer": "قدماء"},
            {"image": "جمع_74.png", "answer": "غالون"},
            {"image": "جمع_75.png", "answer": "رخاص"},
            {"image": "جمع_76.png", "answer": "واسعون"},
            {"image": "جمع_77.png", "answer": "ضيقون"},
            {"image": "جمع_78.png", "answer": "عالون"},
            {"image": "جمع_79.png", "answer": "منخفضون"},
            {"image": "جمع_80.png", "answer": "سهول"}
           
        
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

    @commands.command(name="جمع")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "جمع":
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
    await bot.add_cog(gmagame(bot))