import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class arqgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "arq_scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "ارقام_1.png", "answer": "10384"},
            {"image": "ارقام_2.png", "answer": "12694"},
            {"image": "ارقام_3.png", "answer": "12765"},
            {"image": "ارقام_4.png", "answer": "12845"},
            {"image": "ارقام_5.png", "answer": "15347"},
            {"image": "ارقام_6.png", "answer": "16845"},
            {"image": "ارقام_7.png", "answer": "19437"},
            {"image": "ارقام_8.png", "answer": "20394"},
            {"image": "ارقام_9.png", "answer": "21973"},
            {"image": "ارقام_10.png", "answer": "24816"},
            {"image": "ارقام_11.png", "answer": "26903"},
            {"image": "ارقام_12.png", "answer": "27156"},
            {"image": "ارقام_13.png", "answer": "27490"},
            {"image": "ارقام_14.png", "answer": "29578"},
            {"image": "ارقام_15.png", "answer": "30571"},
            {"image": "ارقام_16.png", "answer": "31960"},
            {"image": "ارقام_17.png", "answer": "32495"},
            {"image": "ارقام_18.png", "answer": "33567"},
            {"image": "ارقام_19.png", "answer": "38201"},
            {"image": "ارقام_20.png", "answer": "38490"},
            {"image": "ارقام_21.png", "answer": "39458"},
            {"image": "ارقام_22.png", "answer": "40156"},
            {"image": "ارقام_23.png", "answer": "40391"},
            {"image": "ارقام_24.png", "answer": "41903"},
            {"image": "ارقام_25.png", "answer": "44829"},
            {"image": "ارقام_26.png", "answer": "47562"},
            {"image": "ارقام_27.png", "answer": "48210"},
            {"image": "ارقام_28.png", "answer": "49265"},
            {"image": "ارقام_29.png", "answer": "50218"},
            {"image": "ارقام_30.png", "answer": "54609"},
            {"image": "ارقام_31.png", "answer": "55103"},
            {"image": "ارقام_32.png", "answer": "55936"},
            {"image": "ارقام_33.png", "answer": "57620"},
            {"image": "ارقام_34.png", "answer": "58274"},
            {"image": "ارقام_35.png", "answer": "59201"},
            {"image": "ارقام_36.png", "answer": "60812"},
            {"image": "ارقام_37.png", "answer": "62489"},
            {"image": "ارقام_38.png", "answer": "63715"},
            {"image": "ارقام_39.png", "answer": "65934"},
            {"image": "ارقام_40.png", "answer": "66721"},
            {"image": "ارقام_41.png", "answer": "67485"},
            {"image": "ارقام_42.png", "answer": "71548"},
            {"image": "ارقام_43.png", "answer": "73290"},
            {"image": "ارقام_44.png", "answer": "73842"},
            {"image": "ارقام_45.png", "answer": "74683"},
            {"image": "ارقام_46.png", "answer": "76532"},
            {"image": "ارقام_47.png", "answer": "78312"},
            {"image": "ارقام_48.png", "answer": "80472"},
            {"image": "ارقام_49.png", "answer": "81934"},
            {"image": "ارقام_50.png", "answer": "84629"},
            {"image": "ارقام_51.png", "answer": "85210"},
            {"image": "ارقام_52.png", "answer": "85671"},
            {"image": "ارقام_53.png", "answer": "88432"},
            {"image": "ارقام_54.png", "answer": "91572"},
            {"image": "ارقام_55.png", "answer": "92103"},
            {"image": "ارقام_56.png", "answer": "93021"},
            {"image": "ارقام_57.png", "answer": "93154"},
            {"image": "ارقام_58.png", "answer": "96347"},
            {"image": "ارقام_59.png", "answer": "97832"},
            {"image": "ارقام_60.png", "answer": "99043"},
           
            
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

    @commands.command(name="ارقام")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "ارقام":
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
    await bot.add_cog(arqgame(bot))