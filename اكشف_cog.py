import discord
from discord.ext import commands
import asyncio
import random

# نظام حفظ النقاط المبسط (استبدله بقاعدة البيانات الخاصة بك)
points_db = {}

# قائمة الكلمات (كلمات عشوائية متعلقة بالرصيد العالي والاقتصاد)
ECONOMY_WORDS = [
    "استثمار", "اقتصاد", "مليونير", "ميزانية", 
    "بورصة", "ارباح", "تجارة", "تمويل", 
    "رصيد", "حوالة", "سيولة", "ثروة"
]

class RevealWordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # حفظ الرومات اللي فيها لعبة شغالة عشان ما تتداخل الألعاب
        self.active_channels = set()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        # الكلمة اللي تشغل اللعبة
        if message.content == "اكشف":
            # التأكد إن مافيه لعبة ثانية شغالة بنفس الروم
            if message.channel.id in self.active_channels:
                await message.channel.send("⏳ فيه لعبة شغالة حالياً في هذا الروم، انتظر تخلص!")
                return
                
            self.active_channels.add(message.channel.id)
            
            # اختيار كلمة عشوائية وإعداد الحروف المخفية
            word = random.choice(ECONOMY_WORDS)
            hidden_word = ["_" for _ in word]
            hidden_indices = list(range(len(word)))
            random.shuffle(hidden_indices) # لخبطة ترتيب الحروف عشان تنكشف بشكل عشوائي
            
            embed = discord.Embed(
                title="🔍 لعبة اكشف الكلمة",
                description=f"الكلمة: `{' '.join(hidden_word)}`\n\nأول شخص يكتب الكلمة كاملة هو الفائز!",
                color=discord.Color.blurple()
            )
            game_msg = await message.channel.send(embed=embed)
            
            # وظيفة (Task) تعمل في الخلفية لكشف الحروف كل 5 ثواني
            async def reveal_loop():
                try:
                    # يوقف كشف إذا بقى حرف واحد فقط
                    while len(hidden_indices) > 1:
                        await asyncio.sleep(5)
                        idx = hidden_indices.pop()
                        hidden_word[idx] = word[idx]
                        
                        embed.description = f"الكلمة: `{' '.join(hidden_word)}`\n\nأول شخص يكتب الكلمة كاملة هو الفائز!"
                        await game_msg.edit(embed=embed)
                except asyncio.CancelledError:
                    # يتم استدعاء هذا الخطأ عمداً عند إلغاء الوظيفة (مثلاً إذا فاز شخص)
                    pass

            # تشغيل وظيفة الكشف
            reveal_task = asyncio.create_task(reveal_loop())
            
            # دالة للتحقق من الرسائل الصحيحة (في نفس الروم + نفس الكلمة)
            def check_answer(m):
                return m.channel == message.channel and m.content.strip() == word and not m.author.bot

            try:
                # انتظار الإجابة الصحيحة لمدة 30 ثانية
                winner_msg = await self.bot.wait_for('message', check=check_answer, timeout=30.0)
                
                # إذا جاوب شخص، نوقف وظيفة كشف الحروف
                reveal_task.cancel()
                
                # إضافة النقاط للفائز
                user_id = str(winner_msg.author.id)
                points_db[user_id] = points_db.get(user_id, 0) + 1
                
                # إعداد إمبد الفوز
                win_embed = discord.Embed(
                    title="🎉 عندنا بطل!",
                    description=f"الأسطورة {winner_msg.author.mention} عرف الكلمة أول واحد!\nالكلمة كانت: **{word}**",
                    color=discord.Color.green()
                )
                
                # زر إظهار النقاط
                view = discord.ui.View()
                points_btn = discord.ui.Button(
                    label=f"رصيد نقاطك: {points_db[user_id]}", 
                    style=discord.ButtonStyle.success, 
                    disabled=True
                )
                view.add_item(points_btn)
                
                await message.channel.send(embed=win_embed, view=view)

            except asyncio.TimeoutError:
                # إذا خلصت الـ 30 ثانية ومحد جاوب
                reveal_task.cancel()
                timeout_embed = discord.Embed(
                    title="⏳ انتهى الوقت!",
                    description=f"محد قدر يكتشف الكلمة في الوقت المحدد.\nالكلمة كانت: **{word}**",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=timeout_embed)
                
            finally:
                # إزالة الروم من القائمة عشان يقدرون يلعبون مرة ثانية
                self.active_channels.remove(message.channel.id)

async def setup(bot):
    await bot.add_cog(RevealWordCog(bot))