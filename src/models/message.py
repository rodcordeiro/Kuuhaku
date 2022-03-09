class Message:
    def __init__(self,message_id,text,date,mentions,embeds,reactions,channel_id,channel_name,nfsw,isBot,guild_id,guild_name,author_id,author_name,author_nick):
        self.message_id = message_id
        self.text = text
        self.date = date
        self.mentions = mentions
        self.embeds = embeds
        self.reactions = reactions
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.nfsw = nfsw
        self.isBot = isBot
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.author_id = author_id
        self.author_name = author_name
        self.author_nick = author_nick
        