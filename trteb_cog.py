import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class trrgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "ترتيب_1.png", "answer": "012459"},
            {"image": "ترتيب_2.png", "answer": "134789"},
            {"image": "ترتيب_3.png", "answer": "012479"},
            {"image": "ترتيب_4.png", "answer": "123568"},
            {"image": "ترتيب_5.png", "answer": "013589"},
            {"image": "ترتيب_6.png", "answer": "234789"},
            {"image": "ترتيب_7.png", "answer": "023589"},
            {"image": "ترتيب_8.png", "answer": "234789"},
            {"image": "ترتيب_9.png", "answer": "234789"},
            {"image": "ترتيب_10.png", "answer": "012478"},
            {"image": "ترتيب_11.png", "answer": "236789"},
            {"image": "ترتيب_12.png", "answer": "234789"},
            {"image": "ترتيب_13.png", "answer": "234678"},
            {"image": "ترتيب_14.png", "answer": "235789"},
            {"image": "ترتيب_15.png", "answer": "345678"},
            {"image": "ترتيب_16.png", "answer": "123789"},
            {"image": "ترتيب_17.png", "answer": "234789"},
            {"image": "ترتيب_18.png", "answer": "235678"},
            {"image": "ترتيب_19.png", "answer": "234789"},
            {"image": "ترتيب_20.png", "answer": "024578"},
            {"image": "ترتيب_21.png", "answer": "234678"},
            {"image": "ترتيب_22.png", "answer": "235789"},
            {"image": "ترتيب_23.png", "answer": "123789"},
            {"image": "ترتيب_24.png", "answer": "234678"},
            {"image": "ترتيب_25.png", "answer": "345678"},
            {"image": "ترتيب_26.png", "answer": "234789"},
            {"image": "ترتيب_27.png", "answer": "023589"},
            {"image": "ترتيب_28.png", "answer": "234789"},
            {"image": "ترتيب_29.png", "answer": "012489"},
            {"image": "ترتيب_30.png", "answer": "345678"},
            {"image": "ترتيب_31.png", "answer": "012479"},
            {"image": "ترتيب_32.png", "answer": "235789"},
            {"image": "ترتيب_33.png", "answer": "234789"},
            {"image": "ترتيب_34.png", "answer": "123568"},
            {"image": "ترتيب_35.png", "answer": "013589"},
            {"image": "ترتيب_36.png", "answer": "234789"},
            {"image": "ترتيب_37.png", "answer": "023589"},
            {"image": "ترتيب_38.png", "answer": "234789"},
            {"image": "ترتيب_39.png", "answer": "234789"},
            {"image": "ترتيب_40.png", "answer": "012478"},
            {"image": "ترتيب_41.png", "answer": "236789"},
            {"image": "ترتيب_42.png", "answer": "234789"},
            {"image": "ترتيب_43.png", "answer": "234678"},
            {"image": "ترتيب_44.png", "answer": "235789"},
            {"image": "ترتيب_45.png", "answer": "345678"},
            {"image": "ترتيب_46.png", "answer": "123789"},
            {"image": "ترتيب_47.png", "answer": "234789"},
            {"image": "ترتيب_48.png", "answer": "235678"},
            {"image": "ترتيب_49.png", "answer": "234789"},
            {"image": "ترتيب_50.png", "answer": "024578"},
            {"image": "ترتيب_51.png", "answer": "234678"},
            {"image": "ترتيب_52.png", "answer": "235789"},
            {"image": "ترتيب_53.png", "answer": "123789"},
            {"image": "ترتيب_54.png", "answer": "234678"},
            {"image": "ترتيب_55.png", "answer": "345678"},
            {"image": "ترتيب_56.png", "answer": "234789"},
            {"image": "ترتيب_57.png", "answer": "023589"},
            {"image": "ترتيب_58.png", "answer": "234789"},
            {"image": "ترتيب_59.png", "answer": "012489"},
            {"image": "ترتيب_60.png", "answer": "345678"},
            {"image": "ترتيب_61.png", "answer": "012479"},
            {"image": "ترتيب_62.png", "answer": "235789"},
            {"image": "ترتيب_63.png", "answer": "234789"},
            {"image": "ترتيب_64.png", "answer": "123568"},
            {"image": "ترتيب_65.png", "answer": "013589"},
            {"image": "ترتيب_66.png", "answer": "234789"},
            {"image": "ترتيب_67.png", "answer": "023589"},
            {"image": "ترتيب_68.png", "answer": "234789"},
            {"image": "ترتيب_69.png", "answer": "234789"},
            {"image": "ترتيب_70.png", "answer": "012478"},
            {"image": "ترتيب_71.png", "answer": "236789"},
            {"image": "ترتيب_72.png", "answer": "234789"},
            {"image": "ترتيب_73.png", "answer": "234678"},
            {"image": "ترتيب_74.png", "answer": "235789"},
            {"image": "ترتيب_75.png", "answer": "345678"},
            {"image": "ترتيب_76.png", "answer": "123789"},
            {"image": "ترتيب_77.png", "answer": "234789"},
            {"image": "ترتيب_78.png", "answer": "235678"},
            {"image": "ترتيب_79.png", "answer": "234789"},
            {"image": "ترتيب_80.png", "answer": "024578"}
        
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

    @commands.command(name="ترتيب")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "ترتيب":
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
    await bot.add_cog(trrgame(bot))