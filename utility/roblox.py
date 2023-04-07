import discord
import aiohttp
import aiosqlite
import requests

token  = ""

async def verification(ctx,roblox:str):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS roblox(username text,discord int, PRIMARY KEY(discord))"
        )
        await db.execute(
            "INSERT OR IGNORE INTO roblox VALUES(?,?)",
            (roblox, ctx.author.id)
        )
        me = await db.execute("SELECT username FROM roblox WHERE discord = ?", (ctx.author.id,))
        s = await me.fetchone()
        await db.commit()
        return s


async def getid(ctx,username:str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.roblox.com/users/get-by-username?username={username}") as s:
            me = await s.json()
            if "success" in me:
                embed = discord.Embed(
                    title="Incorrect Username",
                    description="That username doesn't exist.\nRetry again in 5 seconds.",
                    timestamp=discord.utils.utcnow(),
                    color=0x3cc1d3
                )
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                embed.set_footer(text=f"Make sure to support Tylo.")
                await ctx.send(embed=embed)
            else:
                ids = me["Id"]
                return ids


async def getgrouproles(group:int,rank:str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://groups.roblox.com/v1/groups/{group}/roles") as s:
            me = await s.json()
            for entry in me["roles"]:
                if entry["name"] == rank:
                    return entry["rank"]
                else:
                    pass

async def getrank(group:int,role_id:int):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://groups.roblox.com/v1/groups/{group}/roles") as s:
            me = await s.json()
            for entry in me["roles"]:
                if entry["id"] == role_id:
                    return entry["rank"]
                else:
                    pass


async def getrankname(group:int,role_id:int):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://groups.roblox.com/v1/groups/{group}/roles") as s:
            me = await s.json()

            for entry in me["roles"]:
                if entry["rank"] == role_id:
                    return entry["name"]
            else:
                pass



async def roleid(ctx,client,name:str,id:int):
    rr = requests.get(f"http://goblinisepic.000webhostapp.com/pacific/renk/userconfirm.php?groupid={id}&user={name}")
    lol = rr.content
    lol2 = lol.decode("utf-8")
    lol3 = str(lol2)
    if lol3 == "user found in group":
        rra = requests.get(
            f"http://goblinisepic.000webhostapp.com/pacific/renk/testgetnextrank.php?groupid={id}&user={name}")
        aa = rra.content
        rra1 = aa.decode("utf-8")
        return rra1
    else:
        await ctx.send("user not found")

async def promote(ctx,client,roblox:str,group:int):
    me = await roleid(ctx,client,roblox,group)
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://groups.roblox.com/v1/groups/{group}/roles") as s:
            me2 = await s.json()
            for entry in me2["roles"]:
                if entry["id"] == int(me):
                    return entry["rank"]
                else:
                    pass

async def demote(ctx,roblox:str,group:id):
    pass




