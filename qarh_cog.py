import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class qarhgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "qarh_scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "قارة_1.png", "country": "السعودية", "continent": "آسيا"},
            {"image": "قارة_2.png", "country": "الإمارات", "continent": "آسيا"},
            {"image": "قارة_3.png", "country": "قطر", "continent": "آسيا"},
            {"image": "قارة_4.png", "country": "الكويت", "continent": "آسيا"},
            {"image": "قارة_5.png", "country": "عمان", "continent": "آسيا"},
            {"image": "قارة_6.png", "country": "البحرين", "continent": "آسيا"},
            {"image": "قارة_7.png", "country": "العراق", "continent": "آسيا"},
            {"image": "قارة_8.png", "country": "الأردن", "continent": "آسيا"},
            {"image": "قارة_9.png", "country": "فلسطين", "continent": "آسيا"},
            {"image": "قارة_10.png", "country": "لبنان", "continent": "آسيا"},
            {"image": "قارة_11.png", "country": "سوريا", "continent": "آسيا"},
            {"image": "قارة_12.png", "country": "مصر", "continent": "أفريقيا"},
            {"image": "قارة_13.png", "country": "السودان", "continent": "أفريقيا"},
            {"image": "قارة_14.png", "country": "ليبيا", "continent": "أفريقيا"},
            {"image": "قارة_15.png", "country": "تونس", "continent": "أفريقيا"},
            {"image": "قارة_16.png", "country": "الجزائر", "continent": "أفريقيا"},
            {"image": "قارة_17.png", "country": "المغرب", "continent": "أفريقيا"},
            {"image": "قارة_18.png", "country": "موريتانيا", "continent": "أفريقيا"},
            {"image": "قارة_19.png", "country": "الصومال", "continent": "أفريقيا"},
            {"image": "قارة_20.png", "country": "جيبوتي", "continent": "أفريقيا"},
            {"image": "قارة_21.png", "country": "اليابان", "continent": "آسيا"},
            {"image": "قارة_22.png", "country": "كوريا الجنوبية", "continent": "آسيا"},
            {"image": "قارة_23.png", "country": "الصين", "continent": "آسيا"},
            {"image": "قارة_24.png", "country": "الهند", "continent": "آسيا"},
            {"image": "قارة_25.png", "country": "إندونيسيا", "continent": "آسيا"},
            {"image": "قارة_26.png", "country": "ماليزيا", "continent": "آسيا"},
            {"image": "قارة_27.png", "country": "تركيا", "continent": "آسيا/أوروبا"},
            {"image": "قارة_28.png", "country": "إيران", "continent": "آسيا"},
            {"image": "قارة_29.png", "country": "باكستان", "continent": "آسيا"},
            {"image": "قارة_30.png", "country": "الفلبين", "continent": "آسيا"},
            {"image": "قارة_31.png", "country": "فيتنام", "continent": "آسيا"},
            {"image": "قارة_32.png", "country": "تايلاند", "continent": "آسيا"},
            {"image": "قارة_33.png", "country": "سنغافورة", "continent": "آسيا"},
            {"image": "قارة_34.png", "country": "كازاخستان", "continent": "آسيا"},
            {"image": "قارة_35.png", "country": "أوزبكستان", "continent": "آسيا"},
            {"image": "قارة_36.png", "country": "فرنسا", "continent": "أوروبا"},
            {"image": "قارة_37.png", "country": "ألمانيا", "continent": "أوروبا"},
            {"image": "قارة_38.png", "country": "إيطاليا", "continent": "أوروبا"},
            {"image": "قارة_39.png", "country": "بريطانيا", "continent": "أوروبا"},
            {"image": "قارة_40.png", "country": "إسبانيا", "continent": "أوروبا"},
            {"image": "قارة_41.png", "country": "البرتغال", "continent": "أوروبا"},
            {"image": "قارة_42.png", "country": "هولندا", "continent": "أوروبا"},
            {"image": "قارة_43.png", "country": "سويسرا", "continent": "أوروبا"},
            {"image": "قارة_44.png", "country": "السويد", "continent": "أوروبا"},
            {"image": "قارة_45.png", "country": "النرويج", "continent": "أوروبا"},
            {"image": "قارة_46.png", "country": "اليونان", "continent": "أوروبا"},
            {"image": "قارة_47.png", "country": "روسيا", "continent": "آسيا/أوروبا"},
            {"image": "قارة_48.png", "country": "بلجيكا", "continent": "أوروبا"},
            {"image": "قارة_49.png", "country": "النمسا", "continent": "أوروبا"},
            {"image": "قارة_50.png", "country": "الدنمارك", "continent": "أوروبا"},
            {"image": "قارة_51.png", "country": "أمريكا", "continent": "أمريكا الشمالية"},
            {"image": "قارة_52.png", "country": "كندا", "continent": "أمريكا الشمالية"},
            {"image": "قارة_53.png", "country": "المكسيك", "continent": "أمريكا الشمالية"},
            {"image": "قارة_54.png", "country": "البرازيل", "continent": "أمريكا الجنوبية"},
            {"image": "قارة_55.png", "country": "الأرجنتين", "continent": "أمريكا الجنوبية"},
            {"image": "قارة_56.png", "country": "تشيلي", "continent": "أمريكا الجنوبية"},
            {"image": "قارة_57.png", "country": "كولومبيا", "continent": "أمريكا الجنوبية"},
            {"image": "قارة_58.png", "country": "أستراليا", "continent": "أوقيانوسيا"},
            {"image": "قارة_59.png", "country": "نيوزيلندا", "continent": "أوقيانوسيا"},
            {"image": "قارة_60.png", "country": "جنوب أفريقيا", "continent": "أفريقيا"}
            
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
    await bot.add_cog(qarhgame(bot))