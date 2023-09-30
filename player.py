import pygame, sys, random, copy
from board import *


PLAYER_1 = 1
PLAYER_2 = 2


class Player(object):
    """
    Base player class
    """

    token: int

    def __init__(self, token: int):
        self.token = token

    def is_human(self) -> bool:
        pass
    
    def is_ai(self) -> bool:
        pass

    def get_move(self, game_board: Board):
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

    def get_move(self, game_board: Board) -> bool:
        """
        Get a tile chosen by AI
        """
        pass


class AI_Random_Player(AI_Player):
    
    def __init__(self, token: int):
        super().__init__(token)
    
    def get_move(self, game_board: Board) -> tuple[int, int]:
        """
        Get a random unocupied tile
        """
        possible_moves = game_board.get_unoccupied_tiles()
        return possible_moves[random.randint(0, len(possible_moves) - 1)]


class AI_Minmax_Player(AI_Player):

    max_depth: int

    def __init__(self, token: int):
        super().__init__(token)
        self.max_depth = 3
        assert self.max_depth > 0
    
    def get_move(self, game_board: Board) -> tuple[int, int]:
        """
        Get best move using minmax algorithm with alpha beta pruning
        """
        _, best_move = self.__alpha_beta_pruned_minmax(board=game_board.board, player_token=self.token,
                                                       is_maximizing_player=True, current_depth=0)
        return best_move

    def __alpha_beta_pruned_minmax(self, board: list[list[int]], player_token: int, 
                                   is_maximizing_player: bool, current_depth: int, 
                                   alpha: int = float('-inf'), beta: int = float('inf')) -> tuple[float, tuple[int, int]]:
        """
        Find next best state using minmax algorithm with alpha beta pruning

        Return the best state's score and the best tile position
        """
        pygame.event.pump()  # Trick computer into thinking events are being handled
        successor_moves = [(i, j) for j in range(len(board)) for i in range(len(board)) if board[i][j] == UNOCCUPIED]

        if current_depth == self.max_depth or len(successor_moves) == 0:
            return self.__evaluate_score(board, self.token), (None, None)
        
        opponent_token = 1 if player_token == 2 else 2

        if is_maximizing_player is True:
            result_value, result_move = float('-inf'), (None, None)
            for successor_move in successor_moves:
                s_i, s_j = successor_move
                new_board = copy.deepcopy(board)
                new_board[s_i][s_j] = player_token
                best_value, _ = self.__alpha_beta_pruned_minmax(new_board, opponent_token,
                                                                False, current_depth + 1,
                                                                alpha, beta)
                # if best_value == float('inf'):
                #     if self.__evaluate_score(new_board, self.token) == float('inf'):
                #         return best_value, successor_move
                if best_value > result_value or result_move == (None, None):
                    result_value = best_value
                    result_move = successor_move
                alpha = max(alpha, best_value)
                if beta <= alpha:  # how to fix this, prunes everything after finding victory
                    break
            return result_value, result_move
        else:
            result_value, result_move = float('inf'), (None, None)
            for successor_move in successor_moves:
                s_i, s_j = successor_move
                new_board = copy.deepcopy(board)
                new_board[s_i][s_j] = player_token
                best_value, _ = self.__alpha_beta_pruned_minmax(new_board, opponent_token,
                                                                True, current_depth + 1,
                                                                alpha, beta)
                if best_value < result_value or result_move == (None, None):
                    result_value = best_value
                    result_move = successor_move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return result_value, result_move
    
    def __evaluate_score(self, board: list[list[int]], player_token: int):
        """
        Return heuristic score for a given board state
        """
        opponent_token = 1 if player_token == 2 else 2
        opponent_score = self.__get_dijkstra_score(board, opponent_token)
        player_score = self.__get_dijkstra_score(board, player_token)
        if player_score == 0:
            return float('inf')
        if player_score == float('inf'):
            return 0
        return opponent_score - player_score

    def __get_dijkstra_score(self, board: list[list[int]], player_token: int) -> float:
        """
        This is a heuristic function

        Return the minimal number of tiles needed to make a winning path on current state
        """
        source_nodes = [(i, 0) if player_token == 1 else (0, i) for i in range(len(board))]
        resulting_min_distance = float('inf')
        for source_node in source_nodes:
            s_i, s_j = source_node
            if board[s_i][s_j] == player_token or board[s_i][s_j] == UNOCCUPIED:
                current_distances_to_sink = self.__dijkstra(board, player_token, source_node)
                current_min = min(current_distances_to_sink)
                if current_min < resulting_min_distance:
                    resulting_min_distance = current_min
        return resulting_min_distance

    def __dijkstra(self, board: list[list[int]], player_token: int, source_node: tuple[int, int]) -> list[float]:
        """
        Calculate and return distances from source node to opposite border
        """
        distances = [[float('inf') for _ in range(len(board))] for _ in range(len(board))]
        s_i, s_j = source_node
        distances[s_i][s_j] = (0 if board[s_i][s_j] == player_token else 1)
        queue = [(i, j) for j in range(len(board)) for i in range(len(board))]

        while len(queue) > 0:
            i, j = self.__get_min_distance_pos_in_queue(queue, distances)
            if i is None:
                break
            queue.remove((i, j))

            for neighbor in self.__get_neighboring_nodes(board, (i, j), player_token):
                if neighbor in queue:
                    n_i, n_j = neighbor
                    new_distance = distances[i][j] + (0 if board[n_i][n_j] == player_token else 1)
                    if new_distance < distances[n_i][n_j]:
                        distances[n_i][n_j] = new_distance
        
        sink_nodes = [(i, len(board) - 1) if player_token == 1 else (len(board) - 1, i) for i in range(len(board))]
        result = list()
        for i, j in sink_nodes:
            result.append(distances[i][j])
        return result

    def __get_min_distance_pos_in_queue(self, queue: list[tuple[int, int]], distances: list[list[float]]) -> tuple[int, int]:
        """
        Get the node position with the smallest distance in 'distances' 
        """
        resulting_i: int = None
        resulting_j: int = None
        min_distance: float = float('inf')
        if len(queue) == 1:
            return queue[0]
        for (i, j) in queue:
            if distances[i][j] < min_distance:
                min_distance = distances[i][j]
                resulting_i, resulting_j = i, j
        return resulting_i, resulting_j
    
    def __get_neighboring_nodes(self, board: list[list[int]], current_node: tuple[int, int], player_token: int) -> list[tuple[int, int]]:
        """
        Return neighboring nodes of a given node that are NOT occupied by the opponent
        """
        result: list[tuple[int, int]] = list()
        row, column = current_node
        opponent_token = 1 if player_token == 2 else 2
        if 0 <= row - 1:
            if board[row - 1][column] != opponent_token:
                result.append((row - 1, column))
        if 0 <= row - 1 and column + 1 < len(board):
            if board[row - 1][column + 1] != opponent_token:
                result.append((row - 1, column + 1))
        if 0 <= column - 1:
            if board[row][column - 1] != opponent_token:
                result.append((row, column - 1))
        if column + 1 < len(board):
            if board[row][column + 1] != opponent_token:
                result.append((row, column + 1))
        if row + 1 < len(board) and 0 <= column - 1:
            if board[row + 1][column - 1] != opponent_token:
                result.append((row + 1, column - 1))
        if row + 1 < len(board):
            if board[row + 1][column] != opponent_token:
                result.append((row + 1, column))
        return result


        
        

