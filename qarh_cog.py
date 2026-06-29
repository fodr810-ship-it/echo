import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class qarhgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "قارة_1.png", "answer": "اسيا"},
            {"image": "قارة_2.png", "answer": "اسيا"},
            {"image": "قارة_3.png", "answer": "اسيا"},
            {"image": "قارة_4.png", "answer": "اسيا"},
            {"image": "قارة_5.png", "answer": "اسيا"},
            {"image": "قارة_6.png", "answer": "اسيا"},
            {"image": "قارة_7.png", "answer": "اسيا"},
            {"image": "قارة_8.png", "answer": "اسيا"},
            {"image": "قارة_9.png", "answer": "اسيا"},
            {"image": "قارة_10.png", "answer": "اسيا"},
            {"image": "قارة_11.png", "answer": "اسيا"},
            {"image": "قارة_12.png", "answer": "افريقيا"},
            {"image": "قارة_13.png", "answer": "افريقيا"},
            {"image": "قارة_14.png", "answer": "افريقيا"},
            {"image": "قارة_15.png", "answer": "افريقيا"},
            {"image": "قارة_16.png", "answer": "افريقيا"},
            {"image": "قارة_17.png", "answer": "افريقيا"},
            {"image": "قارة_18.png", "answer": "افريقيا"},
            {"image": "قارة_19.png", "answer": "افريقيا"},
            {"image": "قارة_20.png", "answer": "افريقيا"},
            {"image": "قارة_21.png", "answer": "اسيا"},
            {"image": "قارة_22.png", "answer": "اسيا"},
            {"image": "قارة_23.png", "answer": "اسيا"},
            {"image": "قارة_24.png", "answer": "اسيا"},
            {"image": "قارة_25.png", "answer": "اسيا"},
            {"image": "قارة_26.png", "answer": "اسيا"},
            {"image": "قارة_27.png", "answer": "اسيا/اوروبا"},
            {"image": "قارة_28.png", "answer": "اسيا"},
            {"image": "قارة_29.png", "answer": "اسيا"},
            {"image": "قارة_30.png", "answer": "اسيا"},
            {"image": "قارة_31.png", "answer": "اسيا"},
            {"image": "قارة_32.png", "answer": "اسيا"},
            {"image": "قارة_33.png", "answer": "اسيا"},
            {"image": "قارة_34.png", "answer": "اسيا"},
            {"image": "قارة_35.png", "answer": "اسيا"},
            {"image": "قارة_36.png", "answer": "اوروبا"},
            {"image": "قارة_37.png", "answer": "اوروبا"},
            {"image": "قارة_38.png", "answer": "اوروبا"},
            {"image": "قارة_39.png", "answer": "اوروبا"},
            {"image": "قارة_40.png", "answer": "اوروبا"},
            {"image": "قارة_41.png", "answer": "اوروبا"},
            {"image": "قارة_42.png", "answer": "اوروبا"},
            {"image": "قارة_43.png", "answer": "اوروبا"},
            {"image": "قارة_44.png", "answer": "اوروبا"},
            {"image": "قارة_45.png", "answer": "اوروبا"},
            {"image": "قارة_46.png", "answer": "اوروبا"},
            {"image": "قارة_47.png", "answer": "اسيا/اوروبا"},
            {"image": "قارة_48.png", "answer": "اوروبا"},
            {"image": "قارة_49.png", "answer": "اوروبا"},
            {"image": "قارة_50.png", "answer": "اوروبا"},
            {"image": "قارة_51.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_52.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_53.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_54.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_55.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_56.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_57.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_58.png", "answer": "اوقيانوسيا"},
            {"image": "قارة_59.png", "answer": "اوقيانوسيا"},
            {"image": "قارة_60.png", "answer": "افريقيا"}
            
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

    @commands.command(name="قارة")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "قارة":
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
    await bot.add_cog(qarhgame(bot))