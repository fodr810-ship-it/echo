import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class fastgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

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
    await bot.add_cog(fastgame(bot))