from trello import TrelloClient
from decouple import config


class Trello:
    def __init__(self, token):
        self.client = TrelloClient(
            api_key=config("TRELLO_API_KEY"),
            token=token,
        )
        self.default_board = None
        self.boards = []

    def about(self):
        print(self)

    def get_boards(self):
        boards = self.client.list_boards()
        print(boards[0])
        for board in boards:
            print(board)
            self.boards.append({
                "id": board.id,
                "name": board.name,
                "lists": [],
                "board": board
            })
        print(self.boards)
        return boards

    def get_lists(self, board=None):
        print(board, self.default_board)
        if board:
            for b in self.boards:
                if b['name'] == board:
                    print("board", board)
                    lists = b.list_lists()
                    b.lists = lists
                    print("lists", lists)
                    return lists
        if self.default_board != None:
            print("self.default_board", self.default_board)
            for board in self.boards:
                if board.id == self.default_board.id:
                    print("board", board)
                    lists = board.list_lists()
                    print("lists", lists)
                    return lists
                raise Exception("Lists not found")
        raise Exception("Board not provided")

    def get_cards(self, board = None, list = None):
        if list is None:
            raise Exception("List not provided")
        if board is None:
            if self.default_board is None:
                raise Exception('Board not provided')
            for board in self.boards:
                if board.id == self.default_board.id:
                    for l in board.lists:
                        if l.name == list:
                            # list = board.get_list(l.id)
                            cards = l.list_cards()
                            for card in cards:
                                print(card.name)
                            return cards
        for b in self.boards:
                if b.id == self.default_board.id:
                    for l in b.lists:
                        if l.name == list:
                            # list = b.get_list(l.id)
                            cards = l.list_cards()
                            for card in cards:
                                print(card.name)
                            return cards
            

            
        list = board.get_list(list_id)
        for card in list.list_cards():
            print(card.name)
        return list
