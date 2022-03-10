import time
import logging
from decouple import config
import discord
from discord.channel import TextChannel
from discord.ext import commands
import random
from Trello import Trello
from db import Database
from utils import EMOJIS, FILTERED_WORDS, GENERAL_CHANNEL_NAMES, Clients
from functions import extract_guild, extract_message, extract_user, attribute_msg_xp

logger = logging.getLogger(__name__)
db = Database()
clients = Clients()


async def get_prefix(client, message):
    prefixes = db.get_prefixes(message.guild.id)
    return prefixes["prefix"]


class Embed(discord.Embed):
    def __init__(self, **kwargs):
        color = kwargs.pop("color", 0x9CCFFF)
        super().__init__(**kwargs, color=color)


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
async def profile(ctx):
    """Displays user profile"""
    user = extract_user(ctx)
    embed = Embed(
        title=f"Hey {user.name}#{user.discriminator}! \N{WAVING HAND SIGN}",
        description=f"Here's your profile",
    )
    embed.set_thumbnail(url=user.avatar)
    embed.add_field(
        name="XP",
        value=(user.xp),
        inline=True,
    )
    embed.add_field(
        name="Level",
        value=(user.level),
        inline=True,
    )
    embed.add_field(
        name="Next Level",
        value=(user.level_requirement),
        inline=True,
    )

    await ctx.channel.send(embed=embed)


@bot.group(pass_context=True)
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def settings(ctx):
    """defines settings"""
    if ctx.invoked_subcommand is None:
        return await ctx.channel.send("Please, use one of the trello subcommands")
    
        if setting == "trello":
            config = db.get_trello_config(ctx.guild.id)
            if config == False:
                return await ctx.channel.send("There's no trello account linked yet.")
            return await ctx.channel.send(config)
        if setting == "set":
            if key == "trello":
                if value is None:
                    return await ctx.channel.send("Please, u must provide a value")
                user = extract_user(ctx)
                guild = extract_guild(ctx)
                db.set_trello_config(guild.guild_id, value, user.id)
                return await ctx.channel.send("Done!")

        await ctx.channel.send("setting")
        return
    await ctx.channel.send("pong")


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except Exception:
        await ctx.send("Format has to be in NdN!")
        return
    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.group(pass_context=True)
async def trello(ctx):
    if ctx.invoked_subcommand is None:
        return await ctx.channel.send("Please, use one of the trello subcommands")
    guild = extract_guild(ctx)
    trello_token = db.get_trello_config(guild.guild_id)
    clients.add_client("trello", guild.guild_id, Trello(trello_token["TOKEN"]))


@trello.group(pass_context=True)
async def boards(ctx):
    guild = extract_guild(ctx)
    trello = clients.get_client("trello", guild.guild_id)
    boards = trello.get_boards()
    embed = Embed(
        title="Aqui estão seus quadros do Trello!",
        description="\n".join([board.name for board in boards])
    )
    return await ctx.channel.send(embed=embed)

@trello.group(pass_context=True)
async def lists(ctx, board = None):
    guild = extract_guild(ctx)
    print(board)
    trello = clients.get_client("trello", guild.guild_id)
    if trello.default_board is None:
        if board is None:
            return await ctx.channel.send("You must define default board or pass the board name")
    lists = trello.get_lists(board)
    print(lists)
    return await ctx.channel.send("lists")

@trello.group(pass_context=True)
async def cards(ctx, board = None, list = None):
    guild = extract_guild(ctx)
    print(board)
    trello = clients.get_client("trello", guild.guild_id)
    if trello.default_board is None:
        if board is None:
            return await ctx.channel.send("You must define default board or pass the board name")
    cards = trello.get_cards(board,list)
    print(cards)
    return await ctx.channel.send("cards")

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = "Welcome {0.mention} to {1.name}!".format(member, guild)
        await guild.system_channel.send(to_send)


@bot.event
async def on_guild_join(guild):
    priority_channels = []
    channels = []
    for channel in guild.channels:
        if channel == guild.system_channel or any(
            x in channel.name for x in GENERAL_CHANNEL_NAMES
        ):
            priority_channels.append(channel)
        else:
            channels.append(channel)
    channels = priority_channels + channels
    try:
        channel = next(
            x
            for x in channels
            if isinstance(x, TextChannel) and x.permissions_for(guild.me).send_messages
        )
    except StopIteration:
        return
    prefix = "!"

    embed = Embed(
        title="Thanks for adding me to your server! \N{WAVING HAND SIGN}",
        description=f"To get started, do `{prefix}start` to pick your starter pokémon. As server members talk, wild pokémon will automatically spawn in the server, and you'll be able to catch them with `{prefix}catch <pokémon>`! For a full command list, do `{prefix}help`.",
    )
    embed.add_field(
        name="Common Configuration Options",
        value=(
            f"• `{prefix}prefix <new prefix>` to set a different prefix (default: `p!`)\n"
            f"• `{prefix}redirect <channel>` to redirect pokémon spawns to one channel\n"
            f"• More can be found in `{prefix}config help`\n"
        ),
        inline=False,
    )
    embed.add_field(
        name="Support Server",
        value="Join our server at [discord.gg/poketwo](https://discord.gg/poketwo) for support.",
        inline=False,
    )
    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    for word in FILTERED_WORDS:
        if word in message.content:
            await message.delete()
            return
    if message.author == bot.user:
        return
    guild = extract_guild(message)
    msg = extract_message(message)
    user = extract_user(message)
    if user.isBot == False:
        attribute_msg_xp(user, guild.guild_id)
    # if message.content.startswith(guild.prefix):
    #     await message.channel.send("Hello!")
    try:
        await bot.process_commands(message)
    except commands.CommandError as err:
        print(err)
        await message.channel.send(
            "Hey, what?! I don't know this command. Try a known command."
        )
    print("Message from {0.author}: {0.content}".format(message))


@bot.event
async def on_ready():
    logger.info("Logged on as {0}!".format(bot.user))


class Bot:
    def __init__(self):
        self.bot = bot

    def run(self):
        self.bot.run(config("TOKEN"))
