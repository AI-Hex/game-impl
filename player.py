import pygame, sys, random
from board import *
from strategies import *
from graph import *


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

    def get_opponent_token(self):
        return 1 if self.token == 2 else 2

    def find_max_value_move(self, minimax_results: list[float]) -> int:
        maximum: float = max(minimax_results)

        return minimax_results.index(maximum)

    def get_move(self, board: Board) -> tuple[int, int]:
        unoccupied_tiles = board.get_unoccupied_tiles()
        possible_states: list[Board] = list()
        strategy: Strategy = Strategy()
        for tile in unoccupied_tiles:
            new_board: Board
            new_board = board.__copy__()
            new_board.make_move(tile, self.token)
            possible_states.append(new_board)
        minmax_results: list[float] = list()
        for state in possible_states:
            minmax_results.append(strategy.alpha_beta_pruned_minimax(depth=1, isMaximizingPlayer=False, alpha=float("-inf"),
                                                                     beta=float("inf"), board=state, player_token=self.get_opponent_token(), max_depth=3))
        # return sorted(list(zip(minmax_results, unoccupied_tiles)))[0][1]
        index: int = self.find_max_value_move(minmax_results)
        return unoccupied_tiles[index]