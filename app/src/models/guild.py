from db import Database

db = Database()


class Guild:
    def __init__(self, guild_id, guild_name):
        self.guild_id = guild_id
        self.guild_name = guild_name
        data = db.get_guild(guild_id)
        self.prefix = data['prefix']
        self.invited_at = data['invited_at']
