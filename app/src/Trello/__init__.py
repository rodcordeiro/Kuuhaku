from trello import TrelloClient
from decouple import config

class Trello:
    def __init__(self):
       self.client =  TrelloClient(
        api_key=config('TRELLO_API_KEY'),
        token=config('TRELLO_TOKEN'),
        )
       self.defaultBoard = None
    def about(self):
        print(self.defaultBoard)
    def getBoards(self):
        boards = self.client.list_boards()
        return boards
    def getLists(self, board = None):
        if board:
            lists = board.list_lists()
            return lists
        if self.defaultBoard != None:
            print('self.defaultBoard',self.defaultBoard)
            boards = self.client.list_boards()
            for board in boards:
                if board.id == self.defaultBoard.id:
                    print('board',board)
                    lists = board.list_lists()
                    print('lists',lists)
                    return lists
                raise Exception("Lists not found")
                
        raise Exception("Board not provided")
    def getList(self, board, list_id):
        list = board.get_list(list_id)
        for card in list.list_cards():
            print(card.name)
        return list
