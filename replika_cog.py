import discord
from discord.ext import commands
import random
import asyncio

class ReplikaGame:
    def __init__(self, ctx):
        self.ctx = ctx
        self.players = []

class ReplikaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.letters = ["أ", "ب", "ت", "ج", "ح", "خ", "د", "ر", "ز", "س", "ش", "ص", "ط", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "هـ", "و", "ي"]
        self.categories = ["اسم 🧑", "حيوان 🦁", "نبات 🌿", "جماد 📦", "دولة 🗺️"]

    @commands.command(name="ريبلكا", aliases=["replika"])
    async def start_replika(self, ctx):
        if ctx.channel.id in self.active_games:
            return await ctx.send("❌ توجد مباراة ريبلكا قائمة بالفعل في هذا الروم!")

        game = ReplikaGame(ctx)
        self.active_games[ctx.channel.id] = game

        embed = discord.Embed(
            title="🎮 لعبة ريبلكا الإقصائية 🎮",
            description="اضغط على الزر أدناه للمشاركة. آخر لاعب يصمد هو الفائز!",
            color=discord.Color.teal()
        )
        
        class RegisterView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30.0)
            @discord.ui.button(label="دخول اللعبة 🕹️", style=discord.ButtonStyle.blurple)
            async def join_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user in game.players:
                    return await interaction.response.send_message("❌ أنت مسجل بالفعل!", ephemeral=True)
                game.players.append(interaction.user)
                await interaction.response.send_message(f"✅ انضم {interaction.user.mention} للعبة!", ephemeral=True)

        view = RegisterView()
        await ctx.send(embed=embed, view=view)
        await asyncio.sleep(30)
        view.stop()

        if len(game.players) < 2:
            del self.active_games[ctx.channel.id]
            return await ctx.send("❌ تم إلغاء اللعبة: يجب توفر لاعبين على الأقل.")

        active_players = list(game.players)
        await ctx.send("🏁 **بدأت المباراة!**")

        round_num = 1
        while len(active_players) > 1:
            current_letter = random.choice(self.letters)
            await ctx.send(f"🏹 **الجولة {round_num}** | الحرف المختار: **[{current_letter}]**")
            await asyncio.sleep(2)

            for category in self.categories:
                if len(active_players) <= 1: break
                
                # خلط اللاعبين لاختيار دور جديد عشوائي لكل قسم
                random.shuffle(active_players)
                target_player = active_players[0]
                
                await ctx.send(f"🚨 {target_player.mention} الدور عليك! أرسل **{category}** يبدأ بحرف **({current_letter})** (معاك 15 ثانية)")

                def check_reply(m):
                    return m.author.id == target_player.id and m.channel.id == ctx.channel.id

                try:
                    msg = await self.bot.wait_for("message", check=check_reply, timeout=15.0)
                    content = msg.content.strip()
                    
                    # فحص ذكي للألف والهمزات
                    alif = ["أ", "ا", "إ", "آ"]
                    is_correct = (content.startswith(current_letter)) or (current_letter in alif and content[0] in alif)

                    if is_correct:
                        await ctx.send(f"✅ صح! نجا {target_player.mention}.")
                    else:
                        await ctx.send(f"❌ الكلمة خطأ! تم إقصاء {target_player.mention} من اللعبة.")
                        active_players.remove(target_player)
                
                except asyncio.TimeoutError:
                    await ctx.send(f"💥 انتهى الوقت! تم إقصاء {target_player.mention} لعدم الرد.")
                    active_players.remove(target_player)
                
                await asyncio.sleep(1)
            
            round_num += 1

        if len(active_players) == 1:
            winner = active_players[0]
            await ctx.send(f"👑 **مبروك! الفائز بالبطولة هو {winner.mention}** 👑")
        
        del self.active_games[ctx.channel.id]

async def setup(bot):
    await bot.add_cog(ReplikaCog(bot))