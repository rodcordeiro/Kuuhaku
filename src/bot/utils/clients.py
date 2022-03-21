class Clients:
    def __init__(self):
        self.__init__ = self
        self.clients = {
            "trello":{}
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
        return clients[guild]