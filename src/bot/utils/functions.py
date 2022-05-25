import json
from discord import Message, Colour
from azure.devops.v5_1.work_item_tracking.models import WorkItemReference

from models.channel import Channel
from models.message import Message as MessageModel
from models.guild import Guild
from models.user import User
from db import Database
from Azure import Azure
import random
import re
from . import FILTERED_WORDS, Clients, Embed

db = Database()
clients = Clients()

def get_color(type:str):
    if type == 'Bug':
        return Colour.red()
    if type == 'Feature':
        return Colour.purple()
    if type == 'task':
        return Colour.gold()
    if type == 'Product Backlog Item':
        return Colour.red()
    if type == 'Bug':
        return Colour.red()
    if type == 'Bug':
        return Colour.red()
    if type == 'Bug':
        return Colour.red()
    return Colour.blurple()
 

async def filtered_words(message: Message):
    for bad_word in FILTERED_WORDS:
        regex = re.compile(bad_word, re.IGNORECASE)
        for word in message.content.split(" "):
            match = regex.match(word)
            if match is not None:
                await message.delete()


async def has_azure_task(message: Message):
    for word in message.content.split(" "):
        regex = re.compile("^#\d{3,}", re.IGNORECASE)
        match = regex.match(word)
        # print(word,match)
        if match is not None:
            try:
                guild = extract_guild(message)
                client: Azure = clients.get_client("azure", guild.guild_id)
                task = client.get_task(match)
                await message.channel.send("oi")
            except Exception as err:
                if err.args[0] == "No clients available":
                    azure = db.get_azure_config(guild.guild_id)
                    client = Azure(
                        azure["TOKEN"],
                        azure["ORGANIZATION"],
                        azure["DEFAULT_PROJECT"]
                        if azure["DEFAULT_PROJECT"] is not None
                        else None,
                    )
                    clients.add_client("azure", guild.guild_id, client)
                    task: WorkItemReference = client.get_task(
                        str(word).replace("#", "")
                    )
                    data = task.serialize()["fields"]
                    print(data)
                    embed = Embed(
                        title=data["System.Title"], 
                        description=data["System.Description"] if data["System.Description"] else "",
                        url=task.url,
                        color=get_color(data['System.WorkItemType'])
                    )
                    # embed.
                    embed.set_footer(
                        text=task.url,  # f"[{data['System.WorkItemType']}]({task.url})",
                        icon_url="https://cdn.iconscout.com/icon/free/png-256/bug-fixing-seo-web-repair-virus-insect-spider-10-8829.png",
                    )
                    embed.set_thumbnail(
                        url="https://cdn.iconscout.com/icon/free/png-256/bug-fixing-seo-web-repair-virus-insect-spider-10-8829.png"
                    )
                    return await message.channel.send(embed=embed)
                print("err", err.args[0])
                pass


def extract_message(message):
    return Message(
        message.id,
        message.content,
        message.created_at,
        message.mentions,
        message.embeds,
        message.reactions,
        message.channel.id,
        message.channel.name,
        message.channel.nsfw,
        message.author.bot,
        message.guild.id,
        message.guild.name,
        message.author.id,
        message.author.name,
        message.author.nick,
    )


def extract_channel(message):
    return Channel(
        message.channel.id,
        message.channel.name,
        message.channel.nsfw,
        message.channel.news,
        message.channel.category_id,
    )


def extract_guild(message):
    return Guild(message.guild.id, message.guild.name)


def extract_user(message):
    return User(message.guild.id, message.author)


async def attribute_msg_xp(user, guildId):
    data = db.has_user(guildId, user)
    if data:
        xp = data["XP"] + random.randint(5, 15)
        await db.increase_xp(guildId, user.id, xp)


# <Message id=950959298576539658
# channel=<TextChannel id=699699656241840129 name='testes' position=7 nsfw=False news=False category_id=704855564580028507>
# type=<MessageType.default: 0>
# author=<Member id=687670706959679576 name='RodCordeiro' discriminator='2122' bot=False nick='Darth RodC0rdeiro'
# guild=<Guild id=697180940127961128 name='Darth Code' shard_id=None chunked=True member_count=9>>
# flags=<MessageFlags value=0>>
