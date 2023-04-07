import discord
from discord.ext import commands
import traceback
from datetime import datetime
from discord import Interaction
from discord import app_commands
from discord.app_commands import AppCommandError

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))

class ErrorHandler(commands.Cog):
    def __int__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def app_command_error(self,interaction: Interaction,error: AppCommandError):
        print(error)


    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="Error", description=f"<:error:901411672441360424> {error}", color=0x36393E,
                                  timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Error", description=f"<:error:901411672441360424>  {error}", color=0x36393E,
                                  timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NSFWChannelRequired):
            embed = discord.Embed(title="Error", description=f"<:error:901411672441360424>  {error}", color=0x36393E,
                                  timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Error", description=f"<:error:901411672441360424> {error}", color=0x36393E,
                                  timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                embed = discord.Embed(title=f"Cooldown",
                                      description=f"Chill wait {int(s)} seconds\nThen do the command again",
                                      color=0x36393E, timestamp=datetime.utcnow())
                await ctx.send(embed=embed)
            elif int(h) == 0 and int(m) != 0:
                embed = discord.Embed(title=f"Cooldown",
                                      description=f"Chill wait {int(m)}minutes and {int(s)} seconds\nThen do the command again",
                                      color=0x36393E, timestamp=datetime.utcnow())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f"Cooldown",
                                      description=f"Chill wait {int(h)}hours, {int(m)}minutes and {int(s)} seconds\nThen do the command again",
                                      color=0x36393E, timestamp=datetime.utcnow())
                await ctx.send(embed=embed)

        elif isinstance(error,commands.CheckFailure):
            embed = discord.Embed(title=f"CheckFailure",
                                  description=f"You don't have permission to use this.",
                                  color=0x36393E, timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            msg = "".join(traceback.format_exception(type(error), error, error.__traceback__))
            await ctx.send(error)

            print(msg)




