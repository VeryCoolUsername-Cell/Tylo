import discord
from discord.ext import commands
import aiohttp
import asyncio
import random
import datetime
from roblox import Client
from utility.roblox import token,getgrouproles,getid,verification,promote,getrankname
import requests
from discord import app_commands


def randomsentence():
    sentences = "cool nice epic giant dinosaur food lunch dinner carrots computer tasty presentation rich shift consumer retire intelligent awesome great fantastic wow approval books shelf line flask kettle funny great pond river ocean shoes".split()
    me = random.sample(sentences,15)
    return me

async def setup(bot):
    await bot.add_cog(ROBLOX(bot))

class ROBLOX(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.client = Client(f"{token}")
        self.bot.launch_time = datetime.datetime.now(datetime.timezone.utc)
        self.group = 8597721

    @commands.command(name='uptime')
    async def uptime(self, ctx: commands.Context):
        resolved_full = discord.utils.format_dt(self.bot.launch_time, "F")
        resolved_rel = discord.utils.format_dt(self.bot.launch_time, "R")
        fmt = f"I started at {resolved_full}, and have been up since: {resolved_rel}"
        await ctx.send(fmt)

    @commands.command()
    async def promote(self,ctx: commands.Context,user:str,group_id):
        me = await promote(ctx,self.client,user,group_id)
        group = self.client.get_base_group(group_id)
        user2= await getid(ctx, user)
        await group.set_rank(user2, me)
        me4 = await getrankname(group_id,me)
        await ctx.send(f"Successful, you have now been ranked to {me4}.")

    @commands.command()
    async def demote(self, ctx: commands.Context, user: str):
        pass

    @commands.command()
    async def rank(self,ctx: commands.Context,group:int,user:str,rank:str):
        group = self.client.get_base_group(group)
        user = await getid(ctx, user)
        print("id issue")
        me2 = await getgrouproles(int(group), rank)
        if me2 is None:
            await ctx.send("That following rank doesn't exist.")
        else:
            await group.set_rank(user, me2)
            await ctx.send(f"The following user has been promoted to {rank} | {me2}")

    @commands.command()
    async def verify(self, ctx: commands.Context, username):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.roblox.com/users/get-by-username?username={username}") as d:
                me = await d.json()
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
                    id = me["Id"]
                    me21 = randomsentence()
                    me532 = " ".join(me21)
                    embed = discord.Embed(
                        title=f"{username}",
                        description=f"To verify this account place the following sentence into your bio.\n\n`{me532}`",
                        timestamp=discord.utils.utcnow(),
                        color=0x3cc1d3
                    )
                    me3 = await cs.get(
                        f"https://thumbnails.roblox.com/v1/users/avatar-bust?userIds={id}&size=420x420&format=Png&isCircular=false")
                    m34 = await me3.json()
                    url = m34["data"][0]["imageUrl"]
                    embed.set_thumbnail(url=url)
                    message = await ctx.send(embed=embed)

                    def check(message):
                        return message.author == ctx.author

                    me521 = await self.bot.wait_for("message", timeout=30, check=check)
                    await asyncio.sleep(5)
                    if me521.content == "Done":
                        me51231 = await cs.get(f"https://users.roblox.com/v1/users/{id}")
                        rweuy2 = await me51231.json()
                        description = rweuy2["description"]
                        if description == me532:
                            me5215 = await verification(ctx,username)
                            embed2 = discord.Embed(
                                title="Success",
                                description=f"You have been verified as {me5215[0]}.",
                                timestamp = discord.utils.utcnow(),
                                color=0x3cc1d3
                            )
                            embed2.set_thumbnail(url=url)
                            await message.edit(embed=embed2)
                        else:
                            await ctx.send("Didn't work.")

                    else:
                        await ctx.send("ye something random ig")