import discord
from discord.ext import commands
import random
import asyncio

class ReplikaGame:
    def __init__(self, ctx):
        self.ctx = ctx
        self.players = []
        self.is_registration_open = True

class ReplikaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        # قائمة الحروف المتاحة للعب (تم استبعاد الحروف الصعبة جداً لمتعة اللعب)
        self.letters = ["أ", "ب", "ت", "ج", "ح", "خ", "د", "ر", "ز", "س", "ش", "ص", "ط", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "هـ", "و", "ي"]
        # الأقسام المطلوبة
        self.categories = ["اسم 🧑", "حيوان 🦁", "نبات 🌿", "جماد 📦", "دولة 🗺️"]

    @commands.command(name="ريبلكا", aliases=["replika", "ريبلكا"])
    async def start_replika(self, ctx):
        if ctx.channel.id in self.active_games:
            return await ctx.send("❌ توجد مباراة ريبلكا قائمة بالفعل في هذا الروم!")

        game = ReplikaGame(ctx)
        self.active_games[ctx.channel.id] = game

        # ⏱️ 1. مرحلة فتح التسجيل عبر الأزرار
        embed = discord.Embed(
            title="🎮 لعبة ريبلكا (إنسان حيوان نبات الإقصائية) 🎮",
            description="**طريقة اللعب:**\n1️⃣ اضغط على الزر أدناه لدخول اللعبة.\n2️⃣ يتم اختيار حرف عشوائي كل جولة.\n3️⃣ لكل قسم، يتم اختيار لاعب عشوائي ليرسل الكلمة المناسبة للحرف.\n4️⃣ آخر لاعب يصمد في الحلبة هو الفائز!\n\n⏱️ **الوقت المتبقي للتسجيل: 30 ثانية**\n\n**المشاركين حالياً:**\nلا يوجد أحد بعد.",
            color=discord.Color.teal()
        )
        
        class RegisterView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30.0)
            @discord.ui.button(label="دخول اللعبة 🕹️", style=discord.ButtonStyle.blurple)
            async def join_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user in game.players:
                    return await interaction.response.send_message("❌ أنت مسجل في اللعبة بالفعل!", ephemeral=True)
                game.players.append(interaction.user)
                
                players_list = "\n".join([f"🔹 {p.mention}" for p in game.players])
                embed.description = f"**طريقة اللعب:**\n1️⃣ اضغط على الزر أدناه لدخول اللعبة.\n2️⃣ يتم اختيار حرف عشوائي كل جولة.\n3️⃣ لكل قسم، يتم اختيار لاعب عشوائي ليرسل الكلمة المناسبة للحرف.\n4️⃣ آخر لاعب يصمد في الحلبة هو الفائز!\n\n⏱️ **الوقت المتبقي للتسجيل: 30 ثانية**\n\n**المشاركين حالياً ({len(game.players)}):**\n{players_list}"
                await interaction.response.edit_message(embed=embed)

        view = RegisterView()
        msg = await ctx.send(embed=embed, view=view)
        
        await asyncio.sleep(30) # انتظار انتهاء التسجيل
        view.stop()

        if len(game.players) < 2:
            if ctx.channel.id in self.active_games:
                del self.active_games[ctx.channel.id]
            return await ctx.send("❌ تم إلغاء اللعبة بسبب عدم وجود لاعبين كافيين (أقل شيء لاعبين 2).")

        active_players = list(game.players)
        await ctx.send("🏁 **انتهى وقت التسجيل! جاري تجهيز الجولة الأولى وبدء صراع الحروف...**")
        await asyncio.sleep(2)

        # 🎯 2. حلقة الجولات الإقصائية
        round_num = 1
        while len(active_players) > 1:
            current_letter = random.choice(self.letters)
            
            round_embed = discord.Embed(
                title=f"🏹 ريبلكا - الجولة {round_num} 🏹",
                description=f"🔤 الحرف المختار لهذه الجولة هو: **[ {current_letter} ]**\n\nالبوت سيقوم الآن باختيار لاعبين عشوائيين للأقسام! جهزوا أنفسكم في الشات بسرعة!",
                color=discord.Color.random()
            )
            await ctx.send(embed=round_embed)
            await asyncio.sleep(3)

            # توزيع الأقسام على اللاعبين المتواجدين
            for category in self.categories:
                if len(active_players) <= 1:
                    break # إذا بقي لاعب واحد أثناء الجولة ينتهي كل شيء فوراً

                # اختيار ضحية عشوائية للقسم الحالي
                target_player = random.choice(active_players)
                
                await ctx.send(f"🚨 {target_player.mention} الدور عليك! أرسل في الشات **{category}** يبدأ بحرف **({current_letter})** عجلللل! (معاك 15 ثانية)")

                def check_reply(m):
                    # التحقق أن الرسالة من اللاعب المستهدف، في نفس الروم، وتبدأ بالحرف المطلوب فعلاً
                    return m.author.id == target_player.id and m.channel.id == ctx.channel.id and m.content.strip().startswith(current_letter)

                try:
                    # انتظار إجابة اللاعب خلال 15 ثانية
                    player_msg = await self.bot.wait_for("message", check=check_reply, timeout=15.0)
                    await ctx.send(f"✅ إجابة مقبولة وسريعة! **{player_msg.content}**.. نجا {target_player.mention} من المقصلة.")
                    await asyncio.sleep(1.5)
                except asyncio.TimeoutError:
                    # في حال انتهاء الوقت يتم إقصاؤه فوراً
                    active_players.remove(target_player)
                    await ctx.send(f"💥 **بمبببب!** انتهى الوقت ولم يرسل الكلمة الصحيحة! تم إقصاء {target_player.mention} 🪓")
                    await asyncio.sleep(2)
                    if len(active_players) <= 1:
                        break

            round_num += 1
            if len(active_players) > 1:
                await ctx.send(f"🔄 انتهت الجولة! اللاعبين الصامدين المتبقين: `{len(active_players)}`. جاري الانتقال للحرف التالي...")
                await asyncio.sleep(3)

        # 🏆 3. إعلان الفائز النهائي بالبطولة
        if len(active_players) == 1:
            winner = active_players[0]
            win_embed = discord.Embed(
                title="👑 بطل ريبلكا الأسطوري! 👑",
                description=f"🏆 ألف مبروك الفوز الأسطوري للاعب: {winner.mention}\nصمد ضد الجميع وثبت ذكاءه وسرعته في ريبلكا الحروف!",
                color=discord.Color.gold()
            )
            win_embed.set_thumbnail(url=winner.display_avatar.url)
            await ctx.send(embed=win_embed)

        # تنظيف الغرفة بعد انتهاء المباراة كاملة
        if ctx.channel.id in self.active_games:
            del self.active_games[ctx.channel.id]

async def setup(bot):
    await bot.add_cog(ReplikaCog(bot))
    print("✅ تم تحميل كوج لعبة ريبلكا الحروف الإقصائية بنجاح!")