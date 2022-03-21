import logging
import discord
from discord import Message
from discord.channel import TextChannel
from discord.ext import commands as DiscCommand
from datetime import datetime


from .bot import bot
from .reaction import ProcessCommands
from .utils import Embed, GENERAL_CHANNEL_NAMES, Clients
from models import Guild, Channel, User, Message
from .utils.functions import (
    extract_guild,
    extract_message,
    extract_user,
    attribute_msg_xp,
    filtered_words,
)
from db import Database


logger = logging.getLogger(__name__)
db = Database()
clients = Clients()
reactions = ProcessCommands()


@bot.event
async def on_raw_reaction_add(
    self: discord.RawReactionActionEvent,
    reaction: discord.RawReactionActionEvent = False,
):  # payload: discord.RawReactionActionEvent):
    """Gives a role based on a reaction emoji."""
    if self.member.bot == True:
        return
    print(self)
    guild = self.member.guild.id
    message = self.message_id
    processo = await db.has_process(guild, message)
    if processo is not None:
        value = await db.get_reaction(message, self.emoji.name)
        print(processo)
        print(value)
        if processo[0]["key"] == "trello_default_board":
            await reactions.trello_default_board(guild, value["value"])
            db.delete_process(processo[0]["id"])
        if processo[0]["key"] == "azure_setup_project":
            reactions.azure_setup_project(guild, value["value"])
            db.delete_process(processo[0]["id"])
        
    # <RawReactionActionEvent
    # message_id=953750434609234032
    # user_id=703264530079285268
    # channel_id=925735083313348618
    # guild_id=911248622421704704
    # emoji=<PartialEmoji animated=False name='🇰' id=None>
    # event_type='REACTION_ADD'
    # member=
    #   <Member id=703264530079285268 name='DMBot'  discriminator='5291' bot=True nick=None
    #   guild=<Guild id=911248622421704704 name='<DarkSe1d />' shard_id=None chunked=True member_count=11>>>

    # if self.message_id != settings_updater_message_id:
    #     return
    # print("valid message")
    # if self.user_id == bot.user.id:
    #     return
    # print("valid user")
    # guild = bot.get_guild(self.guild_id)
    # if guild is None:
    #     # Check if we're still in the guild and it's cached.
    #     return
    # print("valid guild")

    # try:
    #     for emoji in emoji_to_role:
    #         if emoji_to_role[emoji]['emoji'] == self.emoji:
    #             defaultBoard = emoji_to_role[emoji]['board']
    #             trello.defaultBoard = defaultBoard
    # except KeyError as err:
    # #     # If the emoji isn't the one we care about then exit as well.
    #     print(err)
    #     return


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
        description=f"To get started, do `{prefix}help` to see available commands",
    )
    embed.add_field(
        name="Support Server",
        value="Join our server at [discord.gg/poketwo](https://discord.gg/poketwo) for support.",
        inline=False,
    )
    await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    print("error on command: ", error)
    if isinstance(error, DiscCommand.CommandOnCooldown):
        logger.info(
            "Command cooldown hit",
            extra={"userid": ctx.author.id, "user": str(ctx.author)},
        )
        await ctx.message.add_reaction("\N{HOURGLASS}")
    if isinstance(error, Exception):
        logger.info(error)
        await ctx.message.add_reaction(discord.PartialEmoji(name="⬇️"))
        return await ctx.message.channel.send(f"Sorry but, some exception ocurred during the command. \n{error}")
    elif isinstance(error, DiscCommand.MaxConcurrencyReached):
        name = error.per.name
        suffix = "per %s" % name if error.per.name != "default" else "globally"
        plural = "%s times %s" if error.number > 1 else "%s time %s"
        fmt = plural % (error.number, suffix)
        await ctx.send(f"This command can only be used {fmt} at the same time.")
    elif isinstance(error, DiscCommand.NoPrivateMessage):
        await ctx.send("This command cannot be used in private messages.")
    elif isinstance(error, DiscCommand.DisabledCommand):
        await ctx.send("Sorry. This command is disabled and cannot be used.")
    elif isinstance(error, DiscCommand.BotMissingPermissions):
        missing = [
            f"`{perm.replace('_', ' ').replace('guild', 'server').title()}`"
            for perm in error.missing_permissions
        ]
        fmt = "\n".join(missing)
        message = f"💥 Err, I need the following permissions to run this command:\n{fmt}\nPlease fix this and try again."
        botmember = bot.user if ctx.guild is None else ctx.guild.get_member(bot.user.id)
        if ctx.channel.permissions_for(botmember).send_messages:
            await ctx.send(message)
    elif isinstance(error, DiscCommand.ConversionError):
        await ctx.send(error.original)
    elif isinstance(error, DiscCommand.MissingRequiredArgument):
        await ctx.send_help(ctx.command)
    elif isinstance(error, DiscCommand.CommandNotFound):
        return await ctx.channel.send(
            "Hey, what?! I don't know this command. Try a known command."
        )
    else:
        return


@bot.event
async def on_message(message: Message):
    await filtered_words(message)
    if message.author == bot.user:
        return
    if isinstance(message.channel, TextChannel):
        guild = extract_guild(message)
        user: User = extract_user(message)
        if user.isBot == False:
            await attribute_msg_xp(user, guild.guild_id)
            process = await db.has_process(guild=guild.guild_id, user=user.id)
            if process is not None:
                Now = datetime.now()
                expires = datetime.strptime(process[0]["expires"], "%Y-%m-%d %H:%M:%S")
                if Now > expires:
                    db.delete_process(process[0]["id"])
                else:
                    if process[0]["key"] == "azure_setup_token":
                        await reactions.azure_setup_token(message)
                        db.delete_process(process[0]["id"])
                    if process[0]["key"] == "azure_setup_org":
                        await reactions.azure_setup_org(message)
                        db.delete_process(process[0]["id"])
                
    # # if message.content.startswith(guild.prefix):
    #     await message.channel.send("Hello!")
    try:
        await bot.process_commands(message)
    except DiscCommand.CommandError as err:
        print(err)

    print("Message from {0.author}: {0.content}".format(message))


@bot.event
async def on_ready():
    logger.info("Logged on as {0}!".format(bot.user))