import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class fastgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "asr3_scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "اسرع_1.png", "answer": "شمس"},
            {"image": "اسرع_2.png", "answer": "قمر"},
            {"image": "اسرع_3.png", "answer": "سماء"},
            {"image": "اسرع_4.png", "answer": "أرض"},
            {"image": "اسرع_5.png", "answer": "بحر"},
            {"image": "اسرع_6.png", "answer": "جبل"},
            {"image": "اسرع_7.png", "answer": "شجرة"},
            {"image": "اسرع_8.png", "answer": "وردة"},
            {"image": "اسرع_9.png", "answer": "كتاب"},
            {"image": "اسرع_10.png", "answer": "قلم"},
            {"image": "اسرع_11.png", "answer": "سيارة"},
            {"image": "اسرع_12.png", "answer": "طائرة"},
            {"image": "اسرع_13.png", "answer": "قطار"},
            {"image": "اسرع_14.png", "answer": "بيت"},
            {"image": "اسرع_15.png", "answer": "باب"},
            {"image": "اسرع_16.png", "answer": "نافذة"},
            {"image": "اسرع_17.png", "answer": "مكتب"},
            {"image": "اسرع_18.png", "answer": "كرسي"},
            {"image": "اسرع_19.png", "answer": "هاتف"},
            {"image": "اسرع_20.png", "answer": "حاسوب"},
            {"image": "اسرع_21.png", "answer": "طريق"},
            {"image": "اسرع_22.png", "answer": "مدينة"},
            {"image": "اسرع_23.png", "answer": "قرية"},
            {"image": "اسرع_24.png", "answer": "شارع"},
            {"image": "اسرع_25.png", "answer": "حديقة"},
            {"image": "اسرع_26.png", "answer": "مدرسة"},
            {"image": "اسرع_27.png", "answer": "جامعة"},
            {"image": "اسرع_28.png", "answer": "مستشفى"},
            {"image": "اسرع_29.png", "answer": "مطعم"},
            {"image": "اسرع_30.png", "answer": "فندق"},
            {"image": "اسرع_31.png", "answer": "صباح"},
            {"image": "اسرع_32.png", "answer": "مساء"},
            {"image": "اسرع_33.png", "answer": "ليل"},
            {"image": "اسرع_34.png", "answer": "نهار"},
            {"image": "اسرع_35.png", "answer": "وقت"},
            {"image": "اسرع_36.png", "answer": "ساعة"},
            {"image": "اسرع_37.png", "answer": "دقيقة"},
            {"image": "اسرع_38.png", "answer": "ثانية"},
            {"image": "اسرع_39.png", "answer": "أسبوع"},
            {"image": "اسرع_40.png", "answer": "شهر"},
            {"image": "اسرع_41.png", "answer": "سنة"},
            {"image": "اسرع_42.png", "answer": "ربيع"},
            {"image": "اسرع_43.png", "answer": "صيف"},
            {"image": "اسرع_44.png", "answer": "خريف"},
            {"image": "اسرع_45.png", "answer": "شتاء"},
            {"image": "اسرع_46.png", "answer": "هواء"},
            {"image": "اسرع_47.png", "answer": "ماء"},
            {"image": "اسرع_48.png", "answer": "نار"},
            {"image": "اسرع_49.png", "answer": "تراب"},
            {"image": "اسرع_50.png", "answer": "رياح"},
            {"image": "اسرع_51.png", "answer": "مطر"},
            {"image": "اسرع_52.png", "answer": "ثلج"},
            {"image": "اسرع_53.png", "answer": "سحاب"},
            {"image": "اسرع_54.png", "answer": "عاصفة"},
            {"image": "اسرع_55.png", "answer": "سلام"},
            {"image": "اسرع_56.png", "answer": "حب"},
            {"image": "اسرع_57.png", "answer": "أمل"},
            {"image": "اسرع_58.png", "answer": "حلم"},
            {"image": "اسرع_59.png", "answer": "حقيقة"},
            {"image": "اسرع_60.png", "answer": "خيال"},
            {"image": "اسرع_61.png", "answer": "علم"},
            {"image": "اسرع_62.png", "answer": "فن"},
            {"image": "اسرع_63.png", "answer": "تاريخ"},
            {"image": "اسرع_64.png", "answer": "لغة"},
            {"image": "اسرع_65.png", "answer": "كلمة"},
            {"image": "اسرع_66.png", "answer": "حرف"},
            {"image": "اسرع_67.png", "answer": "رقم"},
            {"image": "اسرع_68.png", "answer": "لون"},
            {"image": "اسرع_69.png", "answer": "أحمر"},
            {"image": "اسرع_70.png", "answer": "أزرق"},
            {"image": "اسرع_71.png", "answer": "أخضر"},
            {"image": "اسرع_72.png", "answer": "أصفر"},
            {"image": "اسرع_73.png", "answer": "أسود"},
            {"image": "اسرع_74.png", "answer": "أبيض"},
            {"image": "اسرع_75.png", "answer": "قلب"},
            {"image": "اسرع_76.png", "answer": "عقل"},
            {"image": "اسرع_77.png", "answer": "عين"},
            {"image": "اسرع_78.png", "answer": "أذن"},
            {"image": "اسرع_79.png", "answer": "يد"},
            {"image": "اسرع_80.png", "answer": "قدم"},
            {"image": "اسرع_81.png", "answer": "رجل"},
            {"image": "اسرع_82.png", "answer": "امرأة"},
            {"image": "اسرع_83.png", "answer": "طفل"},
            {"image": "اسرع_84.png", "answer": "صديق"},
            {"image": "اسرع_85.png", "answer": "عائلة"},
            {"image": "اسرع_86.png", "answer": "أخ"},
            {"image": "اسرع_87.png", "answer": "أخت"},
            {"image": "اسرع_88.png", "answer": "أب"},
            {"image": "اسرع_89.png", "answer": "أم"},
            {"image": "اسرع_90.png", "answer": "حيوان"},
            {"image": "اسرع_91.png", "answer": "طائر"},
            {"image": "اسرع_92.png", "answer": "سمك"},
            {"image": "اسرع_93.png", "answer": "حصان"},
            {"image": "اسرع_94.png", "answer": "قطة"},
            {"image": "اسرع_95.png", "answer": "كلب"},
            {"image": "اسرع_96.png", "answer": "أسد"},
            {"image": "اسرع_97.png", "answer": "نمر"},
            {"image": "اسرع_98.png", "answer": "فيل"},
            {"image": "اسرع_99.png", "answer": "قرد"},
            {"image": "اسرع_100.png", "answer": "عصفور"}
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

    @commands.command(name="اسرع")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "اسرع":
            await self.run_game(message.channel)

    async def run_game(self, channel):
        if self.lock:
            return await channel.send("اللعبة جارية بالفعل!")

        q = random.choice(self.questions)
        self.lock = True
        await channel.send(q["image"])

        def check(m):
            return m.channel == channel and not m.author.bot

        try:
            while True:  # حلقة تكرار للسماح بمحاولات متعددة
                msg = await self.bot.wait_for("message", check=check, timeout=30.0)

                if msg.content.strip() == q["answer"]:
                    # تحديث النقاط
                    user_id = str(msg.author.id)
                    self.scores[user_id] = self.scores.get(user_id, 0) + 1
                    self.save_scores()

                    # إنشاء الإيمبد
                    embed = discord.Embed(
                        title="🎉!",
                        description=f"مبروك {msg.author.mention}، لقد فزت في اللعبة!",
                        color=discord.Color.red(),
                    )

                    # إضافة الزر (يحتوي على النقاط)
                    view = discord.ui.View()
                    button = discord.ui.Button(
                        label=f"نقاطك: {self.scores[user_id]}",
                        style=discord.ButtonStyle.primary,
                        disabled=True,
                    )
                    view.add_item(button)

                    await channel.send(embed=embed, view=view)
                    break  # خروج من اللعبة بعد الفوز
                else:
                    await msg.add_reaction("❌")  # تفاعل إكس على الإجابة الخاطئة

        except asyncio.TimeoutError:
            await channel.send("⌛ انتهى الوقت! لم يقم أحد بالإجابة الصحيحة.")

        self.lock = False


async def setup(bot):
    await bot.add_cog(fastgame(bot))
