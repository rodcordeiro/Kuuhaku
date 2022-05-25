from decouple import config
from sqlite3 import connect, Cursor, Connection
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


class Database:
    def __init__(self):
        self.__init__ = self
        logger.info("Connecting to database")
        self.con = connect("./src/db/database.db")

    def prepare(self):
        with open("./src/db/script.sql", "r") as script:
            commands = script.read()
            logger.info("Running db configuration script")
            self.con.executescript(commands)
            self.con.commit()

    def get_prefixes(self, guild_id):
        cursor = self.con.cursor()
        cursor.execute(
            f"SELECT guild_id, prefix FROM KH_TB_GUILDS WHERE guild_id = '{guild_id}'"
        )
        prefix = cursor.fetchone()
        cursor.close()
        return {"prefix": prefix[1]}

    @decorator
    def get_guild(self, guild_id):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM KH_TB_GUILDS WHERE guild_id = '{guild_id}'")
        guild = cursor.fetchone()
        cursor.close()
        if guild is None:
            return
        return {
            "id": guild[0],
            "guild_id": guild[1],
            "name": guild[2],
            "prefix": guild[3],
            "invited_at": guild[4],
        }

    def get_trello_config(self, guild_id):
        cursor = self.con.cursor()
        cursor.execute(
            f"SELECT T.ID,T.GUILD_ID,T.TOKEN,T.DEFAULT_BOARD,T.LINKED_AT,T.LINKED_BY, U.NAME FROM KH_TB_TRELLO T JOIN KH_TB_USERS U ON U.USER_ID = T.LINKED_BY WHERE T.GUILD_ID = '{guild_id}'"
        )
        guild = cursor.fetchone()
        cursor.close()
        if guild:
            return {
                "ID": guild[0],
                "GUILD_ID": guild[1],
                "TOKEN": guild[2],
                "DEFAULT_BOARD": guild[3],
                "LINKED_AT": guild[4],
                "LINKED_BY": guild[5],
                "USER": guild[6],
            }
        return False

    def set_trello_token(self, guild_id, token, user_id):
        cursor = self.con.cursor()
        response = cursor.execute(
            f"INSERT INTO KH_TB_TRELLO (GUILD_ID,TOKEN,LINKED_BY) VALUES ('{guild_id}','{token}','{user_id}')"
        )
        print("response", response)
        self.con.commit()
        cursor.close()
        return

    def update_trello_token(self, guild_id, token, user_id):
        cursor = self.con.cursor()
        cursor.execute(
            f"UPDATE KH_TB_TRELLO SET TOKEN='{token}', LINKED_BY = '{user_id}' WHERE GUILD_ID ='{guild_id}';"
        )
        self.con.commit()
        cursor.close()
        return

    def set_trello_board(self, guild_id, board):
        cursor = self.con.cursor()
        cursor.execute(
            f"UPDATE KH_TB_TRELLO SET DEFAULT_BOARD = '{board}' WHERE GUILD_ID = '{guild_id}'"
        )
        self.con.commit()
        cursor.close()
        return

    def get_azure_config(self, guild_id):
        cursor = self.con.cursor()
        cursor.execute(
            f"SELECT A.ID,A.GUILD_ID,A.TOKEN,A.DEFAULT_PROJECT,A.LINKED_AT,A.LINKED_BY,U.NAME,A.ORGANIZATION FROM KH_TB_AZURE A JOIN KH_TB_USERS U ON U.USER_ID = A.LINKED_BY WHERE A.GUILD_ID = '{guild_id}'"
        )
        guild = cursor.fetchone()
        cursor.close()
        if guild:
            return {
                "ID": guild[0],
                "GUILD_ID": guild[1],
                "TOKEN": guild[2],
                "ORGANIZATION": guild[7],
                "DEFAULT_PROJECT": guild[3],
                "LINKED_AT": guild[4],
                "LINKED_BY": guild[5],
                "USER": guild[6],
            }
        return False

    def set_azure_token(self, guild_id, token, user_id):
        cursor = self.con.cursor()
        cursor.execute(
            f"INSERT INTO KH_TB_AZURE (GUILD_ID,TOKEN,LINKED_BY) VALUES ('{guild_id}','{token}','{user_id}')"
        )
        self.con.commit()
        cursor.close()
        return

    def update_azure_token(self, guild_id, token, user_id):
        cursor = self.con.cursor()
        cursor.execute(
            f"UPDATE KH_TB_AZURE SET TOKEN = '{token}', LINKED_BY='{user_id}', LINKED_AT = '{datetime.now()}' WHERE GUILD_ID = '{guild_id}';"
        )
        self.con.commit()
        cursor.close()
        return

    def set_azure_organization(self, guild_id, organization):
        cursor = self.con.cursor()
        cursor.execute(
            f"UPDATE `KH_TB_AZURE` SET `ORGANIZATION` = '{organization}' WHERE `GUILD_ID` = '{guild_id}';"
        )
        self.con.commit()
        cursor.close()
        return

    def set_azure_project(self, guild_id, project):
        cursor = self.con.cursor()
        cursor.execute(
            f"UPDATE `KH_TB_AZURE` SET `DEFAULT_PROJECT` = '{project}' WHERE `GUILD_ID` = '{guild_id}';"
        )
        self.con.commit()
        cursor.close()
        return

    def has_user(self, guild_id, user):
        cursor = self.con.cursor()
        cursor.execute(
            f"SELECT ID,GUILD_ID,USER_ID,NAME,DISCRIMINATOR,XP FROM KH_TB_USERS WHERE GUILD_ID = '{guild_id}' AND USER_ID = '{user.id}'"
        )
        data = cursor.fetchone()
        cursor.close()
        if data:
            return {
                "ID": data[0],
                "GUILD_ID": data[1],
                "USER_ID": data[2],
                "NAME": data[3],
                "DISCRIMINATOR": data[4],
                "XP": data[5],
            }
        return self.create_user(guild_id, user)

    def create_user(self, guild_id, user):
        cursor = self.con.cursor()
        cursor.execute(
            f"INSERT INTO KH_TB_USERS (GUILD_ID,USER_ID,NAME,DISCRIMINATOR) VALUES ('{guild_id}','{user.id}','{user.name}','{user.discriminator}')"
        )
        self.con.commit()
        cursor.execute(
            f"SELECT ID,GUILD_ID,USER_ID,NAME,DISCRIMINATOR,XP FROM KH_TB_USERS WHERE GUILD_ID = '{guild_id}' AND USER_ID = '{user.id}'"
        )
        user = cursor.fetchone()
        cursor.close()
        if user:
            return {
                "ID": user[0],
                "GUILD_ID": user[1],
                "USER_ID": user[2],
                "NAME": user[3],
                "DISCRIMINATOR": user[4],
                "XP": user[5],
            }

        return False

    async def increase_xp(self, guild_id, user_id, xp):
        cursor = self.con.cursor()
        cursor.execute(
            f"UPDATE KH_TB_USERS SET XP = {xp} WHERE GUILD_ID = '{guild_id}' AND USER_ID = '{user_id}';"
        )
        self.con.commit()
        cursor.close()

    async def create_process(self, guild, msg, processKey, user=None, stage=0):
        cursor = self.con.cursor()
        identifier = uuid.uuid4()
        cursor.execute(
            f"INSERT INTO KH_TB_PROCESSOS (ID,GUILD,USER,MSG,KEY,STAGE) VALUES ('{identifier}','{guild}','{user}','{msg}','{processKey}','{stage}')"
        )

        self.con.commit()
        cursor.close()
        return identifier

    async def has_process(self, guild, msg="", user=""):
        cursor = self.con.cursor()
        cursor.execute(
            f"SELECT ID,KEY,STAGE,USER,EXPIRES FROM KH_TB_PROCESSOS WHERE GUILD = '{guild}' AND MSG = '{msg}' OR GUILD = '{guild}' AND USER = '{user}'"
        )
        id = cursor.fetchall()
        result = []
        for value in id:
            result.append(
                {
                    "id": value[0],
                    "key": value[1],
                    "stage": value[2],
                    "user": value[3],
                    "expires": value[4],
                }
            )

        if id:
            return result
        cursor.close()

    def delete_process(self, process_id):
        cursor = self.con.cursor()
        cursor.execute(f"DELETE FROM KH_TB_REACTIONS WHERE PROCESSO = '{process_id}'")
        cursor.execute(f"DELETE FROM KH_TB_PROCESSOS WHERE ID = '{process_id}'")
        self.con.commit()
        cursor.close()

    async def save_reaction(self, guild, process, emoji, value):
        cursor = self.con.cursor()
        cursor.execute(
            f"INSERT INTO KH_TB_REACTIONS (GUILD,PROCESSO,EMOJI,VALUE) VALUES ('{guild}','{process}','{emoji}','{value}');"
        )
        self.con.commit()
        cursor.close()

    async def get_reaction(self, message, reaction):
        cursor = self.con.cursor()
        cursor.execute(
            f"SELECT R.EMOJI, R.VALUE FROM KH_TB_REACTIONS R JOIN KH_TB_PROCESSOS P ON P.ID = R.PROCESSO WHERE P.MSG = '{message}' AND R.EMOJI = '{reaction}'"
        )
        result = cursor.fetchone()
        cursor.close()
        return {"emoji": result[0], "value": result[1]}
