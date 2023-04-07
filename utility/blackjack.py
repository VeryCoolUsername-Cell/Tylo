import discord
import random
from discord import Interaction
from typing_extensions import *
import traceback

def stuff():
    list1 = []

    cards = [2,3,4,5,6,7,8,9,10,"A","Q","K","J"]
    random.shuffle(cards)
    the = random.sample(cards,2)
    the2 = random.sample(cards,2)
    list1.append(the)
    list1.append(the2)

    return list1

def values(the:list):
    verynice = {
        "A" : 11,
        "A2" : 1,
        "Q" : 10,
        "J" : 10,
        "K" : 10,
        10 : 10,
        9 : 9,
        8 : 8,
        7 : 7,
        6 : 6,
        5 : 5,
        4 : 4,
        3 : 3,
        2 : 2
    }
    newlist = []
    for i in the:
        newlist.append(verynice[i])

    return newlist




def bust(the:list):
    verynice = {
        "A" : 11,
        "A2" : 1,
        "Q" : 10,
        "J" : 10,
        "K" : 10,
        10 : 10,
        9 : 9,
        8 : 8,
        7 : 7,
        6 : 6,
        5 : 5,
        4 : 4,
        3 : 3,
        2 : 2
    }
    newlist = []
    for i in the:
        newlist.append(verynice[i])
    if sum(newlist) > 21:
        if 11 in newlist:
            the = newlist.index(11)
            del newlist[the]
            newlist.append(1)
        else:
            return True
    else:
        return False

class Confirm(discord.ui.View):
    def __init__(self, user,amount,usercards,dealercards,embed):
        super().__init__(timeout=None)
        self.user = user
        self.amount = amount
        self.embed = embed
        self.usercards = usercards
        self.dealercards = dealercards

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True if interaction.user.id == self.user else await interaction.response.send_message(
            "You don't have permission to press this.", ephemeral=True)

    async def disable(self,interaction: discord.Interaction,button):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

    async def stand(self,interaction: discord.Interaction):
        if sum(self.dealercards) < 21:
            if sum(self.dealercards) >= 17:
                pass
            else:
                while True:
                    the = random.randint(1, 11)
                    self.dealercards.append(the)
                    if sum(self.dealercards) >= 21:
                        desc = f"""
                        Dealer:  {",".join(str(s) for s in self.dealercards)},
                        User: {",".join(str(s) for s in self.usercards)}
                                                                        """
                        self.embed.description = desc
                        await interaction.followup.send(embed=self.embed)
                        break
                    elif sum(self.dealercards) >= 17:
                        if sum(self.dealercards) > sum(self.usercards):
                            self.embed.title = "You lost"
                        else:
                            self.embed.title = "You win"
                        desc = f"""
                        Dealer:  {",".join(str(s) for s in self.dealercards)},
                        User: {",".join(str(s) for s in self.usercards)}
                                                                                                """
                        self.embed.description = desc
                        await interaction.followup.send(embed=self.embed)
                        break
                    else:
                        pass


    @discord.ui.button(label='Hit', style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.interaction_check(interaction)
        the = random.randint(1,11)
        self.usercards.append(the)
        desc = f"""
                        Dealer:  {",".join(str(s) for s in self.dealercards)},
                        User: {",".join(str(s) for s in self.usercards)}
                        """
        self.embed.description = desc
        if bust(self.usercards):
            self.embed.title = "Bust"
            await interaction.response.edit_message(embed=self.embed)
            await self.disable(interaction, button)
        elif bust(self.usercards) is False:
            self.embed.title = "Blackjack"
            await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(label='Stand', style=discord.ButtonStyle.green)
    async def Stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.interaction_check(interaction)

        await self.disable(interaction, button)

        the = random.randint(1, 11)

        self.dealercards.append(the)

        desc = f"""
                                Dealer:  {",".join(str(s) for s in self.dealercards)},
                                User: {",".join(str(s) for s in self.usercards)}
                                """
        self.embed.description = desc
        await interaction.response.edit_message(embed=self.embed)
        await self.stand(interaction)














