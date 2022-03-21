import time
import logging
from decouple import config
import discord
from discord.ext import commands
import random
from Trello import Trello
from db import Database



# @commands.guild_only()
# @bot.command(name="boards",help="Returns trello boards")
# async def getBoards(ctx):
#     boards = trello.getBoards()    
#     message = '\n'.join([board.name for board in boards])
#     await ctx.send('Hey :regional_indicator_b:, here\'s your trello boards: {}'.format(message))

# @commands.guild_only()
# @bot.command(name="lists",help="Returns trello boards")
# async def getLists(ctx):
#     try:
#         trello.about()
#         boards = trello.getLists()
#         message = '\n'.join([board.name for board in boards])
#         await ctx.send('Hey :regional_indicator_b:, here\'s your trello boards: {}'.format(message))
#     except Exception as err:
#         print(err)
#         await ctx.send('Sorry bro, couldnt process due to  {}'.format(err))


# @bot.command(name="default",help="Returns trello boards")
# async def defaultBoard(ctx):
#     global settings_updater_message_id
#     global emoji_to_role
#     boards = trello.getBoards()
#     i = 0
#     text = '\n'
#     for board in boards:
#         emoji_to_role[board.name] = {
#             "emoji": discord.PartialEmoji(name=emojis[i]),
#             "board" : board
#         }
#         text += f"{emojis[i]} > {board.name} \n\n"
#         i += 1
#     message = await ctx.send('--------------------------------------\nHey , here\'s your trello boards: \n{}'.format(text))
#     # guild = await bot.fetch_guild(message.author.guild.id)
#     settings_updater_message_id = message.id
#     for board in boards:
#         try:
#             await message.add_reaction(emoji_to_role[board.name]['emoji'])        
#         # emoji_to_role[discord.PartialEmoji(name=)] = board.id
#         except discord.Forbidden as err:
#             print('failed to react due to forbidden',err)
#         except discord.InvalidArgument as err:
#             print('failed to react due to invalid argument',err)    
#         except discord.NotFound as err:
#             print('failed to react due to not found',err)    
#         except discord.HTTPException as err:
#             print('failed to react due to HTTPException',err)    
#     # for board in boards:
#     #     emoji = emojis[i]
        
#         # print(emoji)
        
#         # try:
#         #     await message.add_reaction("THUMBS UP SIGN")        
#         # # emoji_to_role[discord.PartialEmoji(name=)] = board.id
#         # except discord.Forbidden as err:
#         #     print('failed to react due to forbidden',err)
#         # except discord.InvalidArgument as err:
#         #     print('failed to react due to invalid argument',err)    
#         # except discord.NotFound as err:
#         #     print('failed to react due to not found',err)    
#         # except discord.HTTPException as err:
#         #     print('failed to react due to HTTPException',err)    
#         # i += 1 
    


# @bot.command()
# async def roll(ctx, dice: str):
#     """Rolls a dice in NdN format."""
#     print('called this fucking command')
#     try:
#         rolls, limit = map(int, dice.split('d'))
#     except Exception:
#         await ctx.send('Format has to be in NdN!')
#         return
#     result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
#     print("\nctx-=>",ctx,"\ndice-=>",dice,"\nrolls-=>",rolls,"\nlimit-=>",limit,"\nresult-=>",result)
#     await ctx.send(result)

# @bot.command()
# async def ping(ctx):
#     """ Returns pong """
#     await ctx.channel.send("pong")

# @bot.event
# async def on_ready():
#     logger.info('Logged on as {0}!'.format(bot.user))

# @bot.event
# async def on_member_join(member):
#     guild = member.guild
#     if guild.system_channel is not None:
#         to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
#         await guild.system_channel.send(to_send)

# @bot.event
# async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent = False):# payload: discord.RawReactionActionEvent):
#         """Gives a role based on a reaction emoji."""
#         print(self)    
#         # Make sure that the message the user is reacting to is the one we care about.
#         # <RawReactionActionEvent 
#         # message_id=947852175227383839 
#         # user_id=793101939546128394 
#         # channel_id=699699656241840129 
#         # guild_id=697180940127961128 
#         # emoji=<PartialEmoji animated=False name='👍' id=None> 
#         # event_type='REACTION_ADD' 
#         # member=<Member id=793101939546128394 name='Wheatley' discriminator='6125' bot=True nick=None 
#         #     guild=<Guild id=697180940127961128 name='Darth Code' shard_id=None chunked=True member_count=10>>>
#         if self.message_id != settings_updater_message_id:
#             return
#         print("valid message")    
#         if self.user_id == bot.user.id:
#             return
#         print("valid user")    
#         guild = bot.get_guild(self.guild_id)
#         if guild is None:
#             # Check if we're still in the guild and it's cached.
#             return
#         print("valid guild")    
        
#         try:
#             for emoji in emoji_to_role:
#                 if emoji_to_role[emoji]['emoji'] == self.emoji:
#                     defaultBoard = emoji_to_role[emoji]['board']
#                     trello.defaultBoard = defaultBoard
#         except KeyError as err:
#         #     # If the emoji isn't the one we care about then exit as well.
#             print(err)
#             return
        
@bot.event
async def on_message(message):
    # for word in filtered_words:
    #     if word in message.content:
    #         await message.delete()
    #         return
    print(message)
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

