import discord
from discord.ext import commands
from utility.econstuff import add_money,open_account,remove_money,get_account,create_item,sendshop,buy,see_inventory
from utility.check import is_owner
from utility.randomviews import SelectView
from utility.pagination import Pagination
import typing

class Economy(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.db = bot.db
        self.tree = bot.tree

    @commands.command()
    async def traderequest(self,ctx: commands.Context,user: typing.Union[discord.Member] = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title = "Trade Request",
            description = "\n"
        )
        view = SelectView(180,[["Coal",1],["Netherite",110],["Chest",5]],embed)
        await ctx.send(embed=embed,view=view)

    @commands.command()
    async def shop(self,ctx: commands.Context):
        embed = await sendshop(self.bot.db,self.bot)
        await ctx.send(embed=embed)

    @commands.command()
    async def test(self,ctx: commands.Context):
        my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        embeds = []

        for i in range(0, len(my_list), 5):
            sublist = my_list[i:i + 5]
            for j in range(sublist[0], sublist[-1] + 1):
                embeds.append(discord.Embed(title="stuff",description=j))

        embeds[0].set_footer(text=f"0/{len(embeds)}")

        await ctx.send(embed=embeds[0],view=Pagination(embeds))

    @commands.command()
    async def top(self,ctx: commands.Context):
        query = "SELECT * FROM economy ORDER BY cash DESC LIMIT 10"
        the = await self.bot.db.execute(query)
        the = await the.fetchall()
        the2 = 0
        embed = discord.Embed(title="Top 3",description="\n")
        for i,v,k in the:
            the2 += 1
            embed.description += f"\n {the2} |<@{i}> {v+k}"

        await ctx.send(embed=embed)

    @commands.command()
    async def inventory(self,ctx: commands.Context,user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = await see_inventory(self.bot.db,user.id,user.name)
        await ctx.send(embed=embed)


    @commands.command()
    @is_owner
    async def createitem(self,ctx: commands.Context,name:str,emoji: discord.Emoji,price:int,*,description:str):
        await create_item(self.bot.db,ctx,self.bot,name,emoji.id,price,description)


    @commands.hybrid_command()
    @is_owner
    async def addmoney(self,ctx: commands.Context,user: discord.Member,amount:int):
        if user == None:
            user = ctx.author

        await add_money(self.bot.db,user,amount)
        await ctx.send("Success, check your balance!")

    @commands.hybrid_command()
    @is_owner
    async def removemoney(self, ctx: commands.Context, user: discord.Member, amount: int,):
        if user == None:
            await ctx.send("Mention an user.")

        await remove_money(self.bot.db,user, amount)
        await ctx.send("Success, check your balance!")

    @commands.command()
    async def buy(self,ctx: commands.Context,item:str,amount:int=None):
        if amount is None:
            amount = 1
        the = await buy(self.bot.db,ctx.author.id,amount,item)
        await ctx.send(embed=the)


    @commands.hybrid_command()
    async def balance(self,ctx: commands.Context,user: discord.Member=None):
        if user == None:
            user = ctx.author

        me = await get_account(self.bot.db,user)
        cash,bank = me
        embed = discord.Embed(
            title=f"{user.name}'s Balance",
            description=f"```yaml\nCash: {cash}\nBank: {bank}```",
            timestamp = discord.utils.utcnow(),
            color = 0x599f3
        )
        embed.set_footer(text="Support Tylo or else.")
        embed.set_author(name=" ",icon_url=user.display_avatar.url)
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot),guild=discord.Object(id=881874875155898438))