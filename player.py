import pygame, sys, random, copy, numpy, time
from board import *


PLAYER_1 = 1
PLAYER_2 = 2


class Player(object):
    """
    Base player class
    """

    token: int
    board: numpy.ndarray

    def __init__(self, token: int):
        self.token = token
        self.board = None

    def is_human(self) -> bool:
        raise NotImplementedError('Abstract method should be overriden')
    
    def is_ai(self) -> bool:
        raise NotImplementedError('Abstract method should be overriden')

    def get_move(self, game_board: Board):
        raise NotImplementedError('Abstract method should be overriden')


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
        self.board = numpy.copy(game_board.board)
        start_time = time.time()
        _, best_move = self.__alpha_beta_pruned_minmax(player_token=self.token,
                                                       is_maximizing_player=True, current_depth=0)
        end_time = time.time()
        print(end_time - start_time)
        return best_move

    def __alpha_beta_pruned_minmax(self, player_token: int, is_maximizing_player: bool, current_depth: int,
                                   alpha: int = float('-inf'), beta: int = float('inf')) -> tuple[float, tuple[int, int]]:
        """
        Find next best state using minmax algorithm with alpha beta pruning

        Return the best state's score and the best tile position
        """
        pygame.event.pump()  # Trick computer into thinking events are being handled
        successor_moves = [(i, j) for j in range(len(self.board)) for i in range(len(self.board)) if self.board[i, j] == UNOCCUPIED]

        if current_depth == self.max_depth or len(successor_moves) == 0:
            state_string = self.board.tostring()
            if state_string in move_list:
                return lookup(current_depth, state_string)
            else:
                evaluation = self.__evaluate_score(self.token)
                store(current_depth, state_string, (None, None), evaluation)
                return evaluation, (None, None)
        
        opponent_token = 1 if player_token == 2 else 2

        if is_maximizing_player is True:
            result_value, result_move = float('-inf'), (None, None)
            for successor_move in successor_moves:
                s_i, s_j = successor_move
                self.board[s_i, s_j] = player_token
                best_value, _ = self.__alpha_beta_pruned_minmax(opponent_token,
                                                                False, current_depth + 1,
                                                                alpha, beta)
                self.board[s_i, s_j] = UNOCCUPIED
                if best_value == result_value and best_value == float('-inf'):
                    result_move = successor_move
                if best_value > result_value:
                    result_value = best_value
                    result_move = successor_move
                alpha = max(alpha, best_value)
                if beta <= best_value:  # how to fix this, prunes everything after finding victory
                    break
            return result_value, result_move
        else:
            result_value, result_move = float('inf'), (None, None)
            for successor_move in successor_moves:
                s_i, s_j = successor_move
                self.board[s_i, s_j] = player_token
                best_value, _ = self.__alpha_beta_pruned_minmax(opponent_token,
                                                                True, current_depth + 1,
                                                                alpha, beta)
                self.board[s_i, s_j] = UNOCCUPIED
                if best_value == result_value and best_value == float('+inf'):
                    result_move = successor_move
                if best_value < result_value:
                    result_value = best_value
                    result_move = successor_move
                beta = min(beta, best_value)
                if best_value <= alpha:
                    break
            return result_value, result_move
    
    def __evaluate_score(self, player_token: int):
        """
        Return heuristic score for a given board state
        """
        opponent_token = 1 if player_token == 2 else 2
        opponent_score = self.__get_dijkstra_score(opponent_token)
        player_score = self.__get_dijkstra_score(player_token)
        
        return opponent_score - player_score

    def __get_dijkstra_score(self, player_token: int) -> float:
        """
        This is a heuristic function

        Return the minimal number of tiles needed to make a winning path on current state
        """
        source_node = (len(self.board), 0)

        # source_nodes = [(i, 0) if player_token == 1 else (0, i) for i in range(len(self.board))]
        return min(self.__dijkstra(player_token, source_node))

        # for source_node in source_nodes:
        #     s_i, s_j = source_node
        #     if self.board[s_i, s_j] == player_token or self.board[s_i, s_j] == UNOCCUPIED:
        #         current_distances_to_sink = self.__dijkstra(player_token, source_node)
        #         current_min = min(current_distances_to_sink)
        #         if current_min < resulting_min_distance:
        #             resulting_min_distance = current_min
        # return resulting_min_distance

    def __dijkstra(self, player_token: int, source_node: tuple[int, int]) -> list[float]:
        """
        Calculate and return distances from source node to opposite border
        """
        distances = [[float('inf') for _ in range(len(self.board))] for _ in range(len(self.board))]
        distances.append([0])

        queue = [(i, j) for j in range(len(self.board)) for i in range(len(self.board))] + [source_node]

        while len(queue) > 0:
            i, j = self.__get_min_distance_pos_in_queue(queue, distances)
            if i is None:
                break
            queue.remove((i, j))

            for neighbor in self.__get_neighboring_nodes((i, j), player_token):
                if neighbor in queue:
                    n_i, n_j = neighbor
                    new_distance = distances[i][j] + (0 if self.board[n_i, n_j] == player_token else 1)
                    if new_distance < distances[n_i][n_j]:
                        distances[n_i][n_j] = new_distance
        
        sink_nodes = [(i, len(self.board) - 1) if player_token == 1 else (len(self.board) - 1, i) for i in range(len(self.board))]
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
    
    def __get_neighboring_nodes(self, current_node: tuple[int, int], player_token: int) -> list[tuple[int, int]]:
        """
        Return neighboring nodes of a given node that are NOT occupied by the opponent
        """
        result: list[tuple[int, int]] = list()
        row, column = current_node
        opponent_token = 1 if player_token == 2 else 2

        if (row, column) == (len(self.board), 0):
            if player_token == PLAYER_1_TOKEN:
                return [(i, 0) for i in range(len(self.board)) if self.board[i, 0] != opponent_token]
            else:
                return [(0, i) for i in range(len(self.board)) if self.board[0, i] != opponent_token]

        if 0 <= row - 1:
            if self.board[row - 1, column] != opponent_token:
                result.append((row - 1, column))
        if 0 <= row - 1 and column + 1 < len(self.board):
            if self.board[row - 1, column + 1] != opponent_token:
                result.append((row - 1, column + 1))
        if 0 <= column - 1:
            if self.board[row, column - 1] != opponent_token:
                result.append((row, column - 1))
        if column + 1 < len(self.board):
            if self.board[row, column + 1] != opponent_token:
                result.append((row, column + 1))
        if row + 1 < len(self.board) and 0 <= column - 1:
            if self.board[row + 1, column - 1] != opponent_token:
                result.append((row + 1, column - 1))
        if row + 1 < len(self.board):
            if self.board[row + 1, column] != opponent_token:
                result.append((row + 1, column))
        return result

class AI_Iterative_Deepening_Player(AI_Player):
    pass