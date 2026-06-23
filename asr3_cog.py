import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class fastgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "asr3_scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "https://files.catbox.moe/3pa6aq.png", "answer": "دراسة"},
            {"image": "https://files.catbox.moe/sqx1s7.png", "answer": "عطالة"},
            {"image": "https://files.catbox.moe/gqbvd1.png", "answer": "ربح"},
            {"image": "https://files.catbox.moe/hum0pk.png", "answer": "امريكا"},
            {"image": "https://files.catbox.moe/1olbr6.png", "answer": "روسيا"},
            {"image": "https://files.catbox.moe/nodhfz.png", "answer": "السعودية"},
            {"image": "https://files.catbox.moe/kc42ox.png", "answer": "مملكة"},
            {"image": "https://files.catbox.moe/317sya.png", "answer": "عبدالله"},
            {"image": "https://files.catbox.moe/9isxh6.png", "answer": "محمد"},
            {"image": "https://files.catbox.moe/t3irn1.png", "answer": "قلم"},
            {"image": "https://files.catbox.moe/3dhd9u.png", "answer": "كتاب"},
            {"image": "https://files.catbox.moe/9cqdf0.png", "answer": "حبر"},
            {"image": "https://files.catbox.moe/cw7lwq.png", "answer": "حقيبة"},
            {"image": "https://files.catbox.moe/0cy145.png", "answer": "معلم"},
            {"image": "https://files.catbox.moe/nbw8p7.png", "answer": "مدرسة"},
            {"image": "https://files.catbox.moe/73q4c4.png", "answer": "سفر"},
            {"image": "https://files.catbox.moe/fb6bmg.png", "answer": "استطاعة"},
            {"image": "https://files.catbox.moe/faslv5.png", "answer": "قدرة"},
            {"image": "https://files.catbox.moe/aagedt.png", "answer": "زمن"},
            {"image": "https://files.catbox.moe/kp086m.png", "answer": "طيار"},
            {"image": "https://files.catbox.moe/p388no.png", "answer": "طيارة"},
            {"image": "https://files.catbox.moe/46mu6b.png", "answer": "نادل"},
            {"image": "https://files.catbox.moe/o8jvvs.png", "answer": "سريع"},
            {"image": "https://files.catbox.moe/oo38ih.png", "answer": "حزين"},
            {"image": "https://files.catbox.moe/vriyyz.png", "answer": "برتقال"},
            {"image": "https://files.catbox.moe/vbwrl9.png", "answer": "يحيى"},
            {"image": "https://files.catbox.moe/c78pqa.png", "answer": "علم"},
            {"image": "https://files.catbox.moe/02rn5e.png", "answer": "عاصمة"},
            {"image": "https://files.catbox.moe/wgxlo1.png", "answer": "جديد"},
            {"image": "https://files.catbox.moe/e2eacx.png", "answer": "التالي"},
            {"image": "https://files.catbox.moe/p6620n.png", "answer": "كوريا الشمالية"},
            {"image": "https://files.catbox.moe/3vhgve.png", "answer": "شمال"},
            {"image": "https://files.catbox.moe/axhliu.png", "answer": "جنوب"},
            {"image": "https://files.catbox.moe/04kurl.png", "answer": "شرق"},
            {"image": "https://files.catbox.moe/ym2t4z.png", "answer": "غرب"},
            {"image": "https://files.catbox.moe/nf3wzx.png", "answer": "قبيلة"},
            {"image": "https://files.catbox.moe/9ywpzf.png", "answer": "حياة"},
            {"image": "https://files.catbox.moe/v83tf0.png", "answer": "فائز"},
            {"image": "https://files.catbox.moe/1xlmaf.png", "answer": "اقنصاد"},
            {"image": "https://files.catbox.moe/gmibir.png", "answer": "دولة"},
            {"image": "https://files.catbox.moe/4sz7qy.png", "answer": "قرطاس"},
            {"image": "https://files.catbox.moe/41cnc0.png", "answer": "سيف"},
            {"image": "https://files.catbox.moe/vkqn5p.png", "answer": "رمح"},
            {"image": "https://files.catbox.moe/7obphj.png", "answer": "الملك"},
            {"image": "https://files.catbox.moe/p9adgq.png", "answer": "قائد"},
            {"image": "https://files.catbox.moe/l6pvi9.png", "answer": "هاتف"},
            {"image": "https://files.catbox.moe/zmstj8.png", "answer": "اماكن"},
            {"image": "https://files.catbox.moe/5gua55.png", "answer": "جبال"},
            {"image": "https://files.catbox.moe/pv2uhc.png", "answer": "شاهقة"},
            {"image": "https://files.catbox.moe/tir70s.png", "answer": "معركة"},
            {"image": "https://files.catbox.moe/2e3jfb.png", "answer": "جيش"},
            {"image": "https://files.catbox.moe/x8z79l.png", "answer": "كفاءة"},
            {"image": "https://files.catbox.moe/jw8fkq.png", "answer": "موظف"},
            {"image": "https://files.catbox.moe/p5gfhq.png", "answer": "كرة قدم"},
           
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
    await bot.add_cog(fastgame(bot))
