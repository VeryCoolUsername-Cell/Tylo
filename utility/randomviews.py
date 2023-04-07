import discord
from discord import ui
import traceback
from typing import List


class Select(discord.ui.Select):
    def __init__(self, stuff,embed):
        options = []
        self.the = []
        self.max = 0

        if len(options) > 4:
            self.max += 4
        else:
            self.max += len(stuff)

        for item, amount in stuff:
            options.append(discord.SelectOption(label=item, emoji="🎭", description=amount))

        super().__init__(placeholder="Select an option", max_values=self.max, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) >= self.max:
            stuff2 = ["`x1` " + s + "\n" for s in self.values]
            self.embed = discord.Embed(
                title = "Items",
                description = "\n".join(s for s in stuff2),
            )
            try:
                self.disabled = True
                await interaction.response.edit_message(embed=self.embed,view=self.view)
            except:
                print(traceback.format_exc())
        else:
            await interaction.response.send_message(content=f"You have successfully added {self.values[-1]}", ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, timeout: int, stuff,embed):
        super().__init__(timeout=timeout)
        self.dropdown = Select(stuff,embed)
        self.embed = embed

        self.add_item(self.dropdown)

    @discord.ui.button(label='Done', style=discord.ButtonStyle.green)
    async def Done(self, interaction: discord.Interaction, button: discord.ui.Button):
        stuff2 = ["`x1` " + s + "\n" for s in self.dropdown.values]
        self.embed = discord.Embed(
            title="Items",
            description="\n".join(s for s in stuff2),
        )
        self.dropdown.disabled = True
        await interaction.response.edit_message(embed=self.embed,view=self.dropdown.view)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.green)
    async def Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.edit_message(content="Aborted command.",embed=None,view=None)
        except:
            print(traceback.format_exc())


