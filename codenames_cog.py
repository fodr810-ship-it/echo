import discord
from discord.ext import commands
import random

class CodenamesGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command(name="start_codenames")
    async def start_codenames(self, ctx):
        self.games[ctx.channel.id] = {
            "players": [], "turn": "blue", "status": "playing",
            "words": [], "colors": [], "blue_score": 0, "red_score": 0,
            "blue_team": [], "red_team": [], "blue_leader": None, "red_leader": None
        }
        await ctx.send("🕵️ **لعبة كود نيمز!** بانتظار 4 لاعبين للانضمام:", view=JoinView(self))

class JoinView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="انضم للعبة", style=discord.ButtonStyle.primary)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        game = self.cog.games[interaction.channel.id]
        
        if interaction.user not in game["players"]:
            game["players"].append(interaction.user)
            await interaction.response.send_message(f"تم الانضمام! ({len(game['players'])}/4)", ephemeral=True)
            
            if len(game["players"]) == 4:
                # إيقاف زر الانضمام بعد اكتمال العدد
                for child in self.children:
                    child.disabled = True
                await interaction.message.edit(view=self)
                await self.start_match(interaction)
        else:
            await interaction.response.send_message("أنت منضم بالفعل!", ephemeral=True)

    async def start_match(self, interaction):
        game = self.cog.games[interaction.channel.id]
        random.shuffle(game["players"])
        game["blue_team"] = [game["players"][0], game["players"][1]]
        game["red_team"] = [game["players"][2], game["players"][3]]
        game["blue_leader"], game["red_leader"] = game["players"][0], game["players"][2]
        
        words = ["قمر", "شمس", "سيارة", "طيارة", "مفتاح", "باب", "بحر", "رمل", "جبل", "ثلج", "نار", "ماء", "سيف", "درع", "حصان", "فارس", "ملك", "قلعة", "ذهب", "فضة", "شجرة", "وردة", "عصفور", "نسر", "أسد"]
        game["words"] = random.sample(words, 25)
        game["colors"] = ["blue"]*11 + ["red"]*11 + ["black"]*3
        random.shuffle(game["colors"])

        # حماية الكود من الإيقاف في حال كان الخاص مغلقاً عند أحد القادة
        try:
            for leader in [game["blue_leader"], game["red_leader"]]:
                team = "الأزرق 🔵" if leader == game["blue_leader"] else "الأحمر 🔴"
                target_color = 'blue' if team == 'الأزرق 🔵' else 'red'
                leader_words = [game['words'][i] for i, c in enumerate(game['colors']) if c == target_color]
                
                await leader.send(f"أنت قائد الفريق {team}.\n**كلماتك هي:** {', '.join(leader_words)}")
                await leader.send("استخدم هذا الزر لتقديم التلميح في الروم العام:", view=HintView(self.cog, interaction.channel.id))
        except discord.Forbidden:
            await interaction.channel.send("⚠️ **تنبيه:** أحد القادة مقفل الخاص! لا يمكن إرسال الكلمات السرية، يرجى فتح الخاص وإعادة اللعبة.")
            return

        for member in game["players"]:
            if member not in [game["blue_leader"], game["red_leader"]]:
                try:
                    team = "الأزرق 🔵" if member in game['blue_team'] else "الأحمر 🔴"
                    await member.send(f"أنت في الفريق {team}. انتظر التلميح في الروم العام!")
                except discord.Forbidden:
                    pass
        
        await interaction.channel.send("🚀 **بدأت اللعبة!** الدور الآن للفريق الأزرق.", view=GameBoardView(self.cog, interaction.channel.id))

class HintView(discord.ui.View):
    def __init__(self, cog, cid):
        super().__init__(timeout=None)
        self.cog, self.cid = cog, cid
        
    @discord.ui.button(label="تقديم تلميح", style=discord.ButtonStyle.success)
    async def h(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.send_modal(HintModal(self.cog, self.cid))

class HintModal(discord.ui.Modal, title='تلميح القائد'):
    hint = discord.ui.TextInput(label='التلميح', placeholder='اكتب تلميحك هنا')
    count = discord.ui.TextInput(label='عدد الكلمات', placeholder='رقم')
    
    def __init__(self, c, cid): 
        super().__init__()
        self.c, self.cid = c, cid
        
    async def on_submit(self, i):
        channel = i.client.get_channel(self.cid)
        if channel:
            await channel.send(f"📢 **تلميح القائد:** {self.hint.value} (عدد الكلمات: {self.count.value})")
        await i.response.send_message("تم إرسال التلميح بنجاح!", ephemeral=True)

class GameBoardView(discord.ui.View):
    def __init__(self, cog, cid):
        super().__init__(timeout=None)
        self.cog, self.cid = cog, cid
        for i in range(25):
            self.add_item(WordButton(i, cog.games[cid]["words"][i], cog, cid))

class WordButton(discord.ui.Button):
    def __init__(self, idx, lbl, cog, cid):
        # استخدام row=idx // 5 ضروري لترتيب الـ 25 زر كشبكة 5 في 5
        super().__init__(label=lbl, style=discord.ButtonStyle.secondary, custom_id=f"btn_{cid}_{idx}", row=idx // 5)
        
        # الخطأ كان هنا (فك حزم المتغيرات بشكل خاطئ أدى لإيقاف إرسال الأزرار)
        self.idx = idx
        self.cog = cog
        self.cid = cid

    async def callback(self, i: discord.Interaction):
        g = self.cog.games[self.cid]
        
        if (g["turn"] == "blue" and i.user not in g["blue_team"]) or \
           (g["turn"] == "red" and i.user not in g["red_team"]):
            return await i.response.send_message("ليس دور فريقك الآن!", ephemeral=True)
            
        color = g["colors"][self.idx]
        self.disabled = True
        
        if color == "black":
            self.style = discord.ButtonStyle.danger
            await i.response.edit_message(content=f"💀 **خسارة!** الفريق {g['turn'].upper()} ضغط على الكلمة القاتلة!", view=self.view)
            return
        
        # تغيير لون الزر حسب اللون الفعلي
        self.style = discord.ButtonStyle.primary if color == "blue" else discord.ButtonStyle.danger
        
        # نقل الدور للفريق الآخر
        g["turn"] = "red" if g["turn"] == "blue" else "blue"
        await i.response.edit_message(content=f"الدور الحالي: **الفريق {'الأحمر 🔴' if g['turn'] == 'red' else 'الأزرق 🔵'}**", view=self.view)

async def setup(bot): 
    await bot.add_cog(CodenamesGame(bot))