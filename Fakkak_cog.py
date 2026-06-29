import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class fkkgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "فكك_1.png", "answer": "ب ر م ج ة"},
            {"image": "فكك_2.png", "answer": "خ ا د م"},
            {"image": "فكك_3.png", "answer": "ح م ا ي ة"},
            {"image": "فكك_4.png", "answer": "ت ش ف ي ر"},
            {"image": "فكك_5.png", "answer": "ش ب ك ة"},
            {"image": "فكك_6.png", "answer": "ش ا ش ة"},
            {"image": "فكك_7.png", "answer": "ل و ح ة"},
            {"image": "فكك_8.png", "answer": "ع د س ة"},
            {"image": "فكك_9.png", "answer": "ك ا م ي ر ا"},
            {"image": "فكك_10.png", "answer": "ت ص و ي ر"},
            {"image": "فكك_11.png", "answer": "م و ن ت ا ج"},
            {"image": "فكك_12.png", "answer": "ت ص م ي م"},
            {"image": "فكك_13.png", "answer": "ت ر ا ث"},
            {"image": "فكك_14.png", "answer": "آ ث ا ر"},
            {"image": "فكك_15.png", "answer": "ق ر ي ة"},
            {"image": "فكك_16.png", "answer": "م ت ح ف"},
            {"image": "فكك_17.png", "answer": "ت ا ر ي خ"},
            {"image": "فكك_18.png", "answer": "ن ق و ش"},
            {"image": "فكك_19.png", "answer": "ج ب ل"},
            {"image": "فكك_20.png", "answer": "و ا د ي"},
            {"image": "فكك_21.png", "answer": "أ س ط و ر ة"},
            {"image": "فكك_22.png", "answer": "م غ ا م ر ة"},
            {"image": "فكك_23.png", "answer": "ت ح د ي"},
            {"image": "فكك_24.png", "answer": "م س ا ب ق ة"},
            {"image": "فكك_25.png", "answer": "ج ا ئ ز ة"},
            {"image": "فكك_26.png", "answer": "ت ف ا ع ل"},
            {"image": "فكك_27.png", "answer": "م ج ت م ع"},
            {"image": "فكك_28.png", "answer": "ق و ا ن ي ن"},
            {"image": "فكك_29.png", "answer": "ص ل ا ح ي ا ت"},
            {"image": "فكك_30.png", "answer": "إ د ا ر ة"},
            {"image": "فكك_31.png", "answer": "ت و ث ي ق"},
            {"image": "فكك_32.png", "answer": "ر و ل ي ت"},
            {"image": "فكك_33.png", "answer": "ا خ ت ر ا ق"},
            {"image": "فكك_34.png", "answer": "ف ح ص"},
            {"image": "فكك_35.png", "answer": "ن ظ ا م"},
            {"image": "فكك_36.png", "answer": "خ و ا ر ز م ي ة"},
            {"image": "فكك_37.png", "answer": "ا س ت و د ي و"},
            {"image": "فكك_38.png", "answer": "إ ض ا ء ة"},
            {"image": "فكك_39.png", "answer": "ه ن د س ة"},
            {"image": "فكك_40.png", "answer": "ت ك ن و ل و ج ي ا"},
            {"image": "فكك_41.png", "answer": "ا ب ت ك ا ر"},
            {"image": "فكك_42.png", "answer": "ذ ك ا ء"},
            {"image": "فكك_43.png", "answer": "ا ص ط ن ا ع ي"},
            {"image": "فكك_44.png", "answer": "ب ي ا ن ا ت"},
            {"image": "فكك_45.png", "answer": "ت ح ل ي ل"},
            {"image": "فكك_46.png", "answer": "إ ح ص ا ء"},
            {"image": "فكك_47.png", "answer": "ر س و م ا ت"},
            {"image": "فكك_48.png", "answer": "و ا ج ه ة"},
            {"image": "فكك_49.png", "answer": "ت ط ب ي ق"},
            {"image": "فكك_50.png", "answer": "ت ط و ي ر"},
            {"image": "فكك_51.png", "answer": "م ح ت و ى"},
            {"image": "فكك_52.png", "answer": "إ ب د ا ع"},
            {"image": "فكك_53.png", "answer": "ا ح ت ر ا ف"},
            {"image": "فكك_54.png", "answer": "م ه ا ر ة"},
            {"image": "فكك_55.png", "answer": "م و ه ب ة"},
            {"image": "فكك_56.png", "answer": "ط م و ح"},
            {"image": "فكك_57.png", "answer": "ن ج ا ح"},
            {"image": "فكك_58.png", "answer": "إ ن ج ا ز"},
            {"image": "فكك_59.png", "answer": "ه د ف"},
            {"image": "فكك_60.png", "answer": "ت خ ط ي ط"},
            {"image": "فكك_61.png", "answer": "ا س ت ر ا ت ي ج ي ة"},
            {"image": "فكك_62.png", "answer": "ت ك ت ي ك"},
            {"image": "فكك_63.png", "answer": "ف ر ي ق"},
            {"image": "فكك_64.png", "answer": "ت ع ا و ن"},
            {"image": "فكك_65.png", "answer": "ا ت ص ا ل"},
            {"image": "فكك_66.png", "answer": "ت و ا ص ل"},
            {"image": "فكك_67.png", "answer": "ر س ا ل ة"},
            {"image": "فكك_68.png", "answer": "إ ش ع ا ر"},
            {"image": "فكك_69.png", "answer": "ت ن ب ي ه"},
            {"image": "فكك_70.png", "answer": "د ع و ة"},
            {"image": "فكك_71.png", "answer": "ت ر ح ي ب"},
            {"image": "فكك_72.png", "answer": "ض ي ا ف ة"},
            {"image": "فكك_73.png", "answer": "ا ح ت ف ا ل"},
            {"image": "فكك_74.png", "answer": "م ه ر ج ا ن"},
            {"image": "فكك_75.png", "answer": "ف ع ا ل ي ة"},
            {"image": "فكك_76.png", "answer": "ن ش ا ط"},
            {"image": "فكك_77.png", "answer": "ر ي ا ض ة"},
            {"image": "فكك_78.png", "answer": "ل ي ا ق ة"},
            {"image": "فكك_79.png", "answer": "ص ح ة"},
            {"image": "فكك_80.png", "answer": "م ن ا ع ة"},
            {"image": "فكك_81.png", "answer": "ع ل ا ج"},
            {"image": "فكك_82.png", "answer": "ط ب ي ع ة"},
            {"image": "فكك_83.png", "answer": "ب ي ئ ة"},
            {"image": "فكك_84.png", "answer": "م ن ا خ"},
            {"image": "فكك_85.png", "answer": "ط ق س"},
            {"image": "فكك_86.png", "answer": "ع ا ص ف ة"},
            {"image": "فكك_87.png", "answer": "إ ع ص ا ر"},
            {"image": "فكك_88.png", "answer": "ز ل ز ا ل"},
            {"image": "فكك_89.png", "answer": "ب ر ك ا ن"},
            {"image": "فكك_90.png", "answer": "م ح ي ط"},
            {"image": "فكك_91.png", "answer": "ج ز ي ر ة"},
            {"image": "فكك_92.png", "answer": "ق ا ر ة"},
            {"image": "فكك_93.png", "answer": "ك و ك ب"},
            {"image": "فكك_94.png", "answer": "ف ض ا ء"},
            {"image": "فكك_95.png", "answer": "م ج ر ة"},
            {"image": "فكك_96.png", "answer": "ج ا ذ ب ي ة"},
            {"image": "فكك_97.png", "answer": "م د ا ر"},
            {"image": "فكك_98.png", "answer": "ن ي ز ك"},
            {"image": "فكك_99.png", "answer": "ش ه ا ب"},
            {"image": "فكك_100.png", "answer": "س م ا ء"}
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

    @commands.command(name="فكك")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "فكك":
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
    await bot.add_cog(fkkgame(bot))