from discord import ui
import discord
import traceback

class Pagination(discord.ui.View):
    def __init__(self,embeds):
        super().__init__(timeout=None)
        self.page = 1
        self.embed = embeds
        self.max = len(embeds)+1

    async def updatepag(self,interaction: discord.Interaction):
        if self.page == self.max:
            self.page -= self.page
            await interaction.response.edit_message(embed=self.embed[self.page])
        else:
            self.embed[self.page].set_footer(text=f"{self.page}/{len(self.embed)}")
            await interaction.response.edit_message(embed=self.embed[self.page])

    @discord.ui.button(label='<<', style=discord.ButtonStyle.blurple)
    async def _1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= len(self.embed)-1
        await self.updatepag(interaction)

    @discord.ui.button(label='<', style=discord.ButtonStyle.green)
    async def _2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= 1
        await self.updatepag(interaction)

    @discord.ui.button(label='>', style=discord.ButtonStyle.green)
    async def _3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        await self.updatepag(interaction)

    @discord.ui.button(label='>>', style=discord.ButtonStyle.blurple)
    async def _4(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= self.page
        self.page += self.max
        await self.updatepag(interaction)



