import discord
from discord.ext import commands
import random
import asyncio
import aiosqlite
import time

class BankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_name = "bank_system.db"
        self.bot.loop.create_task(self.init_db())

    # 💾 إنشاء قاعدة البيانات وجداول اللاعبين والممتلكات تلقائياً
    async def init_db(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    cash INTEGER DEFAULT 500,
                    bank INTEGER DEFAULT 1000,
                    job TEXT DEFAULT 'عاطل',
                    last_daily INTEGER DEFAULT 0,
                    last_work INTEGER DEFAULT 0,
                    last_rob INTEGER DEFAULT 0,
                    shield_time INTEGER DEFAULT 0,
                    loan_amount INTEGER DEFAULT 0
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    user_id INTEGER,
                    item_name TEXT,
                    item_count INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, item_name)
                )
            """)
            await db.commit()

    # 🔍 دالة مساعدة لجلب بيانات اللاعب أو تسجيله لو كان جديداً
    async def get_user(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        "cash": row[1], "bank": row[2], "job": row[3],
                        "last_daily": row[4], "last_work": row[5], "last_rob": row[6],
                        "shield_time": row[7], "loan_amount": row[8]
                    }
                else:
                    await db.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
                    await db.commit()
                    return {"cash": 500, "bank": 1000, "job": "عاطل", "last_daily": 0, "last_work": 0, "last_rob": 0, "shield_time": 0, "loan_amount": 0}

    async def update_balance(self, user_id, amount, mode="cash"):
        async with aiosqlite.connect(self.db_name) as db:
            if mode == "cash":
                await db.execute("UPDATE users SET cash = cash + ? WHERE user_id = ?", (amount, user_id))
            else:
                await db.execute("UPDATE users SET bank = bank + ? WHERE user_id = ?", (amount, user_id))
            await db.commit()

    # ==========================================
    # 🏦 الأوامر العامة والاقتصادية
    # ==========================================

    @commands.command(name="رصيد", aliases=["الرصيد", "فلوسي"])
    async def balance(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        user = await self.get_user(target.id)
        embed = discord.Embed(title=f"🏦 كشف حساب | {target.name}", color=discord.Color.gold())
        embed.add_field(name="💵 كاش بجيبك:", value=f"`{user['cash']}` ريال", inline=False)
        embed.add_field(name="💳 في البنك:", value=f"`{user['bank']}` ريال", inline=False)
        embed.add_field(name="💼 الوظيفة الحالية:", value=f"`{user['job']}`", inline=False)
        if user['loan_amount'] > 0:
            embed.add_field(name="🚨 القرض المطلوب سداده:", value=f"`{user['loan_amount']}` ريال", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="راتب", aliases=["الوظائف", "عمل"])
    async def work(self, ctx):
        user = await self.get_user(ctx.author.id)
        current_time = int(time.time())
        if current_time - user["last_work"] < 3600:
            remaining = 3600 - (current_time - user["last_work"])
            return await ctx.send(f"❌ أنت تعبت اليوم! باقي لك `{remaining // 60}` دقيقة وتقدر تداوم للراتب الجاي.")
        
        jobs = ["مهندس سيرفرات", "ستريمر محترف", "مدير بنك", "مبرمج بايثون", "صانع محتوى"]
        chosen_job = random.choice(jobs)
        salary = random.randint(300, 800)
        
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE users SET cash = cash + ?, job = ?, last_work = ? WHERE user_id = ?", (salary, chosen_job, current_time, ctx.author.id))
            await db.commit()
            
        await ctx.send(f"💼 اشتغلت كـ **{chosen_job}** وعطوك راتب قيمته **{salary}** ريال! 💵")

    @commands.command(name="هدية", aliases=["بخشيش"])
    async def gift(self, ctx):
        user = await self.get_user(ctx.author.id)
        current_time = int(time.time())
        if current_time - user["last_daily"] < 86400:
            return await ctx.send("❌ أخذت هديتك اليومية خلاص! تعال بكرة.")
            
        gift_amount = random.randint(500, 1500)
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE users SET cash = cash + ?, last_daily = ? WHERE user_id = ?", (gift_amount, current_time, ctx.author.id))
            await db.commit()
        await ctx.send(f"🎁 مبروك أخذت الهدية اليومية / البخشيش بقيمة **{gift_amount}** ريال!")

    @commands.command(name="تحويل")
    async def transfer(self, ctx, member: discord.Member, amount: int):
        if amount <= 0: return await ctx.send("❌ حط مبلغ صاحي!")
        user = await self.get_user(ctx.author.id)
        if user["cash"] < amount: return await ctx.send("❌ ما عندك كاش كافي في جيبك للتحويل!")
        
        await self.update_balance(ctx.author.id, -amount, "cash")
        await self.update_balance(member.id, amount, "cash")
        await ctx.send(f"💸 تم تحويل **{amount}** ريال بنجاح من {ctx.author.mention} إلى {member.mention}!")

    @commands.command(name="حماية")
    async def buy_shield(self, ctx):
        user = await self.get_user(ctx.author.id)
        cost = 1000
        if user["cash"] < cost: return await ctx.send("❌ قيمة الحماية ضد الحرامية 1000 ريال كاش، ما معك!")
        
        shield_expiry = int(time.time()) + 86400 # حماية لمدة 24 ساعة
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE users SET cash = cash - ?, shield_time = ? WHERE user_id = ?", (cost, shield_expiry, ctx.author.id))
            await db.commit()
        await ctx.send("🛡️ تم شراء حماية (درع) فعال لمدة 24 ساعة ضد عمليات النهب والسرقة!")

    @commands.command(name="نهب", aliases=["حرامية", "سرقة"])
    async def rob(self, ctx, member: discord.Member):
        if member.id == ctx.author.id: return await ctx.send("❌ بتسرق نفسك؟ صاحي أنت؟")
        attacker = await self.get_user(ctx.author.id)
        victim = await self.get_user(member.id)
        
        current_time = int(time.time())
        if current_time - attacker["last_rob"] < 1800:
            return await ctx.send("🚨 الشرطة تراقبك! انتظر 30 دقيقة قبل عملية النهب الجاية.")
            
        if victim["shield_time"] > current_time:
            return await ctx.send(f"🛡️ فشلت السرقة! {member.mention} مفعل نظام الحماية والدرع الحين.")
            
        if victim["cash"] < 200:
            return await ctx.send("❌ الضحية مطفر وما معاه كاش يستاهل تسرقه.")

        # نسبة النجاح 50%
        if random.choice([True, False]):
            stolen = random.randint(100, int(victim["cash"] * 0.5))
            await self.update_balance(ctx.author.id, stolen, "cash")
            await self.update_balance(member.id, -stolen, "cash")
            await ctx.send(f"🥷 نجحت عملية النهب! {ctx.author.mention} سرق من مخبأ {member.mention} مبلغ **{stolen}** ريال!")
        else:
            penalty = 300
            await self.update_balance(ctx.author.id, -penalty, "cash")
            await ctx.send(f"🚔 صادك ساهر والشرطة! {ctx.author.mention} فشل بالسرقة وتم تغريمه **{penalty}** ريال للبلدية!")

        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE users SET last_rob = ? WHERE user_id = ?", (current_time, ctx.author.id))
            await db.commit()

    @commands.command(name="قرض")
    async def take_loan(self, ctx, amount: int):
        if amount < 1000 or amount > 5000: return await ctx.send("❌ تقدر تاخذ قرض من البنك بين 1000 إلى 5000 ريال فقط.")
        user = await self.get_user(ctx.author.id)
        if user["loan_amount"] > 0: return await ctx.send("❌ عليك قرض قديم ما سددته للحين! سدده أول.")
        
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE users SET bank = bank + ?, loan_amount = ? WHERE user_id = ?", (amount, int(amount * 1.2), ctx.author.id))
            await db.commit()
        await ctx.send(f"🏦 وافق البنك على قرضك وتم إيداع **{amount}** ريال بحسابك! (المطلوب سداده مع الفوائد: **{int(amount * 1.2)}**).")

    @commands.command(name="تسديد")
    async def pay_loan(self, ctx):
        user = await self.get_user(ctx.author.id)
        if user["loan_amount"] == 0: return await ctx.send("❌ ما عليك أي قروض للبنك حالياً.")
        if user["cash"] < user["loan_amount"]: return await ctx.send(f"❌ ما عندك كاش كافي بجيبك لسداد القرض البالغ `{user['loan_amount']}` ريال.")
        
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE users SET cash = cash - user['loan_amount'], loan_amount = 0 WHERE user_id = ?", (ctx.author.id,))
            await db.commit()
        await ctx.send("🎉 كفو! تم تسديد القرض بالكامل للبنك وتصفير سجلاتك الائتمانية.")

    @commands.command(name="توب")
    async def leaderboard(self, ctx):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT user_id, (cash + bank) as total FROM users ORDER BY total DESC LIMIT 5") as cursor:
                rows = await cursor.fetchall()
                
        embed = discord.Embed(title="🏆 قائمة أغنى 5 هوامير في السيرفر", color=discord.Color.purple())
        for index, row in enumerate(rows, 1):
            user = self.bot.get_user(row[0])
            name = user.name if user else f"عضو غامض ({row[0]})"
            embed.add_field(name=f"{index}. {name}", value=f"إجمالي الثروة: `{row[1]}` ريال", inline=False)
        await ctx.send(embed=embed)

    # ==========================================
    # 🕹️ ألعاب كسب وثروات الأموال (Games & Gambling)
    # ==========================================

    @commands.command(name="سلوت", aliases=["حظ", "سلوتس"])
    async def slot(self, ctx, bet: int):
        if bet <= 0: return
        user = await self.get_user(ctx.author.id)
        if user["cash"] < bet: return await ctx.send("❌ الكاش اللي معك ما يغطي الرهان!")

        emojis = ["🍎", "🍊", "🍇", "🍒", "💎"]
        slot1 = random.choice(emojis)
        slot2 = random.choice(emojis)
        slot3 = random.choice(emojis)

        msg = await ctx.send(f"🎰 | 🟩 | 🟩 | 🟩")
        await asyncio.sleep(1)
        await msg.edit(content=f"🎰 | {slot1} | 🟩 | 🟩")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"🎰 | {slot1} | {slot2} | 🟩")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"🎰 | {slot1} | {slot2} | {slot3}")

        if slot1 == slot2 == slot3:
            win = bet * 5
            await self.update_balance(ctx.author.id, win, "cash")
            await ctx.send(f"🎉 **الضربة الكبرى المدوية!** تطابقت الأشكال وفزت بـ **{win}** ريال! 💎")
        elif slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
            win = bet * 2
            await self.update_balance(ctx.author.id, win, "cash")
            await ctx.send(f"💵 **فوز متوسط!** شكلين تطابقوا وفزت بـ **{win}** ريال!")
        else:
            await self.update_balance(ctx.author.id, -bet, "cash")
            await ctx.send(f"😭 راحت عليك الفلوس! الحظ ما حالفك هالمرة وخسرت رهانك.")

    @commands.command(name="نرد")
    async def dice_game(self, ctx, bet: int, guess: int):
        if guess < 1 or guess > 6: return await ctx.send("❌ النرد من 1 إلى 6 فقط!")
        user = await self.get_user(ctx.author.id)
        if user["cash"] < bet: return await ctx.send("❌ ما عندك كاش للعب.")

        bot_roll = random.randint(1, 6)
        await ctx.send(f"🎲 رمينا النرد وطلع الرقم: **{bot_roll}**")

        if guess == bot_roll:
            win = bet * 3
            await self.update_balance(ctx.author.id, win, "cash")
            await ctx.send(f"🎯 **توقع في منتصف الجبهة!** حزرت الرقم وفزت بـ **{win}** ريال!")
        else:
            await self.update_balance(ctx.author.id, -bet, "cash")
            await ctx.send("❌ حظ أوفر المرة الجاية، خسرت الرهان.")

    @commands.command(name="استثمار", aliases=["تداول"])
    async def invest(self, ctx, amount: int):
        user = await self.get_user(ctx.author.id)
        if user["cash"] < amount: return await ctx.send("❌ ما معك هالمبلغ كاش!")
        
        await ctx.send("📈 جاري تحليل سوق الأسهم والعملات الرقمية والمخاطرة...")
        await asyncio.sleep(2)
        
        outcome = random.choice(["ربح_قوي", "ربح_خفيف", "خسارة_كلية", "خسارة_جزئية"])
        if outcome == "ربح_قوي":
            profit = int(amount * 1.5)
            await self.update_balance(ctx.author.id, profit, "cash")
            await ctx.send(f"🚀 السوق طار فوق! سويت استثمار أسطوري وربحت **{profit}** ريال!")
        elif outcome == "ربح_خفيف":
            profit = int(amount * 0.2)
            await self.update_balance(ctx.author.id, profit, "cash")
            await ctx.send(f"🟢 صعود خفيف بالسوق، ربحت فايدة بسيطة **{profit}** ريال.")
        elif outcome == "خسارة_جزئية":
            loss = int(amount * 0.4)
            await self.update_balance(ctx.author.id, -loss, "cash")
            await ctx.send(f"📉 هبط السوق فجأة وخسرت من محفظتك الاستثمارية **{loss}** ريال.")
        else:
            await self.update_balance(ctx.author.id, -amount, "cash")
            await ctx.send("💥 انهار السوق والشركة أعلنت إفلاسها! خسرت كامل مبلغ الاستثمار 😭")

async def setup(bot):
    await bot.add_cog(BankCog(bot))
    print("✅ تم تحميل نظام وألعاب البنك الاقتصادي بنجاح وبدء قاعدة البيانات الحديثة!")