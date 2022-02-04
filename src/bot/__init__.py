import logging
from decouple import config
import discord

logger = logging.getLogger(__name__)

class Client(discord.Client):
    async def on_ready(self):
        logger.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!hello'):
            await message.channel.send('Hello!')
        print('Message from {0.author}: {0.content}'.format(message))

class Bot:
    def __init__(self):
        self.client = Client()
        self.client.run(config('TOKEN'))

