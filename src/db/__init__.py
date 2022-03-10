from decouple import config
import sqlite3
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.__init__ = self
        logger.info("Connecting to database")
        self.con = sqlite3.connect("./src/db/database.db")
        self.cursor = self.con.cursor()

    def prepare(self):
        with open("./src/db/script.sql", "r") as script:
            commands = script.read()
            logger.info("Running db configuration script")
            self.con.executescript(commands)
            self.con.commit()

    def get_prefixes(self, guild_id):
        self.cursor.execute(
            f"SELECT guild_id, prefix FROM KH_TB_GUILDS WHERE guild_id = '{guild_id}'"
        )
        prefix = self.cursor.fetchone()
        return {"prefix": prefix[1]}

    def get_guild(self, guild_id):
        self.cursor.execute(f"SELECT * FROM KH_TB_GUILDS WHERE guild_id = '{guild_id}'")
        guild = self.cursor.fetchone()
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
        self.cursor.execute(
            f"SELECT ID,GUILD_ID,TOKEN,DEFAULT_BOARD,LINKED_AT,LINKED_BY FROM KH_TB_TRELLO WHERE GUILD_ID = '{guild_id}'"
        )
        guild = self.cursor.fetchone()
        if guild:
            return {
                "ID": guild[0],
                "GUILD_ID": guild[1],
                "TOKEN": guild[2],
                "DEFAULT_BOARD": guild[3],
                "LINKED_AT": guild[4],
                "LINKED_BY": guild[5],
            }
        return False

    def set_trello_config(self, guild_id, token, user_id):
        self.cursor.execute(
            f"INSERT INTO KH_TB_TRELLO (GUILD_ID,TOKEN,LINKED_BY) VALUES ('{guild_id}','{token}','{user_id}')"
        )
        self.con.commit()
        return

    def has_user(self, guild_id, user):
        # print("has_user->user", user)
        self.cursor.execute(
            f"SELECT ID,GUILD_ID,USER_ID,NAME,DISCRIMINATOR,XP FROM KH_TB_USERS WHERE GUILD_ID = '{guild_id}' AND USER_ID = '{user.id}'"
        )
        data = self.cursor.fetchone()
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
        self.cursor.execute(
            f"INSERT INTO KH_TB_USERS (GUILD_ID,USER_ID,NAME,DISCRIMINATOR) VALUES ('{guild_id}','{user.id}','{user.name}','{user.discriminator}')"
        )
        self.con.commit()
        self.cursor.execute(
            f"SELECT ID,GUILD_ID,USER_ID,NAME,DISCRIMINATOR,XP FROM KH_TB_USERS WHERE GUILD_ID = '{guild_id}' AND USER_ID = '{user.id}'"
        )
        user = self.cursor.fetchone()
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

    def increase_xp(self, guild_id, user_id, xp):
        self.cursor.execute(
            f"UPDATE KH_TB_USERS SET XP = {xp} WHERE GUILD_ID = '{guild_id}' AND USER_ID = '{user_id}';"
        )
        self.con.commit()
