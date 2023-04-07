import discord
import aiohttp
import aiosqlite
import requests

token  = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_A61302308423CF4049FB82ACD4316026BF2E153EA1BFE3AFC04C92878C560BD968D8C730285223C5F7EBD4E0CF0363FA76CCF7223DB0E0AF36E9F138158576AE54C7C827442D9AD11934770B16F68A463EB5E94A81337AE3BF8E1734A58130283AF68A0D85CC2EB50CD3495E9B5D6F936CEAA86903C753C3C797123E7D5A0F900AD97BCDDD2C3F9F84D56C545B9FC982A78DA8B928D68E20ED9DBD3910D25A1A073DFA4AA1BDE0717E08C1F2DE4EEB9A47F2C87EACA2D764742123E4FEB7D59AEEC3FC8F319DA53CC06DB3CAD8A4D1A204487E88D0EFC2C013A3201B504B54C67AEC29C23F8A4AFD81EB8DE15FD7DDFDB3AFD01A5AA3E607E74C4F71D50E88118E850EAC105A53F484924039FF37EAB773B3BC47E513BAD32D0A060D64357E37400F7DFFCF05A61BCC23A6355BEF025ABA684FD33D50B9A709AAFF8BE43A07090BE1C883DAAA94F3245EE0A26C2F39ACBF2EB49DD4E12891C5C9B066184BB1BEE2834F51C8A14AABDE233FDBC81CCF76150C8C75"

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




