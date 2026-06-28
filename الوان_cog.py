import discord
from discord.ext import commands
import random

# نظام حفظ النقاط (استبدله بقاعدة البيانات الخاصة بك)
points_db = {}

# قاموس يحتوي على 27 لون مع الإيموجي المعبر واللون الدقيق للإمبد
COLORS_DICT = {
    "أحمر": ("🟥", discord.Color.red()),
    "أزرق": ("🟦", discord.Color.blue()),
    "أخضر": ("🟩", discord.Color.green()),
    "أصفر": ("🟨", discord.Color.gold()),
    "بنفسجي": ("🟪", discord.Color.purple()),
    "برتقالي": ("🟧", discord.Color.orange()),
    "أسود": ("⬛", discord.Color.default()),
    "أبيض": ("⬜", discord.Color.light_grey()),
    "بني": ("🟫", discord.Color.dark_theme()),
    "سماوي": ("🩵", discord.Color.from_rgb(135, 206, 235)),
    "وردي": ("🩷", discord.Color.from_rgb(255, 192, 203)),
    "رمادي": ("🩶", discord.Color.from_rgb(128, 128, 128)),
    "عنابي": ("🍷", discord.Color.from_rgb(128, 0, 0)),
    "كحلي": ("🌌", discord.Color.from_rgb(0, 0, 128)),
    "فيروزي": ("💎", discord.Color.from_rgb(64, 224, 208)),
    "زيتوني": ("🫒", discord.Color.from_rgb(128, 128, 0)),
    "ذهبي": ("🪙", discord.Color.from_rgb(255, 215, 0)),
    "فضي": ("🥈", discord.Color.from_rgb(192, 192, 192)),
    "برونزي": ("🥉", discord.Color.from_rgb(205, 127, 50)),
    "ليموني": ("🍋", discord.Color.from_rgb(255, 250, 205)),
    "بطيخي": ("🍉", discord.Color.from_rgb(255, 107, 129)),
    "مشمشي": ("🍑", discord.Color.from_rgb(255, 218, 185)),
    "بيج": ("🐪", discord.Color.from_rgb(245, 245, 220)),
    "أخضر فاتح": ("🥝", discord.Color.from_rgb(144, 238, 144)),
    "نيلي": ("🧿", discord.Color.from_rgb(75, 0, 130)),
    "وردي غامق": ("🌺", discord.Color.from_rgb(255, 20, 147)),
    "خوخي": ("🥭", discord.Color.from_rgb(255, 204, 153))
}

class ColorGameView(discord.ui.View):
    def __init__(self, correct_name, options):
        super().__init__(timeout=30.0) 
        self.correct_name = correct_name
        self.winner = None
        
        # إنشاء 4 أزرار بناءً على الخيارات العشوائية المسحوبة
        for option in options:
            btn = discord.ui.Button(
                label=option,
                style=discord.ButtonStyle.primary,
                custom_id=f"color_{option}" 
            )
            btn.callback = self.check_answer
            self.add_item(btn)

    async def check_answer(self, interaction: discord.Interaction):
        if self.winner:
            return

        clicked_color = interaction.data["custom_id"].replace("color_", "")
        
        if clicked_color == self.correct_name:
            self.winner = interaction.user
            
            # تعطيل جميع الأزرار وتلوين الزر الصحيح بالأخضر والباقي رمادي
            for child in self.children:
                child.disabled = True
                if child.label == self.correct_name:
                    child.style = discord.ButtonStyle.success
                else:
                    child.style = discord.ButtonStyle.secondary
            
            await interaction.message.edit(view=self)
            
            # إضافة وتحديث النقاط
            user_id = str(interaction.user.id)
            points_db[user_id] = points_db.get(user_id, 0) + 1
            current_points = points_db[user_id]
            
            # إمبد الفوز
            win_embed = discord.Embed(
                title="🎉 إجابة صحيحة!",
                description=f"الأسطورة {interaction.user.mention} عرف اللون أول واحد! 🏆",
                color=discord.Color.green()
            )
            
            # زر عرض النقاط
            points_view = discord.ui.View()
            points_btn = discord.ui.Button(
                label=f"رصيد نقاطك: {current_points}", 
                style=discord.ButtonStyle.success, 
                disabled=True
            )
            points_view.add_item(points_btn)
            
            await interaction.response.send_message(embed=win_embed, view=points_view)
            self.stop()
        else:
            await interaction.response.send_message("خطأ! مو هذا اللون ❌، ركز وحاول أسرع.", ephemeral=True)

class ColorGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        if message.content == "الوان":
            all_colors = list(COLORS_DICT.keys())
            
            # سحب 4 ألوان عشوائية بالكامل في كل مرة (الأزرار راح تتغير كل قيم)
            options = random.sample(all_colors, 4)
            
            # تحديد لون واحد فقط من الأربعة ليكون هو الإجابة الصحيحة
            correct_name = random.choice(options)
            correct_emoji, embed_color = COLORS_DICT[correct_name]
            
            # تجهيز الإمبد وعرض الإيموجي المعبر عن اللون
            embed = discord.Embed(
                title="🎨 لعبة الألوان",
                description=f"خمن وش هذا اللون بأسرع وقت؟\n\n# {correct_emoji}",
                color=embed_color
            )
            
            view = ColorGameView(correct_name, options)
            await message.channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ColorGameCog(bot))