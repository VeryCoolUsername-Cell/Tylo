import discord
from discord.ext import commands
from aiogtts import aiogTTS
import asyncio
import random
from discord import app_commands
from utility.blackjack import Confirm,stuff

async def setup(bot):
    await bot.add_cog(Random(bot))

class Random(commands.Cog):
    def __init__(self,bot: commands.Bot):
        self.bot = bot


    @commands.command()
    async def tts(self,ctx: commands.Context, *,message):
        aiogtts = aiogTTS()
        await aiogtts.save(message, 'audio.mp3', lang='en')

        voice = await ctx.author.voice.channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=r"s",source=f"audio.mp3"))
        voice.play(source)
        while voice.is_playing():
            await asyncio.sleep(1)
        await voice.disconnect()



    @commands.command()
    async def blackjack(self,ctx: commands.Context,amount:int):
        cards = stuff()
        usercards = cards[1]
        dealercards = cards[0]
        bjcombinations = [["A",10],["A","Q"],["A","K"],["A","J"]]
        otherbjcombinations = [i[::-1] for i in bjcombinations[::-1]]
        the = bjcombinations + otherbjcombinations


        if usercards in the:
            desc = f"""
            Dealer: {",".join(str(s) for s in dealercards)}
            User: {",".join(str(s) for s in usercards)}
            """
            embed = discord.Embed(
                title="You won!",
                description = desc
            )
            await ctx.send(embed=embed)
        else:
            desc = f"""
                            Dealer:  {dealercards[0]}
                            User: {",".join(str(s) for s in usercards)}
                            """
            embed = discord.Embed(
                title="Blackjack",
                description=desc
            )

            view = Confirm(ctx.author.id,amount,usercards,dealercards,embed)

            await ctx.send(embed=embed,view=view)









