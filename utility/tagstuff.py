import aiohttp
import discord
import aiosqlite
from discord import ui
import traceback
import requests

async def createtag(interaction: discord.Interaction,name,embed,description):
    async with aiosqlite.connect("database5.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS tagss(name text,user int,embed text, description text,guild int,usage int)")
        me = await db.execute("SELECT usage FROM tagss WHERE guild = ? AND name = ?",(interaction.guild.id,str(name)))
        s = await me.fetchone()
        if s is None:
            await db.execute("INSERT OR IGNORE INTO tagss VALUES(?,?,?,?,?,?)",(
                    str(name),
                    interaction.user.id,
                    str(embed),
                    str(description),
                    interaction.guild.id,
                    0

            ))
            await db.commit()
            await interaction.response.send_message(f"The tag is already taken..", ephemeral=True)

        else:
            await db.commit()
            await interaction.response.send_message(f"The tag is being checked.", ephemeral=True)


class Tag(ui.Modal, title='Tag Creation'):
    name = ui.TextInput(label='Name')
    description = ui.TextInput(label='Description', style=discord.TextStyle.paragraph)
    foo = discord.ui.Select(options=[discord.SelectOption(label='Yes'), discord.SelectOption(label='No')])

    async def on_submit(self, interaction: discord.Interaction):
        print("nice")
        me = self.foo.values
        the =", ".join(me)
        print(the)
        print(self.name,self.description,interaction.guild.id)
        await createtag(interaction,self.name,str(the),self.description)
        print("create tag")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(content='Oops! Something went wrong.')

        traceback.print_tb(error.__traceback__)


class Test(ui.Modal, title='Add Product'):
    name = ui.TextInput(label='Name')
    description = ui.TextInput(label='Product', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):

            s = requests.get(f"http://goblinisepic.000webhostapp.com/pacific/hubsystem/applyuserprod.php?username={self.name}&add={self.description}")
            thing = s.content
            Decoded = thing.decode("utf - 8")
            if Decoded == "Nothing":
                embed = discord.Embed(
                    title = "Error",
                    description="Player isn’t found on the database.",
                    timestamp = discord.utils.utcnow()
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title="Success",
                    description=Decoded,
                    timestamp = discord.utils.utcnow()
                )
                await interaction.response.send_message(embed=embed)



    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(content='Oops! Something went wrong.')

        traceback.print_tb(error.__traceback__)










