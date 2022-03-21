import logging
from decouple import config

from .reaction import ProcessCommands
from .commands import profile
from .bot import bot
from .events import on_ready, on_message

logger = logging.getLogger(__name__)

class Bot:
    def __init__(self):
        self.bot = bot

    def run(self):
        self.bot.run(config("TOKEN"))
