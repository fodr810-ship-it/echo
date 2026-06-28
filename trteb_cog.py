import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class trrgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "trr_scores.json"
        self.scores = self.load_scores()
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
    await bot.add_cog(trrgame(bot))