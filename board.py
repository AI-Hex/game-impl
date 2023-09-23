import pygame


<<<<<<< HEAD
# State of tile pieces in board
UNOCUPIED = 0
PLAYER_1_TOKEN = 1
PLAYER_2_TOKEN = 2


class Board(object):

    board: list[list[int]]
    '''Keeps track of the tokens (lack there of) on the board'''
    board_size: int

    def __init__(self, board_size: int):
        """
        Initialize an empty hex board
        """
        self.board = [[UNOCUPIED for i in range(board_size)] for j in range(board_size)]
        self.board_size = board_size

    def make_move(self, tile_pos: tuple[int], player_token: int):
        """
        Place a player token on an unocupied tile
        """
        row, column = tile_pos
        self.board[row][column] = player_token
    
    def occupies(self, tile_pos: tuple[int]) -> bool:
        """
        Return whether the tile is occupied by a player's token
        """
        row, column = tile_pos
        return self.board[row][column] != UNOCUPIED
    
    def get_unocupied_tiles(self) -> list[tuple[int]]:
        return [(i, j) for j in range(self.board_size) for i in range(self.board_size) if self.board[i][j] == UNOCUPIED]
    
=======
class Token(object):
    pass


class Hex_board(object):

    board_size: int
    board: list[list[Token]]
    click_board: tuple[tuple[pygame.Rect]]

    def __init__(self):
        pass

    pass
>>>>>>> ae7030dff4adc72573dec5a5a6d7c50d9ae02e0e


