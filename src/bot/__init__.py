import logging
from decouple import config
import discord
from discord.ext import commands
import random
from Trello import Trello

logger = logging.getLogger(__name__)

description="""# < Kuuhaku /> bot
"""

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=config('PREFIX'), description=description, intents=intents)
# trello = Trello()

@bot.command(name="test",help="Provides some test functionallity")
async def test(ctx, arg1, arg2):
    board = trello.getBoards()
    print(board)
    await ctx.send('The Trello board name is {}'.format(board[0].name))

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    print('called this fucking command')
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    print("\nctx-=>",ctx,"\ndice-=>",dice,"\nrolls-=>",rolls,"\nlimit-=>",limit,"\nresult-=>",result)
    await ctx.send(result)
@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.event
async def on_ready():
    logger.info('Logged on as {0}!'.format(bot.user))

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    await bot.process_commands(message)
    print('Message from {0.author}: {0.content}'.format(message))



class Bot:
    def __init__(self):
        self.bot = bot
        # self.trello = Trello()
        # board = self.trello.getBoards()
        # print(board)
        # lists = self.trello.getLists(board[0])
        # print('lists',lists,lists[0].id)
        # cards = self.trello.getList(board[0],lists[0].id)
        self.bot.run(config('TOKEN'))

