import time
import logging
from decouple import config
import discord
from discord.ext import commands
import random
from Trello import Trello
from db import Database
from utils import EMOJIS, FILTERED_WORDS
from functions import extract_guild

logger = logging.getLogger(__name__)
db = Database()


async def get_prefix(client, message):
    prefixes = db.get_prefixes(message.guild.id)    
    return prefixes["prefix"]


description = """# < Kuuhaku /> bot
"""
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(
    command_prefix=get_prefix,
    description=description,
    intents=intents,
)


@bot.command()
async def teste(ctx):
    """Returns pong"""
    await ctx.channel.send("pong")

@bot.command()
async def settings(ctx,setting = None):
    """defines settings"""
    if setting is not None:
        if setting == "trello":
            config = db.get_trello_config(ctx.guild.id)
            if config == False:
                return await ctx.channel.send("There's no trello account linked yet.")    
            return await ctx.channel.send(config)    
        await ctx.channel.send("setting")
        return
    await ctx.channel.send("pong")


@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = "Welcome {0.mention} to {1.name}!".format(member, guild)
        await guild.system_channel.send(to_send)


@bot.event
async def on_message(message):
    for word in FILTERED_WORDS:
        if word in message.content:
            await message.delete()
            return
    if message.author == bot.user:
        return
    guild = extract_guild(message)
    # if message.content.startswith(guild.prefix):
    #     await message.channel.send("Hello!")
    try:
        await bot.process_commands(message)
    except discord.CommandError as err:
        print(err)
        await message.channel.send(
            "Hey, what?! I don't know this command. Try a known command."
        )
    print("Message from {0.author}: {0.content}".format(message))


@bot.event
async def on_ready():
    logger.info("Logged on as {0}!".format(bot.user))


class Bot(commands.Cog):
    def __init__(self):
        self.bot = bot

    def run(self):
        self.bot.run(config("TOKEN"))
