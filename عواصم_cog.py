import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class aasgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "عواصم_1.png", "answer": "الرياض"},
            {"image": "عواصم_2.png", "answer": "القاهرة"},
            {"image": "عواصم_3.png", "answer": "أبوظبي"},
            {"image": "عواصم_4.png", "answer": "الكويت"},
            {"image": "عواصم_5.png", "answer": "المنامة"},
            {"image": "عواصم_6.png", "answer": "الدوحة"},
            {"image": "عواصم_7.png", "answer": "مسقط"},
            {"image": "عواصم_8.png", "answer": "صنعاء"},
            {"image": "عواصم_9.png", "answer": "عمان"},
            {"image": "عواصم_10.png", "answer": "بغداد"},
            {"image": "عواصم_11.png", "answer": "دمشق"},
            {"image": "عواصم_12.png", "answer": "بيروت"},
            {"image": "عواصم_13.png", "answer": "القدس"},
            {"image": "عواصم_14.png", "answer": "الخرطوم"},
            {"image": "عواصم_15.png", "answer": "طرابلس"},
            {"image": "عواصم_16.png", "answer": "تونس"},
            {"image": "عواصم_17.png", "answer": "الجزائر"},
            {"image": "عواصم_18.png", "answer": "الرباط"},
            {"image": "عواصم_19.png", "answer": "نواكشوط"},
            {"image": "عواصم_20.png", "answer": "مقديشو"},
            {"image": "عواصم_21.png", "answer": "جيبوتي"},
            {"image": "عواصم_22.png", "answer": "موروني"},
            {"image": "عواصم_23.png", "answer": "أنقرة"},
            {"image": "عواصم_24.png", "answer": "طهران"},
            {"image": "عواصم_25.png", "answer": "إسلام آباد"},
            {"image": "عواصم_26.png", "answer": "كابول"},
            {"image": "عواصم_27.png", "answer": "نيودلهي"},
            {"image": "عواصم_28.png", "answer": "بكين"},
            {"image": "عواصم_29.png", "answer": "طوكيو"},
            {"image": "عواصم_30.png", "answer": "سول"},
            {"image": "عواصم_31.png", "answer": "بيونغ يانغ"},
            {"image": "عواصم_32.png", "answer": "جاكرتا"},
            {"image": "عواصم_33.png", "answer": "كوالالمبور"},
            {"image": "عواصم_34.png", "answer": "سنغافورة"},
            {"image": "عواصم_35.png", "answer": "بانكوك"},
            {"image": "عواصم_36.png", "answer": "هانوي"},
            {"image": "عواصم_37.png", "answer": "موسكو"},
            {"image": "عواصم_38.png", "answer": "برلين"},
            {"image": "عواصم_39.png", "answer": "باريس"},
            {"image": "عواصم_40.png", "answer": "لندن"},
            {"image": "عواصم_41.png", "answer": "روما"},
            {"image": "عواصم_42.png", "answer": "مدريد"},
            {"image": "عواصم_43.png", "answer": "لشبونة"},
            {"image": "عواصم_44.png", "answer": "أثينا"},
            {"image": "عواصم_45.png", "answer": "بيرن"},
            {"image": "عواصم_46.png", "answer": "فيينا"},
            {"image": "عواصم_47.png", "answer": "أمستردام"},
            {"image": "عواصم_48.png", "answer": "بروكسل"},
            {"image": "عواصم_49.png", "answer": "ستوكهولم"},
            {"image": "عواصم_50.png", "answer": "أوسلو"},
            {"image": "عواصم_51.png", "answer": "كوبنهاغن"},
            {"image": "عواصم_52.png", "answer": "دبلن"},
            {"image": "عواصم_53.png", "answer": "وارسو"},
            {"image": "عواصم_54.png", "answer": "بودابست"},
            {"image": "عواصم_55.png", "answer": "براغ"},
            {"image": "عواصم_56.png", "answer": "كييف"},
            {"image": "عواصم_57.png", "answer": "واشنطن"},
            {"image": "عواصم_58.png", "answer": "أوتاوا"},
            {"image": "عواصم_59.png", "answer": "مكسيكو"},
            {"image": "عواصم_60.png", "answer": "برازيليا"},
            {"image": "عواصم_61.png", "answer": "بوينس آيرس"},
            {"image": "عواصم_62.png", "answer": "سانتياغو"},
            {"image": "عواصم_63.png", "answer": "بوغوتا"},
            {"image": "عواصم_64.png", "answer": "كانبرا"},
            {"image": "عواصم_65.png", "answer": "ويلينغتون"},
            {"image": "عواصم_66.png", "answer": "بريتوريا"},
            {"image": "عواصم_67.png", "answer": "أبوجا"},
            {"image": "عواصم_68.png", "answer": "نيروبي"},
            {"image": "عواصم_69.png", "answer": "أديس أبابا"},
            {"image": "عواصم_70.png", "answer": "أكرا"},
            {"image": "عواصم_71.png", "answer": "داكار"},
            {"image": "عواصم_72.png", "answer": "كمبالا"},
            {"image": "عواصم_73.png", "answer": "دودوما"},
            {"image": "عواصم_74.png", "answer": "كيغالي"},
            {"image": "عواصم_75.png", "answer": "زغرب"},
            {"image": "عواصم_76.png", "answer": "بوخارست"},
            {"image": "عواصم_77.png", "answer": "صوفيا"},
            {"image": "عواصم_78.png", "answer": "بلغراد"},
            {"image": "عواصم_79.png", "answer": "هلسنكي"},
            {"image": "عواصم_80.png", "answer": "أستانا"}
           
            
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

    @commands.command(name="عواصم")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "عواصم":
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
    await bot.add_cog(aasgame(bot))