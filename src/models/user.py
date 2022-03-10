from db import Database

db = Database()

class User:
    def __init__(self, guild_id,user):
        self.id = user.id
        self.name = user.name
        self.avatar = user.avatar_url
        self.nick = user.nick
        self.isBot = user.bot
        self.discriminator = user.discriminator
        if user.bot == False:
            userData = db.has_user(guild_id,user)
            if userData:
                user_level = 0
                level_requirement = 0
                while userData['XP'] > level_requirement:
                    user_level += 1
                    level_requirement = round((user_level ** 2) - user_level + 15 + level_requirement)                
                self.xp = userData['XP']
                self.level = user_level
                self.level_requirement = level_requirement
