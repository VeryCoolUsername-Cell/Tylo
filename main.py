
import aiohttp
import aiosqlite
import discord
from discord.ext import commands
import os
import asyncio
from utility.prefix import get_prefix
from dotenv import load_dotenv

load_dotenv()

class Tylo(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description="Cool bot I guess?",
            intents=discord.Intents.all(),
            enable_debug_events=True,
        )


    async def setup_hook(self) -> None:

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
               await self.load_extension(f'cogs.{filename[:-3]}')

            else:
                print(f'Unable to load {filename[:-3]}')
        await self.load_extension('jishaku')

    async def on_ready(self):
        print(f"Bot online\n{self.user.name} | {self.user.id} | {discord.utils.utcnow()}")


async def main():
    bot = Tylo()
    async with bot,aiosqlite.connect("database.db") as db,aiohttp.ClientSession() as cs:
        bot.db = db
        bot.cs = cs
        await bot.start(os.getenv("TOKEN"),reconnect=True)



asyncio.run(main())
