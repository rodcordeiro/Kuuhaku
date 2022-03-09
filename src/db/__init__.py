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

    def get_guild(self, guild_id):
        self.cursor.execute(f"SELECT * FROM KH_TB_GUILDS WHERE guild_id = '{guild_id}'")
        guild = self.cursor.fetchone()
        return {"id": guild[0], "guild_id": guild[1], "name": guild[2], "prefix": guild[3],"invited_at":guild[4]}
    