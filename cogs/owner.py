import aiohttp
import discord
import tabulate
from discord.ext import commands
from discord import app_commands
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Union, Optional
import io
import textwrap
import jishaku
import traceback
from contextlib import redirect_stdout
import prettytable
import aiosqlite
from prettytable import PrettyTable
from utility.prefix import changeprefix
from utility.check import is_owner


async def setup(bot):
    await bot.add_cog(Owner(bot))

class Owner(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.db = bot.db
        self._last_result: Optional[Any] = None

    def cleanup_code(self, content: str) -> str:
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command()
    @is_owner
    async def setprefix(self,ctx: commands.Context,stuff:str):
        the = await changeprefix(ctx.guild.id,stuff)
        await ctx.send(f"Success the prefix is now `{the[0]}`")


    @app_commands.command()
    async def valorantrank(self,interaction: discord.Interaction,region:str,name:str,tag:str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.kyroskoh.xyz/valorant/v1/mmr/{region}/{name}/{tag}") as cs:
                rank = await cs.text()
                rank = rank.split()
                embed = discord.Embed(title="User Rank",description=await cs.text(),timestamp=discord.utils.utcnow())
                if rank[0] == "Iron":
                    embed.set_footer(text="Make sure to support Tylo.",icon_url="https://o.remove.bg/downloads/a3810034-5569-43bb-bcba-ef2a54fab505/image-removebg-preview.png")
                elif rank[0] == "Bronze":
                    embed.set_footer(text="Make sure to support Tylo.",icon_url="https://static.wikia.nocookie.net/valorant/images/b/bd/Bronze_1_Rank.png/revision/latest/scale-to-width-down/250?cb=20200623203119")
                elif rank[0] == "Silver":
                    embed.set_footer(text="Make sure to support Tylo.",icon_url="https://o.remove.bg/downloads/ac213f18-b0ba-4456-ad2f-60e4f117706d/image-removebg-preview.png")
                elif rank[0] == "Gold":
                    embed.set_footer(text="Make sure to support Tylo.",icon_url="https://o.remove.bg/downloads/613fe63a-c38e-4df6-905b-b971ae3577ec/image-removebg-preview.png")
                elif rank[0] == "Platinum":
                    embed.set_footer(text="Make sure to support Tylo.",icon_url="https://o.remove.bg/downloads/12885c89-f6be-425e-b9c9-99afa0f030b4/Platinum_3_Rank-removebg-preview.png")
                elif rank[0] == "Diamond":
                    embed.set_footer(text="Make sure to support Tylo.", icon_url="https://o.remove.bg/downloads/a3eaae45-1d1c-4866-bbbf-acfb93b277a9/Diamond_3_Rank-removebg-preview.png")
                elif rank[0] == "Ascendant":
                    embed.set_footer(text="Make sure to support Tylo.", icon_url="https://o.remove.bg/downloads/e5c20425-60ae-4827-b70f-61748d38e32a/Ascendant_3_Rank-removebg-preview.png")
                elif rank[0] == "Immortal":
                    embed.set_footer(text="Make sure to support Tylo.", icon_url="https://o.remove.bg/downloads/a98ff885-4c41-4bd9-a3bf-f496630bbdc5/valorant_immortal_1_account_1595859500_f0ee976a_progressive-removebg-preview.png")
                elif rank[0] == "Radiant":
                    embed.set_footer(text="Make sure to support Tylo.", icon_url="https://o.remove.bg/downloads/f47f9fa2-7dd7-415c-be5d-4eaa459891fc/st_small_507x507-pad_600x600_f8f8f8-removebg-preview.png")
                await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def reload(self, interaction: discord.Interaction, cog: str):
        await self.bot.unload_extension(f'cogs.{cog}')
        await self.bot.load_extension(f'cogs.{cog}')

        await interaction.response.send_message(f"{cog} has been reloaded.")

    @commands.command()
    async def sql(self,ctx: commands.Context,*,command:str):
            async with await self.bot.db.execute(command) as cur:
                await self.bot.db.commit()
                if cur.description:
                    columns = [tuple[0] for tuple in cur.description]
                else:
                    columns = "keys"
                thing = await cur.fetchall()
                if len(thing) == 0:
                    return await ctx.message.add_reaction("<:check:935611146470293634> ")
                thing = tabulate.tabulate(thing, headers=columns, tablefmt="psql")
                byte = io.BytesIO(str(thing).encode("utf-8"))
                return await ctx.send(file=discord.File(fp=byte, filename="table.txt"))

    @app_commands.command()
    async def unload(self, interaction: discord.Interaction, cog: str):
        await self.bot.unload_extension(f'cogs.{cog}')
        await self.bot.load_extension(f'cogs.{cog}')

        await interaction.response.send_message(f"{cog} has been unloaded.")

    @commands.command(name='eval')
    async def _eval(self, ctx: commands.Context, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
