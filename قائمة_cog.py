import discord
from discord.ext import commands

class GamesListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_channel_id = 1518382443000893440 

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        # إذا أردت تفعيل حصر الروم، قم بإزالة علامات #
        # if message.channel.id != self.allowed_channel_id:
        #     return
            
        if message.content.strip() == "العاب":
            
            # تم إضافة \n إضافية للفصل بين القسمين وتحسين المظهر
            games_text = (
                "**Solo ⟢**\n"
                "𓂃 ترتيب\n𓂃 حروف\n𓂃 ايموجي\n𓂃 اسرع\n𓂃 فكك\n"
                "𓂃 اشبك\n𓂃 صحح\n𓂃 اعلام\n𓂃 قارة\n𓂃 عواصم\n"
                "𓂃 مفرد\n𓂃 جمع\n𓂃 اكشف\n𓂃 الوان\n𓂃 زر\n"
                "𓂃 ارقام\n𓂃 !حجرة\n𓂃 !xo\n𓂃 حساب\n\n"
                "**Group ⟢**\n"
                "𓂃 كراسي!\n𓂃 مافيا!\n𓂃 روليت!\n𓂃 !codenames\n"
                "𓂃 غميضة!\n𓂃 ريبلكا!"
            )

            embed = discord.Embed(
                description=games_text,
                color=discord.Color.blurple()
            )
            
            if self.bot.user.display_avatar:
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
            embed.set_footer(text="EchoGamesSystem")
            
            await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GamesListCog(bot))