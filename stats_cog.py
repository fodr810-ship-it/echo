import discord
from discord.ext import commands
import os
import sys

class BotControlView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None) # الأزرار لن تنتهي صلاحيتها
        self.bot = bot
        self.cog = None  # سيتم ربط الكوج هنا عند إرسال الأمر

    # 1. زر تحديث البيانات
    @discord.ui.button(label="🔄 تحديث الإحصائيات", style=discord.ButtonStyle.blurple, custom_id="btn_refresh")
    async def refresh_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.cog:
            embed = await self.cog.get_stats_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("❌ حدث خطأ أثناء تحديث البيانات.", ephemeral=True)

    # 2. زر إعادة التشغيل
    @discord.ui.button(label="🔁 إعادة تشغيل", style=discord.ButtonStyle.grey, custom_id="btn_restart")
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("❌ هذا الأمر مخصص لصاحب البوت فقط!", ephemeral=True)
            return

        await interaction.response.send_message("🔄 جاري إعادة تشغيل البوت...", ephemeral=True)
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

    # 3. زر إيقاف التشغيل
    @discord.ui.button(label="🛑 إيقاف التشغيل", style=discord.ButtonStyle.red, custom_id="btn_shutdown")
    async def shutdown_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("❌ هذا الأمر مخصص لصاحب البوت فقط!", ephemeral=True)
            return

        await interaction.response.send_message("🛑 تم إيقاف البوت بنجاح.", ephemeral=True)
        await self.bot.close()


class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # دالة بناء الإمبيد الفعلي
    async def get_stats_embed(self) -> discord.Embed:
        # إحصائيات السيرفرات والأعضاء
        guilds_count = len(self.bot.guilds)
        users_count = sum(guild.member_count for guild in self.bot.guilds if guild.member_count)
        
        # إحصائيات البنية التحتية (أوامر وكوجات)
        commands_count = len(self.bot.commands)
        cogs_count = len(self.bot.cogs)
        
        # استخراج أسماء جميع الكوجات المحملة وتنسيقها
        loaded_cogs = [cog for cog in self.bot.cogs.keys()]
        if loaded_cogs:
            cogs_text = "، ".join([f"`{cog}`" for cog in loaded_cogs])
        else:
            cogs_text = "`لا يوجد كوجات محملة`"

        embed = discord.Embed(
            title="📊 لوحة تحكم وإحصائيات البوت",
            color=discord.Color.dark_theme(), 
        )
        
        # إحصائيات عامة
        embed.add_field(name="🌐 السيرفرات", value=f"`{guilds_count}` سيرفر", inline=True)
        embed.add_field(name="👥 المستخدمين", value=f"`{users_count}` مستخدم", inline=True)
        embed.add_field(name="⚡ سرعة الاستجابة", value=f"`{round(self.bot.latency * 1000)}ms`", inline=True)
        
        embed.add_field(name="═══ معلومات البنية والنظام ═══", value="", inline=False)
        
        # إحصائيات النظام الفعلية
        embed.add_field(name="⚙️ إجمالي الأوامر", value=f"`{commands_count}` أمر", inline=True)
        embed.add_field(name="📁 عدد الملفات (Cogs)", value=f"`{cogs_count}` ملف", inline=True)
        
        # عرض أسماء الكوجات
        embed.add_field(name="🧩 الكوجات المحملة حالياً", value=cogs_text, inline=False)
        
        embed.set_footer(text="استخدم الأزرار بالأسفل للتحكم التام")
        return embed

    @commands.command(name="احصاء", aliases=["stats", "الاحصائيات"])
    async def stats_command(self, ctx: commands.Context):
        embed = await self.get_stats_embed()
        
        view = BotControlView(self.bot)
        view.cog = self  
        
        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(StatsCog(bot))