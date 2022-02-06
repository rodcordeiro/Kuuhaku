from trello import TrelloClient
from decouple import config

class Trello:
    def __init__(self):
       self.client =  TrelloClient(
        api_key=config('TRELLO_API_KEY'),
        token=config('TRELLO_TOKEN'),
        )
    
    def getBoards(self):
        boards = self.client.list_boards()
        return boards
    def getLists(self, board):
        lists = board.list_lists()
        return lists
    def getList(self, board, list_id):
        list = board.get_list(list_id)
        for card in list.list_cards():
            print(card.name)
        return list
