import discord
from discord.ext import commands
import random

# نظام نقاط مبسط (تقدر تربطه بـ SQLite أو JSON اللي تستخدمها في بوتك)
points_db = {}

class FastButtonGame20(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30.0) 
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
        
        # تعطيل كل الـ 20 زر بعد الفوز
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        
        # إضافة النقاط
        user_id = str(interaction.user.id)
        points_db[user_id] = points_db.get(user_id, 0) + 1
        current_points = points_db[user_id]
        
        # إمبد الفوز
        win_embed = discord.Embed(
            title="🎉 مبروك عندنا فائز!",
            description=f"أسرع واحد صاد الزر هو {interaction.user.mention} 🏆",
            color=discord.Color.gold()
        )
        
        # زر عرض النقاط
        points_view = discord.ui.View()
        points_btn = discord.ui.Button(
            label=f"نقاطك: {current_points}", 
            style=discord.ButtonStyle.primary, 
            disabled=True
        )
        points_view.add_item(points_btn)
        
        await interaction.response.send_message(embed=win_embed, view=points_view)
        self.stop()

    async def wrong_answer(self, interaction: discord.Interaction):
        await interaction.response.send_message("خطأ! ركز على الزر المنور 🎯", ephemeral=True)


class ButtonGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        if message.content == "زر":
            embed = discord.Embed(
                title="🎮 لعبة صيد الزر",
                description="أمامك 20 زر، أسرع واحد يضغط على الزر المنوّر (🎯 الأخضر) هو الفائز!",
                color=discord.Color.blurple()
            )
            
            view = FastButtonGame20()
            await message.channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ButtonGameCog(bot))