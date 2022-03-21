import logging
from Trello import Trello
from Azure import Azure
from db import Database
from .utils import Clients
import discord
from discord import Message
from .utils import Embed, LETTER_REACTIONS, Clients
from .utils.functions import (
    extract_guild,
    extract_message,
    extract_user,
    attribute_msg_xp,
    filtered_words,
)

logger = logging.getLogger(__name__)
db = Database()
clients = Clients()


class ProcessCommands:
    def __init__(self):
        self.__init__ = self
        logger.info('Reactions commands ready')

    async def trello_default_board(self, guild, board):
        db.set_trello_board(guild, board)
    async def azure_setup_token(self,message: Message):
        text = message.content
        guild = extract_guild(message)
        user = extract_user(message)
        azure = db.get_azure_config(guild.guild_id)
        if azure is None:
            db.set_azure_token(guild.guild_id,text,user.id)
        else:
            db.update_azure_token(guild.guild_id,text,user.id)
        await message.delete()
        await db.create_process(
            guild.guild_id,
            user=user.id,
            msg=message.id,
            processKey="azure_setup_org",
        )
        return await message.channel.send('Perfeito, token armazenado com sucesso! No Azure DevOps é possível ser membro de mais de uma organização, porém no momento eu atendo apenas uma organização, portanto preciso que me informe o nome da organização.\n*Como pegar o nome da organização?*\n> No link do azure devops, https://dev.azure.com/aqui_esta_sua_organiazação/.\n\nPor favor, informe sua organização para prosseguirmos.')
        # 6m7danljhamm4xx2avwgxn6mkjoenz4nc3v5rt6y5oidysxofntq
    async def azure_setup_org(self,message: Message):
        text = message.content
        guild = extract_guild(message)
        user = extract_user(message)
        db.set_azure_organization(guild.guild_id, text)
        await message.delete()
        azure = db.get_azure_config(guild.guild_id)
        client = Azure(azure['TOKEN'],text)
        clients.add_client(
            "azure",
            guild.guild_id,
            client
        )
        list = []
        index = 0
        idx = 0
        for project in client.projects:
            list.append(f"{LETTER_REACTIONS[index]} {project.name}")
            index += 1
        embed = Embed(
            title="Aqui estão seus projetos do Azure DevOps! Por favor, selecione o projeto padrão reagindo aos emojis",
            description="\n".join(list),
        )
        msg: Message = await message.channel.send(embed=embed)
        processo = await db.create_process(
            guild.guild_id,
            user=user.id,
            msg=msg.id,
            processKey="azure_setup_project",
        )
        while idx < index:
            await msg.add_reaction(discord.PartialEmoji(name=LETTER_REACTIONS[idx]))
            await db.save_reaction(
                guild.guild_id, processo, LETTER_REACTIONS[idx], client.projects[idx].id
            )
            idx += 1

    def azure_setup_project(self,guild,project):
        db.set_azure_project(guild,project)
