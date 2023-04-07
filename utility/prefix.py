import aiosqlite
from discord.ext import commands

async def changeprefix(message:int,prefix:str):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("UPDATE dprefix SET prefix = ? WHERE guild_id = ?",(prefix,message))
        the = await db.execute("SELECT prefix FROM dprefix WHERE guild_id = ?",(message,))
        the = await the.fetchone()
        await db.commit()
        return the

async def get_prefix(bot,message):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS dprefix(guild_id int,prefix text, PRIMARY KEY(guild_id))")
        me = await db.execute("SELECT prefix FROM dprefix WHERE guild_id = ?",(message.guild.id,))
        thing = await me.fetchone()
        if thing == None:
            await db.execute("INSERT INTO dprefix (guild_id,prefix) VALUES(?,?)",(message.guild.id,str("!")))
            me2 = await db.execute("SELECT prefix FROM dprefix WHERE guild_id = ?",(message.guild.id,))
            me3 = await me2.fetchone()
            await db.commit()
            return me3

        else:
            await db.commit()
            return thing
