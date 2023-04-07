from typing import List

import aiohttp
import discord
from discord.ext import commands
from discord import ui
from utility.tagstuff import Tag,Test
from discord import app_commands
import random
import json
import requests
import asyncio


async def setup(bot):
    await bot.add_cog(Tags(bot))

class Tags(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tree = bot.tree

    @app_commands.command()
    async def getproduct(self,interaction: discord.Interaction,thing:str):
        r = requests.get(f"http://goblinisepic.000webhostapp.com/pacific/hubsystem/getuserproducts.php?username={thing}")
        s = r.content.decode("utf-8")
        if s == "the user owns no products" or s == "Nothing":
            await interaction.response.send_message("Username doesn't exist within the database.")
        else:
            await interaction.response.send_message(s)

    @app_commands.command()
    async def tesst(self,interaction: discord.Interaction):
        await interaction.response.send_modal(Test())


    @app_commands.command()
    async def createtag(self,interaction: discord.Interaction):
        await interaction.response.send_modal(Tag())







