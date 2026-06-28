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