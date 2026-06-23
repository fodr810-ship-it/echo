import discord
from discord.ext import commands
import random
import asyncio

class HideAndSeekView(discord.ui.View):
    def __init__(self, bot_choice, ctx):
        super().__init__(timeout=30.0)  # مدة اللعبة 30 ثانية
        self.bot_choice = bot_choice
        self.ctx = ctx
        self.winner = None

    async def check_choice(self, interaction: discord.Interaction, choice: str):
        # التحقق إذا انتهت اللعبة مسبقاً
        if self.winner:
            await interaction.response.send_message("❌ انتهت اللعبة بالفعل وصيدنا البوت!", ephemeral=True)
            return

        if choice == self.bot_choice:
            self.winner = interaction.user
            self.stop() # إيقاف الأزرار
            
            # تعديل الرسالة لإظهار الفائز وتعطيل الأزرار
            for child in self.children:
                child.disabled = True
                if child.label == choice:
                    child.style = discord.ButtonStyle.success # زر الفوز أخضر
                else:
                    child.style = discord.ButtonStyle.secondary

            await interaction.response.edit_message(view=self)
            await self.ctx.send(f"🎉 **كفوووو!** {interaction.user.mention} لقى البوت! البوت كان متخبي في: **{self.bot_choice}** 🎯")
        else:
            await interaction.response.send_message(f"❌ مالقيت شي في **{choice}**! دور في مكان ثاني بسرعة!", ephemeral=True)

    @discord.ui.button(label="خلف الشجرة 🌳", style=discord.ButtonStyle.primary)
    async def tree(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_choice(interaction, "خلف الشجرة 🌳")

    @discord.ui.button(label="تحت السرير 🛏️", style=discord.ButtonStyle.primary)
    async def bed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_choice(interaction, "تحت السرير 🛏️")

    @discord.ui.button(label="داخل الخزانة 🚪", style=discord.ButtonStyle.primary)
    async def closet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_choice(interaction, "داخل الخزانة 🚪")

    @discord.ui.button(label="وراء الستارة 🪟", style=discord.ButtonStyle.primary)
    async def curtain(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_choice(interaction, "وراء الستارة 🪟")

    async def on_timeout(self):
        if not self.winner:
            for child in self.children:
                child.disabled = True
            try:
                await self.ctx.send(f"⏰ **انتهى الوقت!** البوت فاز عليكم وما أحد لقى مكانه هههههه! كان متخبي في: **{self.bot_choice}** 🏆")
            except:
                pass

class HideAndSeekCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="غميضة", aliases=["غميضه", "hide"])
    async def hide_game(self, ctx):
        """يبدأ لعبة غميضة في السيرفر"""
        places = ["خلف الشجرة 🌳", "تحت السرير 🛏️", "داخل الخزانة 🚪", "وراء الستارة 🪟"]
        bot_choice = random.choice(places)

        embed = discord.Embed(
            title="🙈 لعبة الغميضة بدأت! 🙈",
            description="البوت تغبى الحين في مكان بالسيرفر!\nمعاكم **30 ثانية** عشان تحزرون وين مكانه، اضغطوا على الأزرار تحت لتوقع المكان 👇",
            color=discord.Color.orange()
        )
        embed.set_footer(text="أول لاعب يضغط على المكان الصح هو الفائز!")

        view = HideAndSeekView(bot_choice, ctx)
        # إرسال الرسالة مع الأزرار
        msg = await ctx.send(embed=embed, view=view)
        
        # ربط الـ view بالرسالة عشان التايم أوت يعدلها لو انتهى الوقت
        view.message = msg

async def setup(bot):
    await bot.load_extension("hide_and_seek_cog") # خطوة اختيارية للتأكيد
    await bot.add_cog(HideAndSeekCog(bot))
    print("✅ تم تحميل كوج لعبة الغميضة بنجاح!")