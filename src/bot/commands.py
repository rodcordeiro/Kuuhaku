import random
import discord
from discord.ext import commands as DiscCommand
from azure.devops.v5_1.git.models import GitRepository


from .bot import bot
from .reaction import ProcessCommands
from models import Guild, Channel, User, Message
from .utils import Embed, LETTER_REACTIONS, Clients
from .utils.functions import (
    extract_guild,
    extract_message,
    extract_user,
    attribute_msg_xp,
    filtered_words,
)
from db import Database
from Trello import Trello
from Azure import Azure

db = Database()
clients = Clients()
reactions = ProcessCommands()


@DiscCommand.guild_only()
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
@DiscCommand.guild_only()
@DiscCommand.check_any(
    DiscCommand.is_owner(), DiscCommand.has_permissions(administrator=True)
)
async def settings(ctx: DiscCommand.Context):
    """Allows server configuration."""
    if ctx.invoked_subcommand is None:
        guild = extract_guild(ctx)
        await ctx.channel.send(
            f"<@{ctx.author.id}> please, use one of the subcommands. See below your options"
        )
        await ctx.send_help("settings")
        return


@settings.group(pass_context=True)
@DiscCommand.check_any(
    DiscCommand.is_owner(), DiscCommand.has_permissions(administrator=True)
)
async def set(ctx):
    """Used to define server configurations"""
    if ctx.invoked_subcommand is None:
        guild = extract_guild(ctx)
        await ctx.channel.send(
            f"<@{ctx.author.id}> please, use one of the subcommands. Use `{guild.prefix}help settings set` for more details."
        )
        return await ctx.send_help("settings set")


@settings.group(pass_context=True)
@DiscCommand.guild_only()
@DiscCommand.check_any(
    DiscCommand.is_owner(), DiscCommand.has_permissions(administrator=True)
)
async def get(ctx):
    """Used to retrieve server configurations"""
    if ctx.invoked_subcommand is None:
        guild = extract_guild(ctx)
        await ctx.channel.send(
            f"<@{ctx.author.id}> please, use one of the subcommands. Use `{guild.prefix}help settings get` for more details."
        )
        return await ctx.send_help("settings get")


@DiscCommand.guild_only()
@get.group(pass_context=True)
async def trello(ctx):
    config = db.get_trello_config(ctx.guild.id)
    if config == False:
        return await ctx.channel.send("There's no trello account linked yet.")
    embed = Embed(
        title="Aqui está sua configuração do trello",
        description=f"<@{ctx.author.id}> aqui estão as configurações referentes ao link do servidor com o Trello",
    )
    embed.set_thumbnail(
        url="https://cdn.icon-icons.com/icons2/3041/PNG/512/trello_logo_icon_189227.png"
    )
    embed.add_field(name="Linked by", value=f"<@{config['LINKED_BY']}>", inline=True)
    embed.add_field(name="Linked at", value=config["LINKED_AT"], inline=True)
    embed.add_field(name="Default board", value=config["DEFAULT_BOARD"], inline=False)
    return await ctx.channel.send(embed=embed)


@set.group(pass_context=True)
async def trello_token(ctx: DiscCommand.Context, value=None):
    if value is None:
        return await ctx.channel.send(
            f"<@{ctx.author.id}> You must provide trello token."
        )
    user = extract_user(ctx)
    guild = extract_guild(ctx)
    config = db.get_trello_config(guild.guild_id)
    if config is False:
        db.set_trello_token(guild.guild_id, value, user.id)
        await ctx.message.delete()
        return await ctx.channel.send(
            f"All done <@{user.id}>! Use `{guild.prefix}settings get trello` to view the data."
        )
    db.update_trello_token(guild.guild_id, value, user.id)
    await ctx.message.delete()
    return await ctx.channel.send(
        f"All done <@{user.id}>! Use `{guild.prefix}settings get trello` to view the data."
    )


@set.group(pass_context=True)
async def trello_boards(ctx: DiscCommand.Context):
    guild: Guild = extract_guild(ctx)
    process = await db.has_process(guild=guild.guild_id, user=ctx.author.id)
    if process is not None:
        return await ctx.channel.send(
            f"You're already in another command, please. Try again later or run {guild.prefix}abort to abort any pending process."
        )
    trello_token = db.get_trello_config(guild.guild_id)
    if trello_token == False:
        return await ctx.channel.send("There's no trello account linked yet.")
    client = Trello(trello_token["TOKEN"])
    clients.add_client(
        "trello",
        guild.guild_id,
        client,
    )
    boards = client.get_boards()
    list = []
    index = 0
    idx = 0
    for board in boards:
        list.append(f"{LETTER_REACTIONS[index]} {board.name}")
        index += 1
    embed = Embed(
        title="Aqui estão seus quadros do Trello! Por favor, selecione o quadro padrão reagindo aos emojis",
        description="\n".join(list),
    )
    msg: Message = await ctx.channel.send(embed=embed)
    processo = await db.create_process(
        guild.guild_id,
        user=ctx.author.id,
        msg=msg.id,
        processKey="trello_default_board",
    )
    while idx < index:
        await msg.add_reaction(discord.PartialEmoji(name=LETTER_REACTIONS[idx]))
        await db.save_reaction(
            guild.guild_id, processo, LETTER_REACTIONS[idx], boards[idx].name
        )
        idx += 1
    await ctx.message.delete()


@get.group(pass_context=True)
async def azure(ctx):
    global projeto
    projeto = None
    client = None
    config = db.get_azure_config(ctx.guild.id)
    if config == False:
        return await ctx.channel.send("There's no azure account linked yet.")
    try:
        client: Azure = clients.get_client("azure", ctx.guild.id)
        print(client)
    except:
        pass
    if client is not None:
        for project in client.projects:
            if project.id == config["DEFAULT_PROJECT"]:
                projeto = project
    embed = Embed(
        title="Aqui está sua configuração do azure",
        description=f"<@{ctx.author.id}> aqui estão as configurações referentes ao link do servidor com o Azure",
    )
    embed.set_thumbnail(
        url="https://cdn.iconscout.com/icon/free/png-256/azure-devops-3628645-3029870.png"
    )
    embed.add_field(name="Linked by", value=f"<@{config['LINKED_BY']}>", inline=True)
    embed.add_field(name="Linked at", value=config["LINKED_AT"], inline=True)
    embed.add_field(name="Organization", value=config["ORGANIZATION"], inline=True)
    if projeto is not None:
        embed.add_field(name="Default Project", value=projeto["name"], inline=True)
    return await ctx.channel.send(embed=embed)


@set.group(pass_context=True)
async def azure(ctx: DiscCommand.Context):
    guild = extract_guild(ctx)
    process = await db.has_process(guild=guild.guild_id, user=ctx.author.id)
    if process is not None:
        return await ctx.channel.send(
            f"You're already in another command, please. Try again later or run {guild.prefix}abort to abort any pending process."
        )
    processo = await db.create_process(
        guild.guild_id,
        user=ctx.author.id,
        msg=ctx.message.id,
        processKey="azure_setup_token",
    )
    return await ctx.channel.send(
        f"Let's setup your azure integration <@{ctx.author.id}>! Please, inform your personal access token."
    )


@DiscCommand.guild_only()
@bot.command()
async def abort(ctx):
    guild = extract_guild(ctx)
    user = extract_user(ctx)
    processos = await db.has_process(guild.guild_id, user=user.id)
    for processo in processos:
        db.delete_process(processo["id"])
    return await ctx.channel.send(f"All process aborted. Thanks for your patience!")


@bot.group(pass_context=True)
async def trello(ctx):
    if ctx.invoked_subcommand is None:
        return await ctx.channel.send("Please, use one of the trello subcommands")
    guild = extract_guild(ctx)
    trello_token = db.get_trello_config(guild.guild_id)
    if trello_token == False:
        return await ctx.channel.send("There's no trello account linked yet.")
    clients.add_client(
        "trello",
        guild.guild_id,
        Trello(trello_token["TOKEN"], trello_token["DEFAULT_BOARD"]),
    )


@trello.group(pass_context=True)
async def boards(ctx):
    guild = extract_guild(ctx)
    trello = clients.get_client("trello", guild.guild_id)
    if trello is None:
        return await ctx.channel.send("There's no trello account linked yet.")
    boards = trello.get_boards()
    embed = Embed(
        title="Aqui estão seus quadros do Trello!",
        description="\n".join([board.name for board in boards]),
    )
    return await ctx.channel.send(embed=embed)


@trello.group(pass_context=True)
async def lists(ctx, board=None):
    guild = extract_guild(ctx)
    print(board)
    trello = clients.get_client("trello", guild.guild_id)
    if trello is None:
        return await ctx.channel.send("There's no trello account linked yet.")
    if trello.default_board is None:
        if board is None:
            return await ctx.channel.send(
                "You must define default board or pass the board name"
            )
    lists = trello.get_lists(board)
    embed = Embed(
        title=f"Aqui estão suas listas do quadro {board if board is not None else trello.default_board}",
        description="\n".join([list.name for list in lists]),
    )
    return await ctx.channel.send(embed=embed)


@trello.group(pass_context=True)
async def cards(ctx, board=None, list=None):
    guild = extract_guild(ctx)
    print(board)
    trello = clients.get_client("trello", guild.guild_id)
    if trello.default_board is None:
        if board is None:
            return await ctx.channel.send(
                "You must define default board or pass the board name"
            )
    cards = trello.get_cards(board, list)
    print(cards)
    return await ctx.channel.send("cards")


@bot.group(pass_context=True)
async def azure(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.channel.send("Please, use one of the Azure subcommands")
        return await ctx.send_help("azure")
    guild = extract_guild(ctx)
    azure = db.get_azure_config(guild.guild_id)
    if azure == False:
        return await ctx.channel.send("There's no Azure account linked yet.")
    client = Azure(azure["TOKEN"], azure["ORGANIZATION"], azure["DEFAULT_PROJECT"])
    clients.add_client("azure", guild.guild_id, client)


@azure.group(pass_context=True)
async def repos(ctx):
    guild = extract_guild(ctx)
    azure: Azure = clients.get_client("azure", guild.guild_id)
    if azure is None:
        return await ctx.channel.send("There's no Azure account linked yet.")
    def sortingCriteria(e: GitRepository):
        print(e)
        return e.name
    repos = azure.get_repositories()
    repos.sort(key=sortingCriteria)
    list = []
    index = 0
    while index < 20:
        repo: GitRepository = repos[index]
        list.append({"name": repo.name, "link": repo.web_url})
        index += 1
    # list.sort(key=sortingCriteria)
    embed = Embed(
        title="Aqui estão seus repositorios no azure!",
        description="\n".join([f"[{repo['name']}]({repo['link']})" for repo in list]), 
    )
    return await ctx.channel.send(embed=embed)

@azure.group(pass_context=True)
async def tasks(ctx):
    guild = extract_guild(ctx)
    azure: Azure = clients.get_client("azure", guild.guild_id)
    if azure is None:
        return await ctx.channel.send("There's no Azure account linked yet.")
    repos = azure.get_tasks()
    return await ctx.channel.send("tasks")
