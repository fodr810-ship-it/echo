import discord
from discord.ext import commands

class GamesListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # حط آيدي الروم المخصص للألعاب هنا (إذا تبي الأمر يشتغل بروم واحد)
        self.allowed_channel_id = 1518382443000893440 

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        # (اختياري) إذا تبي الأمر يشتغل في روم محدد بس، شيل علامة المربع من السطرين اللي تحت
        # if message.channel.id != self.allowed_channel_id:
        #     return
            
        if message.content.strip() == "العاب":
            
            # ترتيبك الأنيق للألعاب تم وضعه هنا
            games_text = (
                "**solo ⟢**\n"
                "𓂃 ترتيب\n"
                "𓂃 حروف\n"
                "𓂃 ايموجي\n"
                "𓂃 اسرع\n"
                "𓂃 فكك\n"
                "𓂃 اشبك\n"
                "𓂃 صحح\n"
                "𓂃 اعلام\n"
                "𓂃 قارة\n"
                "𓂃 عواصم\n"
                "𓂃 مفرد\n"
                "𓂃 جمع\n"
                "𓂃 اكشف\n"
                "𓂃 الوان\n"
                "𓂃 زر\n"
                "𓂃 ارقام\n"
                "𓂃 حساب"
            )

            # إنشاء الإمبد
            embed = discord.Embed(
                description=games_text,
                color=discord.Color.blurple()
            )
            
            # صورة البوت تطلع على اليمين فوق
            if self.bot.user.display_avatar:
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
            # فوتر خفيف يعلمهم كيف يشوفون نقاطهم
            embed.set_footer(text="لمعرفة رصيدك البنكي اكتب: نقاط 💳")
            
            await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GamesListCog(bot))