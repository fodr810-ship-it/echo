import discord
from discord.ext import commands
import json
import os

class PointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = "global_points.json" # ملف النقاط الموحد

    # دالة لقراءة النقاط من الملف
    def get_points(self, user_id):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r", encoding="utf-8") as f:
                try:
                    scores = json.load(f)
                    # إرجاع النقاط إذا كان العضو موجوداً، أو 0 إذا لم يلعب من قبل
                    return scores.get(str(user_id), 0)
                except json.JSONDecodeError:
                    return 0
        return 0

    
    @commands.command(name="نقاط", aliases=["نقاطي", "رصيدي", "points"])
    async def check_points_cmd(self, ctx, member: discord.Member = None):
        # إذا لم يمنشن أحد، نعرض نقاط صاحب الأمر نفسه
        member = member or ctx.author 
        points = self.get_points(member.id)
        
        embed = discord.Embed(
            title="🏆 رصيد النقاط",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        
        if member == ctx.author:
            embed.description = f"أهلاً {member.mention}، رصيد نقاطك الحالي في الألعاب هو: **{points}** نقطة 🌟"
        else:
            embed.description = f"رصيد نقاط {member.mention} في الألعاب هو: **{points}** نقطة 🌟"
            
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        if message.content.strip() == "نقاطي":
            points = self.get_points(message.author.id)
            
            embed = discord.Embed(
                title="🏆 رصيد النقاط",
                description=f"أهلاً {message.author.mention}، رصيد نقاطك الحالي في الألعاب هو: **{points}** نقطة 🌟",
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            
            await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PointsCog(bot))