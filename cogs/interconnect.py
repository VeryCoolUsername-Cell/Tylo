from discord.ext import commands
import asyncio
import discord

async def setup(bot):
    await bot.add_cog(InterConnect(bot))

class InterConnect(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.IDS = []
        self.togethers = []
        self.ids = {}

    @commands.command()
    async def seestuff(self,ctx: commands.Context):
        print(self.ids)
        print(self.togethers)

    @commands.command()
    async def joinqueue(self,ctx: commands.Context):

        id = ctx.author.id
        if id in self.IDS:
            return
        if len(self.IDS) == 0:
            self.IDS.append(id)
            self.ids[id] = ctx.channel.id

            while len(self.IDS) <= 2:
                await asyncio.sleep(1)

        self.ids[id] = ctx.channel.id
        lastid = self.IDS[-1]
        self.IDS.remove(lastid)
        idss = [id,lastid]

        self.togethers.append(idss)

        channel = self.ids[lastid]
        channel = self.bot.get_channel(channel)
        await channel.send(f"Someone has picked up the phone!! <@{ctx.author.id}>")
        await ctx.send(f"Someone has picked up the phone!! <@{lastid}>")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        author_id = message.author.id
        the_ids = []
        index = 0
        for item in self.togethers:
            for stuff in item:
                the_ids.append(stuff)

        if author_id in the_ids:
            for each in self.togethers:
                if author_id in each:
                    index += self.togethers.index(each)
        else:
            return

        if message.content == "--quit":
            sids = self.togethers[index]
            s = sids.copy()

            for item in sids:
                stuff = self.ids[item]
                self.ids.pop(item)
                channel = self.bot.get_channel(stuff)
                await channel.send("terminated")
                self.togethers.pop(index)

            return
        if message.content == "!joinqueue":
            return
        sids = self.togethers[index].copy()
        sids.remove(author_id)
        sids = sids[0]
        channel = self.ids[sids]
        channel = self.bot.get_channel(channel)

        await channel.send(f"{message.content} from <@{author_id}>")


