import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class fkkgame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = "fkk_scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "https://files.catbox.moe/xdzrsq.png", "answer": "ب ر م ج ة"},
            {"image": "https://files.catbox.moe/l233us.png", "answer": "ب ر ت ق ا ل ي"},
            {"image": "https://files.catbox.moe/zpcpgn.png", "answer": "ن ه ر"},
            {"image": "https://files.catbox.moe/tqsjh4.png", "answer": "م ل ح"},
            {"image": "https://files.catbox.moe/d8stsz.png", "answer": "ق م ر"},
            {"image": "https://files.catbox.moe/4nmhhl.png", "answer": "ش م س"},
            {"image": "https://files.catbox.moe/y489tt.png", "answer": "ب ح ر"},
            {"image": "https://files.catbox.moe/njeu8f.png", "answer": "ج ب ل"},
            {"image": "https://files.catbox.moe/qomim5.png", "answer": "ك ت ب"},
            {"image": "https://files.catbox.moe/o9u699.png", "answer": "م ل ع ب"},
            {"image": "https://files.catbox.moe/aiv830.png", "answer": "م ه ن د"},
            {"image": "https://files.catbox.moe/lf8pij.png", "answer": "س ي ف"},
            {"image": "https://files.catbox.moe/300vnz.png", "answer": "ر ا ئ د"},
            {"image": "https://files.catbox.moe/046t7a.png", "answer": "م ر ا ي ة"},
            {"image": "https://files.catbox.moe/4wc9ld.png", "answer": "س ا ع ة"},
            {"image": "https://files.catbox.moe/fhpfh5.png", "answer": "ج ب ل"},
            {"image": "https://files.catbox.moe/4o7e24.png", "answer": "ز م ن"},
            {"image": "https://files.catbox.moe/hhoji1.png", "answer": "ت ف ا ح"},
            {"image": "https://files.catbox.moe/gy5ud0.png", "answer": "ح ق ي ب ة"},
            {"image": "https://files.catbox.moe/d3wp28.png", "answer": "ث ل ا ج ة"},
            {"image": "https://files.catbox.moe/vc0py4.png", "answer": "س ف ر"},
            {"image": "https://files.catbox.moe/nu0gc0.png", "answer": "ح ب ر"},
            {"image": "https://files.catbox.moe/k42m8q.png", "answer": "م ط ا ر"},
            {"image": "https://files.catbox.moe/wx0oxq.png", "answer": "ط ي ا ر ة"},
            {"image": "https://files.catbox.moe/wxbd4n.png", "answer": "ع ص ي ر"},
            {"image": "https://files.catbox.moe/9kw44a.png", "answer": "ط ا و ل ة"},
            {"image": "https://files.catbox.moe/s2y9c9.png", "answer": "ن ا ف ذ ة"},
            {"image": "https://files.catbox.moe/fxue4r.png", "answer": "ق ل م"},
            {"image": "https://files.catbox.moe/055h3q.png", "answer": "ا س ت ط ا ع ة"},
            {"image": "https://files.catbox.moe/v9t4il.png", "answer": "ث و ب"},
            {"image": "https://files.catbox.moe/outa09.png", "answer": "ص ر ا ع"},
            {"image": "https://files.catbox.moe/ea0o20.png", "answer": "س و ر"},
            {"image": "https://files.catbox.moe/51gasi.png", "answer": "ر ع د"},
            {"image": "https://files.catbox.moe/harvwy.png", "answer": "ب ر ق"},
            {"image": "https://files.catbox.moe/68g3n8.png", "answer": "م ط ر"},
            {"image": "https://files.catbox.moe/pzgc9e.png", "answer": "ج ي ل"},
            {"image": "https://files.catbox.moe/w6230s.png", "answer": "ج م ل"},
            {"image": "https://files.catbox.moe/1su0gf.png", "answer": "ا س د"},
            {"image": "https://files.catbox.moe/a65w7l.png", "answer": "ت م ر"},
            {"image": "https://files.catbox.moe/pubw4t.png", "answer": "ن م ر"},
            {"image": "https://files.catbox.moe/nu4j8v.png", "answer": "ب ط ل"},
            {"image": "https://files.catbox.moe/c3rcpq.png", "answer": "ش م ا ل"},
            {"image": "https://files.catbox.moe/9jk0le.png", "answer": "ج ن و ب"},
            {"image": "https://files.catbox.moe/ewahcs.png", "answer": "غ ر ب"},
            {"image": "https://files.catbox.moe/b7rsl5.png", "answer": "ش ر ق"},
            {"image": "https://files.catbox.moe/thvawb.png", "answer": "ن ج م"},
            {"image": "https://files.catbox.moe/0hts0c.png", "answer": "ك و ك ب"},
            {"image": "https://files.catbox.moe/jtp95n.png", "answer": "س ك ي ن"},
            {"image": "https://files.catbox.moe/n5rmhu.png", "answer": "ز ر"},
            {"image": "https://files.catbox.moe/arsqs9.png", "answer": "ب ئ ر"},
            {"image": "https://files.catbox.moe/7w6ntu.png", "answer": "ق ا ع"},
            {"image": "https://files.catbox.moe/h7nheo.png", "answer": "ع م ي ق"},
            {"image": "https://files.catbox.moe/2m0dnq.png", "answer": "م ح م د"},
            {"image": "https://files.catbox.moe/4zj6vz.png", "answer": "س ع و د ي ة"},
            {"image": "https://files.catbox.moe/c35tiv.png", "answer": "م ل ع ب"},
            {"image": "https://files.catbox.moe/50q7tf.png", "answer": "ر و س ي ا"},
            {"image": "https://files.catbox.moe/vypod3.png", "answer": "ا م ر ي ك ا"},
            {"image": "https://files.catbox.moe/j5ttsf.png", "answer": "ب ا ب"},
            {"image": "https://files.catbox.moe/xbtwwt.png", "answer": "ق ف ل"},
            {"image": "https://files.catbox.moe/vimctg.png", "answer": "م ف ت ا ح"},
            {"image": "https://files.catbox.moe/eesg4z.png", "answer": "ر و ض ة"},
            {"image": "https://files.catbox.moe/lstd7r.png", "answer": "ك ر ة"},
            {"image": "https://files.catbox.moe/dmwloo.png", "answer": "ب ا ر ي س"},
            {"image": "https://files.catbox.moe/vxvuxp.png", "answer": "ا ل ر ي ا ض"},
            {"image": "https://files.catbox.moe/aonmyf.png", "answer": "ص د ئ"},
            {"image": "https://files.catbox.moe/eegpvf.png", "answer": "م ه ن ة"},
            {"image": "https://files.catbox.moe/j8us48.png", "answer": "د ر ا س ة"},
          
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
    await bot.add_cog(fkkgame(bot))
