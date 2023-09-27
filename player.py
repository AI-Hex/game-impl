import pygame, sys, random
from board import *


PLAYER_1 = 1
PLAYER_2 = 2


class Player(object):

    token: int

    def __init__(self, token: int):
        self.token = token

    def is_human(self) -> bool:
        pass
    
    def is_ai(self) -> bool:
        pass

    def get_move(self, game_board):
        pass


class Human_Player(Player):

    def __init__(self, token: int):
        super().__init__(token)
    
    def is_human(self) -> bool:
        return True

    def is_ai(self) -> bool:
        return not self.is_human()


class AI_Player(Player):

    def __init__(self, token: int):
        super().__init__(token)
    
    def is_human(self) -> bool:
        return False

    def is_ai(self) -> bool:
        return not self.is_human()

    def get_move(self, board: Board) -> bool:
        """
        Get a tile chosen by AI
        """
        pass


class AI_Random_Player(AI_Player):
    
    def __init__(self, token: int):
        super().__init__(token)
    
    def get_move(self, board: Board) -> tuple[int, int]:
        """
        Get a random unocupied tile
        """
        possible_moves = board.get_unoccupied_tiles()
        return possible_moves[random.randint(0, len(possible_moves)-1)]

class AI_Minmax_Player(AI_Player):
    def __init__(self, token: int):
        super().__init__(token)

    def get_move(self, board: Board) -> tuple[int, int]:
        pass