import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class GameOne(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = "scores.json"
        self.scores = self.load_scores()
        self.questions = [
            {"image": "https://files.catbox.moe/32pqlr.png", "answer": "اجسام مضادة"},
            {"image": "https://files.catbox.moe/a5f2f0.png", "answer": "ابو العتاهية"},
            {"image": "https://files.catbox.moe/5v89y4.png", "answer": "اسامة بن زيد"},
            {"image": "https://files.catbox.moe/uiqye5.png", "answer": "اميتر"},
            {"image": "https://files.catbox.moe/vbt02h.png", "answer": "ابو دجانة"},
            {"image": "https://files.catbox.moe/aomolk.png", "answer": "الايض"},
            {"image": "https://files.catbox.moe/h4ni38.png", "answer": "ابتر"},
            {"image": "https://files.catbox.moe/h8lai1.png", "answer": "الالب"},
            {"image": "https://files.catbox.moe/aigbc2.png", "answer": "الادراك"},
            {"image": "https://files.catbox.moe/bh7jnm.png", "answer": "احد"},
            {"image": "https://files.catbox.moe/peeah7.png", "answer": "الابهر"},
            {"image": "https://files.catbox.moe/803fn6.png", "answer": "اكسجين"},
            {"image": "https://files.catbox.moe/63mpbh.png", "answer": "ارامكو"},
            {"image": "https://files.catbox.moe/b17old.png", "answer": "اصالة"},
            {"image": "https://files.catbox.moe/ul60cd.png", "answer": "اشبيلية"},
            {"image": "https://files.catbox.moe/brtct2.png", "answer": "ابن كثير"},
            {"image": "https://files.catbox.moe/l3fmqn.png", "answer": "بنكرياس"},
            {"image": "https://files.catbox.moe/ygbobj.png", "answer": "برزخ"},
            {"image": "https://files.catbox.moe/snxa3t.png", "answer": "باريس"},
            {"image": "https://files.catbox.moe/b3d2kg.png", "answer": "بث"},
            {"image": "https://files.catbox.moe/j28akp.png", "answer": "بلاغة"},
            {"image": "https://files.catbox.moe/qauqht.png", "answer": "بيت الحكمة"},
            {"image": "https://files.catbox.moe/wffjn3.png", "answer": "بنود"},
            {"image": "https://files.catbox.moe/mq1mm1.png", "answer": "بروتين"},
            {"image": "https://files.catbox.moe/e6r0mi.png", "answer": "بروفة"},
            {"image": "https://files.catbox.moe/ksr1xp.png", "answer": "باب المندب"},
            {"image": "https://files.catbox.moe/dar92u.png", "answer": "بندول"},
            {"image": "https://files.catbox.moe/8tkngo.png", "answer": "بلايستيشن"},
            {"image": "https://files.catbox.moe/23idvc.png", "answer": "بلال بن رباح"},
            {"image": "https://files.catbox.moe/zkt1gj.png", "answer": "بيت"},
            {"image": "https://files.catbox.moe/fr9vax.png", "answer": "البراق"},
            {"image": "https://files.catbox.moe/spzvph.png", "answer": "بارود"},
            {"image": "https://files.catbox.moe/3yg551.png", "answer": "بقلاوة"},
            {"image": "https://files.catbox.moe/a0k2si.png", "answer": "تحكيم"},
            {"image": "https://files.catbox.moe/j00eer.png", "answer": "تنين"},
            {"image": "https://files.catbox.moe/lmt3vs.png", "answer": "تصحر"},
            {"image": "https://files.catbox.moe/0alsc5.png", "answer": "تطوع"},
            {"image": "https://files.catbox.moe/au3iyi.png", "answer": "تشفير"},
            {"image": "https://files.catbox.moe/5igvyu.png", "answer": "تقليد"},
            {"image": "https://files.catbox.moe/et01xi.png", "answer": "تلفاز"},
            {"image": "https://files.catbox.moe/4ngbnq.png", "answer": "ترميم"},
            {"image": "https://files.catbox.moe/jzblr1.png", "answer": "تربة"},
            {"image": "https://files.catbox.moe/765mf1.png", "answer": "تنس"},
            {"image": "https://files.catbox.moe/lcpjld.png", "answer": "تبليسي"},
            {"image": "https://files.catbox.moe/g8vcpd.png", "answer": "تلال"},
            {"image": "https://files.catbox.moe/xxfns3.png", "answer": "تلبينة"},
            {"image": "https://files.catbox.moe/d6473d.png", "answer": "تمثال"},
            {"image": "https://files.catbox.moe/sip80j.png", "answer": "تكاثر"},
            {"image": "https://files.catbox.moe/5zbh4v.png", "answer": "تحليل"},
            {"image": "https://files.catbox.moe/5fqlak.png", "answer": "تغريد"},
            {"image": "https://files.catbox.moe/9qfp53.png", "answer": "ترويض"},
            {"image": "https://files.catbox.moe/fnvf84.png", "answer": "تبوك"},
            {"image": "https://files.catbox.moe/q2y401.png", "answer": "ثقب"},
            {"image": "https://files.catbox.moe/royjt7.png", "answer": "ثادق"},
            {"image": "https://files.catbox.moe/1zxtuy.png", "answer": "ثابت بن قيس"},
            {"image": "https://files.catbox.moe/76bjko.png", "answer": "ثمود"},
            {"image": "https://files.catbox.moe/wges01.png", "answer": "ثمل"},
            {"image": "https://files.catbox.moe/a9xfhu.png", "answer": "ثاج"},
            {"image": "https://files.catbox.moe/w3alqz.png", "answer": "ثنايا"},
            {"image": "https://files.catbox.moe/2gecte.png", "answer": "ثغرة"},
            {"image": "https://files.catbox.moe/hw2osd.png", "answer": "ثعبان"},
            {"image": "https://files.catbox.moe/uva241.png", "answer": "ثقافة"},
            {"image": "https://files.catbox.moe/9178st.png", "answer": "ثقلان"},
            {"image": "https://files.catbox.moe/uz7tmb.png", "answer": "ثعلبة"},
            {"image": "https://files.catbox.moe/5motsd.png", "answer": "ثورة"},
            {"image": "https://files.catbox.moe/s559hc.png", "answer": "ثقوب سوداء"},
            {"image": "https://files.catbox.moe/jkomab.png", "answer": "ثكلى"},
            {"image": "https://files.catbox.moe/q130sr.png", "answer": "ثمين"},
            {"image": "https://files.catbox.moe/qhkpyk.png", "answer": "ثراء"},
            {"image": "https://files.catbox.moe/ocs7r2.png", "answer": "ثاقب"},
            {"image": "https://files.catbox.moe/v2jpfv.png", "answer": "ثابت"},
            {"image": "https://files.catbox.moe/uliate.png", "answer": "ثكنة"},
            {"image": "https://files.catbox.moe/7sj025.png", "answer": "جازف"},
            {"image": "https://files.catbox.moe/3zfebx.png", "answer": "جربوع"},
            {"image": "https://files.catbox.moe/jbjiye.png", "answer": "جب"},
            {"image": "https://files.catbox.moe/ngabto.png", "answer": "جاسوس"},
            {"image": "https://files.catbox.moe/afzexj.png", "answer": "جدال"},
            {"image": "https://files.catbox.moe/8asj51.png", "answer": "جدار خلوي"},
            {"image": "https://files.catbox.moe/owtoas.png", "answer": "جورج وياه"},
            {"image": "https://files.catbox.moe/jxgr26.png", "answer": "جدباء"},
            {"image": "https://files.catbox.moe/dnf5p0.png", "answer": "جاذبية"},
            {"image": "https://files.catbox.moe/cgavdf.png", "answer": "جودة"},
            {"image": "https://files.catbox.moe/rbwzhz.png", "answer": "جزيرة"},
            {"image": "https://files.catbox.moe/ay9khd.png", "answer": "جاهلية"},
            {"image": "https://files.catbox.moe/xojx5l.png", "answer": "جائحة"},
            {"image": "https://files.catbox.moe/l8aoyu.png", "answer": "جبريل"},
            {"image": "https://files.catbox.moe/nguo6p.png", "answer": "جراثيم"},
            {"image": "https://files.catbox.moe/5dcee1.png", "answer": "جابر بن حيان"},
            {"image": "https://files.catbox.moe/pusifs.png", "answer": "جنرال"},
            {"image": "https://files.catbox.moe/r9i9mh.png", "answer": "جدوى"},
            {"image": "https://files.catbox.moe/nuh717.png", "answer": "الجوف"},
            {"image": "https://files.catbox.moe/v9jnfn.png", "answer": "جفون"},
            {"image": "https://files.catbox.moe/ojk16r.png", "answer": "حادة"},
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

    @commands.command(name="حروف")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "حروف":
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
    await bot.add_cog(GameOne(bot))
