import discord
from .constants import (
    EMOJIS,
    FILTERED_WORDS,
    NUMBER_REACTIONS,
    LETTER_REACTIONS,
    GENERAL_CHANNEL_NAMES,
)
from .clients import Clients


class Embed(discord.Embed):
    def __init__(self, **kwargs):
        color = kwargs.pop("color", 0x9CCFFF)
        super().__init__(**kwargs, color=color)
