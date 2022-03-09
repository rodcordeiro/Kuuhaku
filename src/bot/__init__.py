import logging
from decouple import config
import discord
from discord.ext import commands
import random
from Trello import Trello
from db import Database
from functions import extract_message, extract_user, extract_channel, extract_guild

logger = logging.getLogger(__name__)

description="""# < Kuuhaku /> bot
"""
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix=config('PREFIX'), description=description, intents=intents)
trello = Trello()
db = Database()



filtered_words = ['buceta']
defaultBoard = ''
settings_updater_message_id = 0 # ID of the message that can be reacted to to add/remove a role.
emojis=[
    "1️⃣",
    '2️⃣',
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣",
    "🔟",
    "⬅️",
    "↖️",
    "⬆️",
    "↗️",
    "➡️",
    "↘️",
    "⬇️",
    "↙️"
]

emoji_to_role = {
}
# discord.PartialEmoji(name=':\N{regional_indicator_a}:'): 0, # ID of the role associated with unicode emoji '🔴'.

trello = Trello()


@bot.event
async def on_message(message):
    for word in filtered_words:
        if word in message.content:
            await message.delete()
            return
    guild = extract_guild(message)
    print(guild.prefix)
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    try:
        await bot.process_commands(message)
    except Exception as err:
        print(err)
        await message.channel.send('Hey, what?! I don\'t know this command. Try a known command.')
    print('Message from {0.author}: {0.content}'.format(message))

# <Message id=950959298576539658 
# channel=<TextChannel id=699699656241840129 name='testes' position=7 nsfw=False news=False category_id=704855564580028507> 
# type=<MessageType.default: 0> 
# author=<Member id=687670706959679576 name='RodCordeiro' discriminator='2122' bot=False nick='Darth RodC0rdeiro' 
# guild=<Guild id=697180940127961128 name='Darth Code' shard_id=None chunked=True member_count=9>> 
# flags=<MessageFlags value=0>>

# <Message id=950959942410600509 
# channel=<TextChannel id=925735083313348618 name='spammar' position=6 nsfw=False news=False category_id=911248622421704705> 
# type=<MessageType.default: 0> 
# author=<Member id=687670706959679576 name='RodCordeiro' discriminator='2122' bot=False nick=None 
# guild=<Guild id=911248622421704704 name='<Undefined />' shard_id=None chunked=True member_count=9>> 
# flags=<MessageFlags value=0>>
class Bot:
    def __init__(self):
        self.bot = bot
    def run(self):
        self.bot.run(config('TOKEN'))
