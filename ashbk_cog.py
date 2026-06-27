import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class ashbkgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "ashbk_scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "blob:null/05257285-df4e-425b-b432-fc43a99cbe71", "answer": "نجران"},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            {"image": "", "answer": ""},
            
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

    @commands.command(name="اسرع")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "اسرع":
            await self.run_game(message.channel)

    async def run_game(self, channel):
        if self.lock:
            return await channel.send("اللعبة جارية بالفعل!")

        q = random.choice(self.questions)
        self.lock = True
        await channel.send(q["image"])

        def check(m):
            return m.channel == channel and not m.author.bot

        try:
            while True:  # حلقة تكرار للسماح بمحاولات متعددة
                msg = await self.bot.wait_for("message", check=check, timeout=30.0)

                if msg.content.strip() == q["answer"]:
                    # تحديث النقاط
                    user_id = str(msg.author.id)
                    self.scores[user_id] = self.scores.get(user_id, 0) + 1
                    self.save_scores()

                    # إنشاء الإيمبد
                    embed = discord.Embed(
                        title="🎉!",
                        description=f"مبروك {msg.author.mention}، لقد فزت في اللعبة!",
                        color=discord.Color.red(),
                    )

                    # إضافة الزر (يحتوي على النقاط)
                    view = discord.ui.View()
                    button = discord.ui.Button(
                        label=f"نقاطك: {self.scores[user_id]}",
                        style=discord.ButtonStyle.primary,
                        disabled=True,
                    )
                    view.add_item(button)

                    await channel.send(embed=embed, view=view)
                    break  # خروج من اللعبة بعد الفوز
                else:
                    await msg.add_reaction("❌")  # تفاعل إكس على الإجابة الخاطئة

        except asyncio.TimeoutError:
            await channel.send("⌛ انتهى الوقت! لم يقم أحد بالإجابة الصحيحة.")

        self.lock = False


async def setup(bot):
    await bot.add_cog(ashbkgame(bot))
