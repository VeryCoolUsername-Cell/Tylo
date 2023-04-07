import discord
from discord.ext import commands
from io import BytesIO
import aiohttp

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))




class Miscellaneous(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def stuff(self,ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekobot.xyz/api/image?type=4k") as S:
                 s = await S.json()
                 embed = discord.Embed(title="Yeah",description="stuff")
                 embed.set_image(url=s["message"])
                 await ctx.author.send(embed=embed)

    @commands.command()
    async def cemoji(self,ctx: commands.Context, url: str, *, name):
        if ctx.author.guild_permissions.manage_emojis:
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:

                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200, 299):
                            emoji = await ctx.guild.create_custom_emoji(image=b_value, name=name)
                            await ctx.send(f'Successfully created emoji: <:{name}:{emoji.id}>')
                            await ses.close()
                        else:
                            await ctx.send(f'Error when making request | {r.status} response.')
                            await ses.close()

                    except discord.HTTPException:
                        await ctx.send('File size is too big!')
