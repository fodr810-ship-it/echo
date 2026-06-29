import discord
from discord.ext import commands
import random
import asyncio
import json
import os

class asabgame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # اسم ملف النقاط الموحد (تقدر تستخدم هذا الاسم في كل ألعابك القادمة)
        self.scores_file = "global_points.json" 
        self.active_channels = set() # قفل اللعبة لكل روم بشكل منفصل لمنع التداخل
        self.questions = [
            {"image": "مجموع_1.png", "answer": "467"},
            {"image": "مجموع_2.png", "answer": "365"},
            {"image": "مجموع_3.png", "answer": "540"},
            {"image": "مجموع_4.png", "answer": "240"},
            {"image": "مجموع_5.png", "answer": "461"},
            {"image": "مجموع_6.png", "answer": "330"},
            {"image": "مجموع_7.png", "answer": "550"},
            {"image": "مجموع_8.png", "answer": "105"},
            {"image": "مجموع_9.png", "answer": "815"},
            {"image": "مجموع_10.png", "answer": "444"},
            {"image": "مجموع_11.png", "answer": "252"},
            {"image": "مجموع_12.png", "answer": "250"},
            {"image": "مجموع_13.png", "answer": "730"},
            {"image": "مجموع_14.png", "answer": "370"},
            {"image": "مجموع_15.png", "answer": "495"},
            {"image": "مجموع_16.png", "answer": "120"},
            {"image": "مجموع_17.png", "answer": "400"},
            {"image": "مجموع_18.png", "answer": "320"},
            {"image": "مجموع_19.png", "answer": "264"},
            {"image": "مجموع_20.png", "answer": "180"},
            {"image": "مجموع_21.png", "answer": "600"},
            {"image": "مجموع_22.png", "answer": "650"},
            {"image": "مجموع_23.png", "answer": "208"},
            {"image": "مجموع_24.png", "answer": "100"},
            {"image": "مجموع_25.png", "answer": "710"},
            {"image": "مجموع_26.png", "answer": "360"},
            {"image": "مجموع_27.png", "answer": "483"},
            {"image": "مجموع_28.png", "answer": "250"},
            {"image": "مجموع_29.png", "answer": "500"},
            {"image": "مجموع_30.png", "answer": "150"},
            {"image": "مجموع_31.png", "answer": "384"},
            {"image": "مجموع_32.png", "answer": "90"},
            {"image": "مجموع_33.png", "answer": "800"},
            {"image": "مجموع_34.png", "answer": "780"},
            {"image": "مجموع_35.png", "answer": "266"},
            {"image": "مجموع_36.png", "answer": "60"},
            {"image": "مجموع_37.png", "answer": "1000"},
            {"image": "مجموع_38.png", "answer": "410"},
            {"image": "مجموع_39.png", "answer": "390"},
            {"image": "مجموع_40.png", "answer": "320"},
            {"image": "مجموع_41.png", "answer": "1000"},
            {"image": "مجموع_42.png", "answer": "310"},
            {"image": "مجموع_43.png", "answer": "385"},
            {"image": "مجموع_44.png", "answer": "110"},
            {"image": "مجموع_45.png", "answer": "600"},
            {"image": "مجموع_46.png", "answer": "440"},
            {"image": "مجموع_47.png", "answer": "374"},
            {"image": "مجموع_48.png", "answer": "90"},
            {"image": "مجموع_49.png", "answer": "600"},
            {"image": "مجموع_50.png", "answer": "270"},
            {"image": "مجموع_51.png", "answer": "377"},
            {"image": "مجموع_52.png", "answer": "110"},
            {"image": "مجموع_53.png", "answer": "1000"},
            {"image": "مجموع_54.png", "answer": "680"},
            {"image": "مجموع_55.png", "answer": "408"},
            {"image": "مجموع_56.png", "answer": "220"},
            {"image": "مجموع_57.png", "answer": "1000"},
            {"image": "مجموع_58.png", "answer": "320"},
            {"image": "مجموع_59.png", "answer": "504"},
            {"image": "مجموع_60.png", "answer": "90"},
            {"image": "مجموع_61.png", "answer": "800"},
            {"image": "مجموع_62.png", "answer": "540"},
            {"image": "مجموع_63.png", "answer": "392"},
            {"image": "مجموع_64.png", "answer": "110"},
            {"image": "مجموع_65.png", "answer": "1000"},
            {"image": "مجموع_66.png", "answer": "320"},
            {"image": "مجموع_67.png", "answer": "540"},
            {"image": "مجموع_68.png", "answer": "110"},
            {"image": "مجموع_69.png", "answer": "700"},
            {"image": "مجموع_70.png", "answer": "420"},
            {"image": "مجموع_71.png", "answer": "399"},
            {"image": "مجموع_72.png", "answer": "210"},
            {"image": "مجموع_73.png", "answer": "1000"},
            {"image": "مجموع_74.png", "answer": "490"},
            {"image": "مجموع_75.png", "answer": "675"},
            {"image": "مجموع_76.png", "answer": "80"},
            {"image": "مجموع_77.png", "answer": "1000"},
            {"image": "مجموع_78.png", "answer": "590"},
            {"image": "مجموع_79.png", "answer": "486"},
            {"image": "مجموع_80.png", "answer": "190"}
        ]

    # دالة لقراءة النقاط وتحديثها مباشرة وقت الفوز لضمان عدم التعارض مع الألعاب الأخرى
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

    @commands.command(name="حساب")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "حساب":
            await self.run_game(message.channel)

    async def run_game(self, channel):
        # التحقق إذا كانت اللعبة تعمل في هذا الروم تحديداً
        if channel.id in self.active_channels:
            return await channel.send("⚠️ اللعبة جارية بالفعل في هذا الروم!")

        q = random.choice(self.questions)
        self.active_channels.add(channel.id) # إضافة الروم لقائمة الرومات النشطة
        
        # 📂 تحديد مسار المجلد الذي يحتوي على الصور
        image_path = os.path.join("images", q["image"])

        # ⚙️ التحقق من أن ملف الصورة موجود فعلياً
        if os.path.exists(image_path):
            file = discord.File(image_path, filename=q["image"])
            await channel.send(file=file)
        else:
            await channel.send(f"⚠️ خطأ: لم يتم العثور على ملف الصورة في المسار: `{image_path}`")
            self.active_channels.remove(channel.id)
            return

        def check(m):
            return m.channel == channel and not m.author.bot

        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=30.0)

                # إذا الإجابة صحيحة
                if msg.content.strip() == q["answer"]:
                    # تحديث وحفظ النقاط في الملف الموحد
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
                
                # إذا الإجابة خاطئة (بشرط أن تكون الرسالة أرقام لتجنب تخريب سوالف الشات أو الألعاب الأخرى)
                elif msg.content.strip().isdigit():
                    await msg.add_reaction("❌") 

        except asyncio.TimeoutError:
            await channel.send("⌛ انتهى الوقت! لم يقم أحد بالإجابة الصحيحة.")

        finally:
            # إلغاء القفل عن الروم بعد انتهاء اللعبة أو انتهاء الوقت
            if channel.id in self.active_channels:
                self.active_channels.remove(channel.id)

async def setup(bot):
    await bot.add_cog(asabgame(bot))