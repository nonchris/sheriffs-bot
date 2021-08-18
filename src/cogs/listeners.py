import os
import time
import csv
import re

from database import db_models as db
from database import access_users_db as user_db

import discord
from discord.ext import commands
from environment import REQUIRED_MESSAGES

class BaseRoleManagement(commands.Cog):
    """
	No commands here, just a message handler
	"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.guild is None or message.author.bot:
            return

        author: discord.Member = message.author
        send_messsage_role: discord.Role = message.guild.get_role(877570084447592468)
        session = db.open_session()
        user: db.Users = user_db.get_user_by_id(author.id, session=session)

        user.sent_messages = user.sent_messages + 1
        # increase message count and finish
        # if user hasn't reached required message count or if user was already verified
        if user.sent_messages < REQUIRED_MESSAGES or user.is_verified:
            session.add(user)
            session.commit()
            return

        # basically the one case where a user has to be verified when just passed the limit
        await author.add_roles(send_messsage_role)
        await author.send(f"Hey {author.display_name}, thanks for being an active member!\n"
                          f"You can now post pictures on {message.guild.name} :tada:")
        user.is_verified = True
        session.add(user)
        session.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if user_db.get_user_by_id(member.id) is None:
            user_db.add_user(member.id, member.display_name)

        await member.send(f"Hey {member.display_name}, thanks for joining **{member.guild.name}**, have a great time!\n"
                          f"~Sheriff")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        send_messsage_role: discord.Role = before.guild.get_role(877570084447592468)

        if send_messsage_role not in before.roles and send_messsage_role in after.roles:
            session = db.open_session()
            user: db.Users = user_db.get_user_by_id(before.id, session=session)
            user.is_verified = True
            session.add(user)
            session.commit()


def setup(bot):
    bot.add_cog(BaseRoleManagement(bot))
