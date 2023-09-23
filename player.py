<<<<<<< HEAD
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


class Human_player(Player):

    def __init__(self, token: int):
        super().__init__(token)
    
    def is_human(self) -> bool:
        return True

    def is_ai(self) -> bool:
        return not self.is_human()


class AI_player(Player):

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


class AI_random_player(AI_player):
    
    def __init__(self, token: int):
        super().__init__(token)
    
    def get_move(self, board: Board) -> bool:
        """
        Get a random unocupied tile
        """
        possible_moves = board.get_unocupied_tiles()
        return possible_moves[random.randint(0, len(possible_moves)-1)]
=======
import pygame


class Player(object):
    
    def __init__(self):
        pass
    
    pass


class Human_player(Player):
    pass


class AI_player(Player):
    pass
>>>>>>> ae7030dff4adc72573dec5a5a6d7c50d9ae02e0e
