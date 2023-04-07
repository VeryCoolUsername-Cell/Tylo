import discord
from discord.ext import commands
import aiosqlite

async def add_inventory(db,user:int,amount:int,item:str):
        await db.execute("CREATE TABLE IF NOT EXISTS inventory(user,item,amount)")
        the = await db.execute("SELECT amount FROM inventory WHERE user = ? AND item = ?",(user,item))
        the = await the.fetchone()
        if the is None:
            await db.execute("INSERT OR IGNORE INTO inventory VALUES(?,?,?)",(user,item,amount))
            await db.commit()
        else:
            await db.execute("UPDATE inventory SET amount = amount + ? WHERE user = ? AND item = ?",(amount,user,item))
            await db.commit()

async def see_inventory(db,user:int,name:str):
    the = await db.execute("SELECT item,amount FROM inventory WHERE user = ?",(user,))
    the = await the.fetchall()
    if len(the) == 0:
        await db.commit()
        return discord.Embed(title=f"{name} Inventory",description="It seems like the user has nothing.")
    embed = discord.Embed(title=f"{name}",description="\n")
    for item,amount in the:
        embed.description += f"`x{amount}` {item}\n"
    await db.commit()
    return embed

async def buy(db,user:id,amount:int,item:str):
        cash = await db.execute("SELECT cash FROM economy WHERE user_id = ?",(user,))
        cash = await cash.fetchone()
        cost = await db.execute("SELECT price FROM items WHERE name = ?",(item,))
        cost = await cost.fetchone()
        if cost == None:
            await db.commit()
            return discord.Embed(title="Invalid item",description="This item doesn't exist in the shop!",timestamp=discord.utils.utcnow())
        if cash[0] >= cost[0]:
            await db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?",(cost[0],user))
            await add_inventory(db,user,amount,item)
            await db.commit()
            return discord.Embed(title="Success",description="You have sucessfully bought item!")

async def create_item(db,ctx,bot,name:str,emoji:int,price:int,description:str):
        await db.execute("CREATE TABLE IF NOT EXISTS items(name text,emoji int,price int,description text, PRIMARY KEY(name))")
        me = await db.execute("SELECT description FROM items WHERE name = ?",(name,))
        data = await me.fetchone()
        if data == None:
            await db.execute("INSERT OR IGNORE INTO items VALUES(?,?,?,?)",(name,emoji,price,description))
            me2 = await db.execute("SELECT emoji,price,description FROM items WHERE name = ?",(name,))
            data2 = await me2.fetchone()
            emoji2,price2,description2 = data2
            emoji3 = bot.get_emoji(emoji)
            embed = discord.Embed(
                title="Success",
                description=f"The creation has been a success.\nName: `{name}`\nEmoji: <:{emoji3.name}:{emoji3.id}>\nPrice: `{price2}`\nDescription: `{description2}`",
                color =0x599f3,
                timestamp = discord.utils.utcnow()
            )
            embed.set_footer(text="Make sure to support Tylo!")
            await db.commit()
            return await ctx.send(embed=embed)
        elif data:
            await db.commit()
            return await ctx.send("Sorry, the following item name has been taken.")

async def usechest():
    gooditems = []

async def sendshop(db,bot):
    embed = discord.Embed(title="Shop",description="\n")
    the = await db.execute("SELECT * FROM items ORDER BY price ASC")
    the = await the.fetchall()
    for s,v,k,s2 in the:
        emoji = bot.get_emoji(v)
        embed.description += f"\n{s} | <:{emoji.name}:{v}>\n`Price`: {k}\n`Description`: {s2}\n"

    return embed

async def get_account(db,user):
        await db.execute("CREATE TABLE IF NOT EXISTS economy(user_id int,cash int,bank int, PRIMARY KEY(user_id))")
        await db.execute("INSERT OR IGNORE INTO economy VALUES(?,?,?)",(user.id,250,750))
        s = await db.execute("SELECT cash,bank FROM economy WHERE user_id = ?",(user.id,))
        me = await s.fetchone()
        await db.commit()
        return me

async def open_account(db,user):
        await db.execute("CREATE TABLE IF NOT EXISTS economy(user_id int,cash int,bank int, PRIMARY KEY(user_id))")
        await db.execute("INSERT OR IGNORE INTO economy VALUES(?,?,?)",(user.id,250,750))
        await db.commit()

async def add_money(db,user,money:int):
        await db.execute("CREATE TABLE IF NOT EXISTS economy(user_id int,cash int,bank int, PRIMARY KEY(user_id))")
        await db.execute("INSERT OR IGNORE INTO economy VALUES(?,?,?)",(user.id,250,750))
        await db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?",(money,user.id))
        await db.commit()

async def remove_money(db,user,money:int):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS economy(user_id int,cash int,bank int, PRIMARY KEY(user_id))")
        await db.execute("INSERT OR IGNORE INTO economy VALUES(?,?,?)",(user.id,250,750))
        await db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?",(money,user.id))
        await db.commit()
