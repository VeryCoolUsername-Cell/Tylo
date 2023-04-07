from discord.ext import commands

async def is_owner(ctx):
    return True if ctx.author.id in [864956507195441163] else False

is_owner = commands.check(is_owner)