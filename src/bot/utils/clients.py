class Clients:
    def __init__(self):
        self.__init__ = self
        self.clients = {
            "trello":{},
            "azure":{}
        }
    def add_client(self,type,guild,client):
        try:
            clients = self.clients[type]
            clients[guild] = client
            self.clients[type] = clients
        except Exception:
            clients = {}
            clients[guild] = client
            self.clients[type] = clients

    def get_client(self,type,guild):
        clients = self.clients[type]
        if len(clients) == 0:
            raise Exception("No clients available")        
        if clients[guild] is None:
            raise Exception("Client not provided")
        return clients[guild]