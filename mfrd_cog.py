import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class mfrdgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
           {"image": "مفرد_1.png", "answer": "سيارة"},
            {"image": "مفرد_2.png", "answer": "قلم"},
            {"image": "مفرد_3.png", "answer": "كتاب"},
            {"image": "مفرد_4.png", "answer": "بيت"},
            {"image": "مفرد_5.png", "answer": "شجرة"},
            {"image": "مفرد_6.png", "answer": "جبل"},
            {"image": "مفرد_7.png", "answer": "مدرسة"},
            {"image": "مفرد_8.png", "answer": "هاتف"},
            {"image": "مفرد_9.png", "answer": "طاولة"},
            {"image": "مفرد_10.png", "answer": "نهر"},
            {"image": "مفرد_11.png", "answer": "باب"},
            {"image": "مفرد_12.png", "answer": "نافذة"},
            {"image": "مفرد_13.png", "answer": "حديقة"},
            {"image": "مفرد_14.png", "answer": "نجم"},
            {"image": "مفرد_15.png", "answer": "ملبس"},
            {"image": "مفرد_16.png", "answer": "حقيبة"},
            {"image": "مفرد_17.png", "answer": "كرسي"},
            {"image": "مفرد_18.png", "answer": "شارع"},
            {"image": "مفرد_19.png", "answer": "مصباح"},
            {"image": "مفرد_20.png", "answer": "سحابة"},
            {"image": "مفرد_21.png", "answer": "لعبة"},
            {"image": "مفرد_22.png", "answer": "صورة"},
            {"image": "مفرد_23.png", "answer": "طبق"},
            {"image": "مفرد_24.png", "answer": "فاكهة"},
            {"image": "مفرد_25.png", "answer": "خضار"},
            {"image": "مفرد_26.png", "answer": "عصفور"},
            {"image": "مفرد_27.png", "answer": "يوم"},
            {"image": "مفرد_28.png", "answer": "شهر"},
            {"image": "مفرد_29.png", "answer": "سنة"},
            {"image": "مفرد_30.png", "answer": "ساعة"},
            {"image": "مفرد_31.png", "answer": "دقيقة"},
            {"image": "مفرد_32.png", "answer": "قصة"},
            {"image": "مفرد_33.png", "answer": "رسالة"},
            {"image": "مفرد_34.png", "answer": "وجه"},
            {"image": "مفرد_35.png", "answer": "عين"},
            {"image": "مفرد_36.png", "answer": "قلب"},
            {"image": "مفرد_37.png", "answer": "يد"},
            {"image": "مفرد_38.png", "answer": "رجل"},
            {"image": "مفرد_39.png", "answer": "لون"},
            {"image": "مفرد_40.png", "answer": "بحر"},
            {"image": "مفرد_41.png", "answer": "خيل"},
            {"image": "مفرد_42.png", "answer": "قطة"},
            {"image": "مفرد_43.png", "answer": "كلب"},
            {"image": "مفرد_44.png", "answer": "أسد"},
            {"image": "مفرد_45.png", "answer": "نمر"},
            {"image": "مفرد_46.png", "answer": "طائرة"},
            {"image": "مفرد_47.png", "answer": "سفينة"},
            {"image": "مفرد_48.png", "answer": "قطار"},
            {"image": "مفرد_49.png", "answer": "دراجة"},
            {"image": "مفرد_50.png", "answer": "حاسوب"},
            {"image": "مفرد_51.png", "answer": "شاشة"},
            {"image": "مفرد_52.png", "answer": "مفتاح"},
            {"image": "مفرد_53.png", "answer": "حذاء"},
            {"image": "مفرد_54.png", "answer": "قميص"},
            {"image": "مفرد_55.png", "answer": "جورب"},
            {"image": "مفرد_56.png", "answer": "قبعة"},
            {"image": "مفرد_57.png", "answer": "نظارة"},
            {"image": "مفرد_58.png", "answer": "عطر"},
            {"image": "مفرد_59.png", "answer": "هدية"},
            {"image": "مفرد_60.png", "answer": "طعام"},
            {"image": "مفرد_61.png", "answer": "مشروب"},
            {"image": "مفرد_62.png", "answer": "ملعقة"},
            {"image": "مفرد_63.png", "answer": "سكين"},
            {"image": "مفرد_64.png", "answer": "وسادة"},
            {"image": "مفرد_65.png", "answer": "سرير"},
            {"image": "مفرد_66.png", "answer": "ستارة"},
            {"image": "مفرد_67.png", "answer": "سجادة"},
            {"image": "مفرد_68.png", "answer": "لوحة"},
            {"image": "مفرد_69.png", "answer": "برواز"},
            {"image": "مفرد_70.png", "answer": "ساعة"},
            {"image": "مفرد_71.png", "answer": "خاتم"},
            {"image": "مفرد_72.png", "answer": "قلادة"},
            {"image": "مفرد_73.png", "answer": "صندوق"},
            {"image": "مفرد_74.png", "answer": "حقيبة"},
            {"image": "مفرد_75.png", "answer": "ملف"},
            {"image": "مفرد_76.png", "answer": "ورقة"},
            {"image": "مفرد_77.png", "answer": "قرص"},
            {"image": "مفرد_78.png", "answer": "كاميرا"},
            {"image": "مفرد_79.png", "answer": "بطارية"},
            {"image": "مفرد_80.png", "answer": "شاحن"},
            
            
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

    @commands.command(name="مفرد")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "مفرد":
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
    await bot.add_cog(mfrdgame(bot))