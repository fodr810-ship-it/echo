import discord
from discord.ext import commands
import random
import asyncio

class HideSeekCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.spots = ["السطح 🏢", "القبو 🚪", "خلف الشجرة 🌳", "تحت السرير 🛏️", "الخزانة 🧥", "خلف الستارة 🎭", "الحديقة 🌻", "المطبخ 🍽️"]

    @commands.command(name="لعبة_الاختباء", aliases=["تخبي"])
    async def start_hide(self, ctx):
        game = {"players": {}, "started": False}
        self.active_games[ctx.channel.id] = game

        embed = discord.Embed(title="🕵️‍♂️ لعبة الاختباء الكبرى", description="انضموا للعبة! بمجرد اكتمال العدد سيبدأ وقت الاختباء.", color=discord.Color.blurple())
        
        class JoinView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)
            @discord.ui.button(label="انضمام 🏃", style=discord.ButtonStyle.green)
            async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
                game["players"][interaction.user] = None
                await interaction.response.send_message(f"✅ انضم {interaction.user.name}!", ephemeral=True)
                await interaction.message.edit(content=f"**المنضمون:** {', '.join([p.name for p in game['players']])}")

        msg = await ctx.send(embed=embed, view=JoinView())
        await asyncio.sleep(20) # وقت انتظار الانضمام

        if len(game["players"]) < 2:
            return await ctx.send("❌ يحتاج على الأقل لاعبين!")

        # اختيار الصياد
        seeker = random.choice(list(game["players"].keys()))
        game["seeker"] = seeker
        await ctx.send(f"🚨 الصياد هو: {seeker.mention}! باقي اللاعبين لديهم 20 ثانية للاختباء.")

        # اختيار أماكن الاختباء
        for p in game["players"]:
            if p != seeker:
                spot = random.choice(self.spots)
                game["players"][p] = spot
                try:
                    await p.send(f"🤫 اختبأت في: **{spot}**. انتظر الصياد!")
                except:
                    await ctx.send(f"⚠️ لا أستطيع إرسال رسالة خاصة لـ {p.mention}، اختبأ في مكان سري!")

        await asyncio.sleep(20)
        await ctx.send(f"🔍 انتهى وقت الاختباء! يا {seeker.mention}، قم بتخمين مكان أحد اللاعبين باستخدام `!ابحث [المكان]`")
        game["started"] = True

    @commands.command(name="ابحث")
    async def search(self, ctx, *, place: str):
        game = self.active_games.get(ctx.channel.id)
        if not game or not game.get("started") or ctx.author != game["seeker"]:
            return

        for p, spot in game["players"].items():
            if p != ctx.author and place in spot:
                await ctx.send(f"🔥 وجدتك يا {p.mention}! كنت مختبئاً في {spot}!")
                del game["players"][p]
                if len(game["players"]) == 1:
                    await ctx.send("🏆 انتهت اللعبة! الصياد فاز!")
                    del self.active_games[ctx.channel.id]
                return
        
        await ctx.send("❌ خائب الأمل.. المكان فارغ!")

async def setup(bot):
    await bot.add_cog(HideSeekCog(bot))