from models.channel import Channel
from models.message import Message
from models.guild import Guild
from models.user import User

def extract_message(message):
    return Message(message.id,message.content,message.created_at,message.mentions,message.embeds,message.reactions,message.channel.id,message.channel.name,message.channel.nsfw,message.author.bot,message.guild.id,message.guild.name,message.author.id,message.author.name,message.author.nick)

def extract_channel(message):
    return Channel(message.channel.id, message.channel.name, message.channel.nsfw,message.channel.news,message.channel.category_id)

def extract_guild(message):
    return Guild(message.guild.id, message.guild.name)
def extract_user(message):
    return User(message.author.id, message.author.name, message.author.nick, message.author.bot)
    
# <Message id=950959298576539658 
# channel=<TextChannel id=699699656241840129 name='testes' position=7 nsfw=False news=False category_id=704855564580028507> 
# type=<MessageType.default: 0> 
# author=<Member id=687670706959679576 name='RodCordeiro' discriminator='2122' bot=False nick='Darth RodC0rdeiro' 
# guild=<Guild id=697180940127961128 name='Darth Code' shard_id=None chunked=True member_count=9>> 
# flags=<MessageFlags value=0>>