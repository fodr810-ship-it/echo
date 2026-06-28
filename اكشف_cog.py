import discord
from discord.ext import commands
import asyncio
import random

# نظام حفظ النقاط
points_db = {}

# قائمة كلمات الرصيد والاقتصاد
ECONOMY_WORDS = [
    "استثمار", "اقتصاد", "مليونير", "ميزانية", 
    "بورصة", "ارباح", "تجارة", "تمويل", 
    "رصيد", "حوالة", "سيولة", "ثروة"
]

class RevealWordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = set()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        if message.content == "اكشف":
            if message.channel.id in self.active_channels:
                await message.channel.send("⏳ فيه لعبة شغالة حالياً في هذا الروم، انتظر تخلص!")
                return
                
            self.active_channels.add(message.channel.id)
            
            word = random.choice(ECONOMY_WORDS)
            hidden_word = ["_" for _ in word]
            
            # إنشاء أرقام تمثل أماكن الحروف، ثم لخبطتها ليكون الكشف عشوائي
            hidden_indices = list(range(len(word)))
            random.shuffle(hidden_indices) 
            
            embed = discord.Embed(
                title="🔍 لعبة اكشف الكلمة",
                description=f"الكلمة: `{' '.join(hidden_word)}`\n\nأول شخص يكتب الكلمة كاملة هو الفائز!",
                color=discord.Color.blurple()
            )
            game_msg = await message.channel.send(embed=embed)
            
            async def reveal_loop():
                try:
                    # اللوب بيشتغل كل ثانيتين، ويوقف إذا بقى حرف واحد فقط (عشان ما يحلها البوت)
                    while len(hidden_indices) > 1:
                        await asyncio.sleep(2)
                        
                        # سحب حرف عشوائي من القائمة الملخبطة وكشفه
                        idx = hidden_indices.pop()
                        hidden_word[idx] = word[idx]
                        
                        embed.description = f"الكلمة: `{' '.join(hidden_word)}`\n\nأول شخص يكتب الكلمة كاملة هو الفائز!"
                        await game_msg.edit(embed=embed)
                except asyncio.CancelledError:
                    pass

            # تشغيل وظيفة كشف الحروف في الخلفية
            reveal_task = asyncio.create_task(reveal_loop())
            
            def check_answer(m):
                return m.channel == message.channel and m.content.strip() == word and not m.author.bot

            try:
                # ننتظر 30 ثانية للإجابة
                winner_msg = await self.bot.wait_for('message', check=check_answer, timeout=30.0)
                
                # نوقف اللوب حق التعديل لأن فيه شخص فاز
                reveal_task.cancel()
                
                user_id = str(winner_msg.author.id)
                points_db[user_id] = points_db.get(user_id, 0) + 1
                
                win_embed = discord.Embed(
                    title="🎉 عندنا بطل!",
                    description=f"الأسطورة {winner_msg.author.mention} عرف الكلمة أول واحد!\nالكلمة كانت: **{word}**",
                    color=discord.Color.green()
                )
                
                view = discord.ui.View()
                points_btn = discord.ui.Button(
                    label=f"رصيد نقاطك: {points_db[user_id]}", 
                    style=discord.ButtonStyle.success, 
                    disabled=True
                )
                view.add_item(points_btn)
                
                await message.channel.send(embed=win_embed, view=view)

            except asyncio.TimeoutError:
                reveal_task.cancel()
                timeout_embed = discord.Embed(
                    title="⏳ انتهى الوقت!",
                    description=f"محد قدر يكتشف الكلمة في الوقت المحدد.\nالكلمة كانت: **{word}**",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=timeout_embed)
                
            finally:
                self.active_channels.remove(message.channel.id)

async def setup(bot):
    await bot.add_cog(RevealWordCog(bot))