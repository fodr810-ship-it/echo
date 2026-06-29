import discord
from discord.ext import commands
import random
import asyncio
import json
import os

class HideSeekCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = "global_points.json"  # ملف النقاط الموحد
        self.active_games = {}
        self.spots = ["السطح 🏢", "القبو 🚪", "خلف الشجرة 🌳", "تحت السرير 🛏️", "الخزانة 🧥", "خلف الستارة 🎭", "الحديقة 🌻", "المطبخ 🍽️"]

        # التأكد من وجود القفل العام المشترك داخل كائن البوت لجميع الألعاب
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

    # دالة قراءة النقاط وتحديثها في الملف الموحد مباشرة
    def add_score(self, user_id):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r", encoding="utf-8") as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = {}
        else:
            scores = {}
        
        user_id_str = str(user_id)
        scores[user_id_str] = scores.get(user_id_str, 0) + 1
        
        with open(self.scores_file, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)
            
        return scores[user_id_str]

    @commands.command(name="لعبة_الاختباء", aliases=["تخبي"])
    async def start_hide_cmd(self, ctx):
        await self.run_game(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "تخبي" or message.content.strip() == "لعبة_الاختباء":
            ctx = await self.bot.get_context(message)
            await self.run_game(ctx)

    async def run_game(self, ctx):
        # 🟢 الفحص باستخدام القفل العام المشترك لمنع تداخل الألعاب
        if ctx.channel.id in self.bot.global_game_lock:
            return await ctx.send("⚠️ هناك لعبة جارية بالفعل في هذا الروم! انتظر حتى تنتهي.")

        # قفل الروم في البوت كاملاً
        self.bot.global_game_lock.add(ctx.channel.id)

        game = {"players": {}, "started": False}
        self.active_games[ctx.channel.id] = game

        embed = discord.Embed(
            title="🕵️‍♂️ لعبة الاختباء الكبرى", 
            description="اضغطوا على الزر للإنضمام للعبة! تحتاج اللعبة إلى لاعبين على الأقل للبدء.", 
            color=discord.Color.blurple()
        )
        
        class JoinView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=20.0)
            @discord.ui.button(label="انضمام 🏃", style=discord.ButtonStyle.green)
            async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user in game["players"]:
                    return await interaction.response.send_message("❌ أنت منضم بالفعل للعبة!", ephemeral=True)
                game["players"][interaction.user] = None
                await interaction.response.send_message(f"✅ انضممت للعبة بنجاح!", ephemeral=True)
                await interaction.message.edit(content=f"**اللاعبون المنضمون حالياً:**\n" + "\n".join([f"- {p.mention}" for p in game['players']]))

        msg = await ctx.send(embed=embed, view=JoinView())
        await asyncio.sleep(20) # وقت انتظار الانضمام

        if len(game["players"]) < 2:
            await ctx.send("❌ تم إلغاء اللعبة لعدم توفر عدد كافٍ من اللاعبين (تحتاج لاعبين على الأقل).")
            self.bot.global_game_lock.discard(ctx.channel.id)
            del self.active_games[ctx.channel.id]
            return

        # اختيار الصياد
        seeker = random.choice(list(game["players"].keys()))
        game["seeker"] = seeker
        await ctx.send(f"🚨 الصياد المختار هو: {seeker.mention}!\nباقي اللاعبين، تم إرسال أماكن اختبائكم السرية في الخاص. لديكم 15 ثانية للتأهب.")

        # توزيع الأماكن عشوائياً للاختباء وإرسالها للأعضاء في الخاص
        for p in list(game["players"].keys()):
            if p != seeker:
                spot = random.choice(self.spots)
                game["players"][p] = spot
                try:
                    await p.send(f"🤫 مكانك السري المختار للاختباء هو: **{spot}**. لا تخبر الصياد وانتظره حتى يبحث!")
                except:
                    pass

        await asyncio.sleep(15)
        await ctx.send(f"🔍 انتهى وقت التجهيز! الآن يا صياد {seeker.mention}، استخدم أزرار البحث بالأسفل لتخمين أماكن تواجد اللاعبين:")

        # كلاس أزرار البحث المخصصة للصياد فقط
        class SeekerSearchView(discord.ui.View):
            def __init__(self, cog, channel_id, seeker_obj, total_spots):
                super().__init__(timeout=45.0)
                self.cog = cog
                self.channel_id = channel_id
                self.seeker = seeker_obj
                self.message_obj = None

                # توليد الأزرار للأماكن وترتيبها بحد أقصى 5 أزرار في الصف
                for i, spot in enumerate(total_spots):
                    row_idx = i // 4
                    btn = discord.ui.Button(
                        label=spot,
                        style=discord.ButtonStyle.primary,
                        custom_id=f"spot_{spot}",
                        row=row_idx
                    )
                    btn.callback = self.do_search
                    self.add_item(btn)

            async def do_search(self, interaction: discord.Interaction):
                # التحقق أن ضاغط الزر هو الصياد الفعلي للعبة فقط
                if interaction.user != self.seeker:
                    return await interaction.response.send_message("❌ لست أنت الصياد في هذه اللعبة! انتظر دورك.", ephemeral=True)

                current_game = self.cog.active_games.get(self.channel_id)
                if not current_game:
                    return

                chosen_spot = interaction.data["custom_id"].replace("spot_", "")
                
                # إيجاد إذا كان أي لاعب يختبئ في هذا المكان المعين
                found_player = None
                for p, s in current_game["players"].items():
                    if p != self.seeker and s == chosen_spot:
                        found_player = p
                        break

                # تعطيل الزر الذي تم البحث فيه وتغيير لونه بناءً على النتيجة
                for child in self.children:
                    if child.custom_id == interaction.data["custom_id"]:
                        child.disabled = True
                        if found_player:
                            child.style = discord.ButtonStyle.success  # أخضر إذا وجده
                        else:
                            child.style = discord.ButtonStyle.danger   # أحمر إذا كان فارغاً
                        break

                await interaction.message.edit(view=self)

                if found_player:
                    # حذف اللاعب بعد كشفه
                    del current_game["players"][found_player]
                    
                    await interaction.response.send_message(f"🔥 كفو! الصياد وجد {found_player.mention} مختبئاً في **{chosen_spot}**!")
                    
                    # التحقق إذا تم كشف جميع اللاعبين المختبئين وفوز الصياد
                    remaining_players = [p for p in current_game["players"] if p != self.seeker]
                    if len(remaining_players) == 0:
                        # الصياد يحصل على نقطة
                        new_score = self.cog.add_score(self.seeker.id)
                        
                        embed_win = discord.Embed(
                            title="🏆 انتهت اللعبة بفوز الصياد!",
                            description=f"لقد وجد الصياد {self.seeker.mention} جميع المختبئين بنجاح!\nنقاط الصياد الإجمالية: **{new_score}**",
                            color=discord.Color.green()
                        )
                        await interaction.channel.send(embed=embed_win)
                        self.stop()
                        self.clean_game()
                else:
                    await interaction.response.send_message(f"💨 بحثت في **{chosen_spot}** لكنه كان فارغاً تماماً.. حاول مجدداً!")

            def clean_game(self):
                self.cog.bot.global_game_lock.discard(self.channel_id)
                if self.channel_id in self.cog.active_games:
                    del self.cog.active_games[self.channel_id]

            async def on_timeout(self):
                # إذا انتهى الوقت المخصص للبحث، يفوز اللاعبون الصامدون الذين لم يتم كشفهم
                current_game = self.cog.active_games.get(self.channel_id)
                if current_game:
                    remaining_players = [p for p in current_game["players"] if p != self.seeker]
                    if len(remaining_players) > 0:
                        winners_mentions = ", ".join([p.mention for p in remaining_players])
                        
                        # توزيع النقاط على صامدي اللعبة المتبقين
                        for p in remaining_players:
                            self.cog.add_score(p.id)

                        embed_timeout = discord.Embed(
                            title="⏳ انتهى وقت البحث!",
                            description=f"انتصر اللاعبون الصامدون لعدم كشفهم في الوقت المحدد!\n🏆 الفائزون: {winners_mentions}",
                            color=discord.Color.red()
                        )
                        await self.message_obj.channel.send(embed=embed_timeout)
                
                # تعطيل كافة الأزرار عند انتهاء الوقت
                for child in self.children:
                    child.disabled = True
                try:
                    await self.message_obj.edit(view=self)
                except:
                    pass
                self.clean_game()

        search_view = SeekerSearchView(self, ctx.channel.id, seeker, self.spots)
        search_msg = await ctx.send("🎛️ **لوحة التحكم بالبحث السرية:**", view=search_view)
        search_view.message_obj = search_msg

async def setup(bot):
    await bot.add_cog(HideSeekCog(bot))