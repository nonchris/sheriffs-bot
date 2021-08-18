from typing import List

import discord
from discord.ext import commands

from utils import utils as ut
from database import access_users_db as user_db


### @package misc
#
# Collection of miscellaneous helpers.
#

class Misc(commands.Cog):
    """
    Various useful Commands for everyone
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help="Check if Bot available")
    async def ping(self, ctx):
        """!
        ping to check if the bot is available

        @param ctx Context of the message
        """
        print(f"ping: {round(self.bot.latency * 1000)}")

        await ctx.send(
            embed=ut.make_embed(
                name='Bot is available',
                value=f'`{round(self.bot.latency * 1000)}ms`')
        )

    @commands.has_permissions(administrator=True)
    @commands.command(name='gr')
    async def give_role(self, ctx: commands.Context):
        members: List[discord.Member] = ctx.guild.members
        role = ctx.guild.get_role(877570084447592468)
        for member in members:
            if role in member.roles:
                continue

            user_db.add_user(user_id=member.id, username=member.name, join_date=member.joined_at, is_verified=True)
            await member.add_roles(role)
            print(f"Gave {role.name} to {member.display_name}")

        print("Done")



def setup(bot):
    bot.add_cog(Misc(bot))
