import discord
import logging
from decouple import config
from discord import Message
from discord.channel import TextChannel
from discord.ext import commands as DiscCommand
from db import Database

logger = logging.getLogger(__name__)
db = Database()


async def get_prefix(client, message: Message):
    if isinstance(message.channel, TextChannel):
        prefixes = db.get_prefixes(message.guild.id)
        return prefixes["prefix"]
    return "!"

description = """# < Kuuhaku /> bot
"""
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = DiscCommand.Bot(
    command_prefix=get_prefix,
    description=description,
    intents=intents,
)