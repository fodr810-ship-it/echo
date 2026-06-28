import discord
from discord.ext import commands
import random

# نظام نقاط مبسط في الذاكرة (استبدله بقاعدة البيانات الخاصة بك مثل SQLite أو JSON)
points_db = {}

class FastButtonGame(discord.ui.View):
    def __init__(self):
        # مدة اللعبة 60 ثانية إذا محد ضغط
        super().__init__(timeout=30.0) 
        self.winner = None
        
        # تحديد موقع الزر الفائز عشوائياً بين 3 أزرار
        correct_btn_index = random.randint(0, 2)
        
        for i in range(3):
            if i == correct_btn_index:
                # الزر "المنور" (الأخضر)
                btn = discord.ui.Button(
                    label="اضغطني!", 
                    style=discord.ButtonStyle.success, 
                    custom_id=f"correct_{i}"
                )
                btn.callback = self.correct_answer
            else:
                # الأزرار العادية التمويهية (الرمادية)
                btn = discord.ui.Button(
                    label="مو هذا", 
                    style=discord.ButtonStyle.secondary, 
                    custom_id=f"wrong_{i}"
                )
                btn.callback = self.wrong_answer
            
            self.add_item(btn)

    async def correct_answer(self, interaction: discord.Interaction):
        # التأكد إن ما فيه أحد فاز قبله في نفس اللحظة
        if self.winner:
            return 
            
        self.winner = interaction.user
        
        # تعطيل كل الأزرار في الرسالة الأصلية بعد الفوز
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        
        # إضافة وتحديث النقاط
        user_id = str(interaction.user.id)
        points_db[user_id] = points_db.get(user_id, 0) + 1
        current_points = points_db[user_id]
        
        # إمبد إعلان الفائز
        win_embed = discord.Embed(
            title="🎉 مبروك عندنا فائز!",
            description=f"أسرع واحد ضغط الزر هو {interaction.user.mention} 🏆",
            color=discord.Color.gold()
        )
        
        # view جديد لزر النقاط (يكون معطل فقط للعرض)
        points_view = discord.ui.View()
        points_btn = discord.ui.Button(
            label=f"نقاطك: {current_points}", 
            style=discord.ButtonStyle.primary, 
            disabled=True
        )
        points_view.add_item(points_btn)
        
        # إرسال رسالة الفوز مع زر النقاط
        await interaction.response.send_message(embed=win_embed, view=points_view)
        self.stop()

    async def wrong_answer(self, interaction: discord.Interaction):
        # رد مخفي للشخص اللي يضغط الزر الغلط
        await interaction.response.send_message("خطأ! مو هذا الزر المنور، ركز وحاول مرة ثانية.", ephemeral=True)


class ButtonGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # تجاهل رسائل البوتات عشان ما يصير سبام
        if message.author.bot:
            return
            
        # التحقق من الكلمة المطلوبة
        if message.content == "زر":
            embed = discord.Embed(
                title="🎮 لعبة أسرع زر",
                description="أسرع واحد يضغط على الزر المنوّر (الأخضر) هو الفائز!",
                color=discord.Color.blurple()
            )
            
            view = FastButtonGame()
            await message.channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ButtonGameCog(bot))