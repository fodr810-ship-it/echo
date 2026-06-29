import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class alamgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "flag_1.png", "answer": "السعودية"},
            {"image": "flag_2.png", "answer": "الإمارات"},
            {"image": "flag_3.png", "answer": "قطر"},
            {"image": "flag_4.png", "answer": "الكويت"},
            {"image": "flag_5.png", "answer": "عمان"},
            {"image": "flag_6.png", "answer": "البحرين"},
            {"image": "flag_7.png", "answer": "مصر"},
            {"image": "flag_8.png", "answer": "العراق"},
            {"image": "flag_9.png", "answer": "سوريا"},
            {"image": "flag_10.png", "answer": "لبنان"},
            {"image": "flag_11.png", "answer": "الأردن"},
            {"image": "flag_12.png", "answer": "فلسطين"},
            {"image": "flag_13.png", "answer": "اليمن"},
            {"image": "flag_14.png", "answer": "ليبيا"},
            {"image": "flag_15.png", "answer": "تونس"},
            {"image": "flag_16.png", "answer": "الجزائر"},
            {"image": "flag_17.png", "answer": "المغرب"},
            {"image": "flag_18.png", "answer": "السودان"},
            {"image": "flag_19.png", "answer": "الصومال"},
            {"image": "flag_20.png", "answer": "موريتانيا"},
            {"image": "flag_21.png", "answer": "اليابان"},
            {"image": "flag_22.png", "answer": "كوريا الجنوبية"},
            {"image": "flag_23.png", "answer": "الصين"},
            {"image": "flag_24.png", "answer": "الهند"},
            {"image": "flag_25.png", "answer": "إندونيسيا"},
            {"image": "flag_26.png", "answer": "ماليزيا"},
            {"image": "flag_27.png", "answer": "تركيا"},
            {"image": "flag_28.png", "answer": "بريطانيا"},
            {"image": "flag_29.png", "answer": "فرنسا"},
            {"image": "flag_30.png", "answer": "ألمانيا"},
            {"image": "flag_31.png", "answer": "إيطاليا"},
            {"image": "flag_32.png", "answer": "إسبانيا"},
            {"image": "flag_33.png", "answer": "البرتغال"},
            {"image": "flag_34.png", "answer": "هولندا"},
            {"image": "flag_35.png", "answer": "سويسرا"},
            {"image": "flag_36.png", "answer": "روسيا"},
            {"image": "flag_37.png", "answer": "السويد"},
            {"image": "flag_38.png", "answer": "اليونان"},
            {"image": "flag_39.png", "answer": "أمريكا"},
            {"image": "flag_40.png", "answer": "كندا"},
            {"image": "flag_41.png", "answer": "المكسيك"},
            {"image": "flag_42.png", "answer": "البرازيل"},
            {"image": "flag_43.png", "answer": "الأرجنتين"},
            {"image": "flag_44.png", "answer": "تشيلي"},
            {"image": "flag_45.png", "answer": "كولومبيا"},
            {"image": "flag_46.png", "answer": "أستراليا"},
            {"image": "flag_47.png", "answer": "نيوزيلندا"},
            {"image": "flag_48.png", "answer": "جنوب أفريقيا"},
            {"image": "flag_49.png", "answer": "كينيا"},
            {"image": "flag_50.png", "answer": "المالديف"}
            
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

    @commands.command(name="اعلام")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "اعلام":
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
    await bot.add_cog(alamgame(bot))