from decouple import config
import sqlite3


class Database:
    def __init__(self):
        self.__init__ = self
        self.con = sqlite3.connect("./src/db/database.db")
        self.cursor = self.con.cursor()

    def prepare(self):
        with open("./src/db/script.sql", "r") as script:
            commands = script.read()
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
                "LINKED_BY": guild[5]
            }
        return False
