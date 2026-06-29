import discord
from discord.ext import commands
import random
import json
import os

class FastButtonGame20(discord.ui.View):
    def __init__(self, cog, channel_id):
        super().__init__(timeout=30.0) 
        self.cog = cog
        self.channel_id = channel_id
        self.message_obj = None # لحفظ الرسالة والتحكم فيها عند التايم آوت
        self.winner = None
        
        # اختيار زر واحد عشوائياً ليكون الفائز من بين 20 زر (الاندكس من 0 إلى 19)
        correct_btn_index = random.randint(0, 19)
        
        for i in range(20):
            # تحديد الصف (ديسكورد يقبل 5 أزرار في كل صف كحد أقصى)
            # بهذه الطريقة الـ 20 زر راح تترتب في 4 صفوف
            current_row = i // 5 
            
            if i == correct_btn_index:
                # الزر المنور (الصحيح)
                btn = discord.ui.Button(
                    label="🎯", # إيموجي مميز للزر الصحيح
                    style=discord.ButtonStyle.success, 
                    custom_id=f"correct_{i}",
                    row=current_row
                )
                btn.callback = self.correct_answer
            else:
                # الأزرار التمويهية
                btn = discord.ui.Button(
                    label="➖", # إيموجي بسيط للأزرار الغلط عشان يطلع الشكل مرتب
                    style=discord.ButtonStyle.secondary, 
                    custom_id=f"wrong_{i}",
                    row=current_row
                )
                btn.callback = self.wrong_answer
            
            self.add_item(btn)

    async def correct_answer(self, interaction: discord.Interaction):
        # منع أكثر من شخص من الفوز بنفس اللحظة
        if self.winner:
            return 
            
        self.winner = interaction.user
        
        # 🟢 فتح القفل العام للبوت في هذه الروم فور الفوز للسماح بلعب ألعاب أخرى
        self.cog.bot.global_game_lock.discard(self.channel_id)
        
        # تعطيل كل الـ 20 زر بعد الفوز
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        
        # 🟢 تحديث وحفظ النقاط في ملف الجيسون الموحد المشترك
        new_score = self.cog.add_score(interaction.user.id)
        
        # إمبد الفوز
        win_embed = discord.Embed(
            title="🎉 مبروك عندنا فائز!",
            description=f"أسرع واحد صاد الزر هو {interaction.user.mention} 🏆",
            color=discord.Color.gold()
        )
        
        # زر عرض النقاط
        points_view = discord.ui.View()
        points_btn = discord.ui.Button(
            label=f"نقاطك الإجمالية: {new_score}", 
            style=discord.ButtonStyle.primary, 
            disabled=True
        )
        points_view.add_item(points_btn)
        
        await interaction.response.send_message(embed=win_embed, view=points_view)
        self.stop()

    async def wrong_answer(self, interaction: discord.Interaction):
        await interaction.response.send_message("خطأ! ركز على الزر المنور 🎯", ephemeral=True)
        
    # دالة ذكية لإغلاق اللعبة وفتح القفل إذا مرت 30 ثانية ولم يضغط أحد على الزر الصحيح
    async def on_timeout(self):
        # 🟢 فتح القفل العام للبوت
        self.cog.bot.global_game_lock.discard(self.channel_id)
        
        # تعطيل جميع الأزرار
        for child in self.children:
            child.disabled = True
            
        if self.message_obj:
            try:
                timeout_embed = discord.Embed(
                    title="⏳ انتهى الوقت!",
                    description="محد قدر يضغط الزر الصحيح في الوقت المحدد.",
                    color=discord.Color.red()
                )
                await self.message_obj.edit(embed=timeout_embed, view=self)
            except:
                pass


class ButtonGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = "global_points.json" # ملف النقاط المشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

    # دالة قراءة وإضافة النقاط لملف الجيسون
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        if message.content.strip() == "زر":
            # 🟢 الفحص باستخدام القفل العام لمنع تشغيل اللعبة إذا كانت هناك لعبة أخرى نشطة
            if message.channel.id in self.bot.global_game_lock:
                await message.channel.send("⚠️ هناك لعبة جارية بالفعل في هذا الروم! انتظر حتى تنتهي.")
                return

            # قفل الروم في البوت كاملاً
            self.bot.global_game_lock.add(message.channel.id)

            embed = discord.Embed(
                title="🎮 لعبة صيد الزر",
                description="أمامك 20 زر، أسرع واحد يضغط على الزر المنوّر (🎯 الأخضر) هو الفائز!",
                color=discord.Color.blurple()
            )
            
            view = FastButtonGame20(self, message.channel.id)
            msg = await message.channel.send(embed=embed, view=view)
            
            # تمرير كائن الرسالة للكلاس للتحكم به عند انتهاء الوقت
            view.message_obj = msg

async def setup(bot):
    await bot.add_cog(ButtonGameCog(bot))