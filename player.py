import pygame, sys, random, copy, numpy, time
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
        raise NotImplementedError('Abstract method should be overriden')
    
    def is_ai(self) -> bool:
        raise NotImplementedError('Abstract method should be overriden')

    def get_move(self):
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

    def get_move(self) -> bool:
        """
        Get a tile chosen by AI
        """
        pass


class AI_Random_Player(AI_Player):
    
    def __init__(self, token: int):
        super().__init__(token)
    
    def get_move(self) -> tuple[int, int]:
        """
        Get a random unocupied tile
        """
        possible_moves = Board.get_unoccupied_tiles()
        return possible_moves[random.randint(0, len(possible_moves) - 1)]


class AI_Minmax_Player(AI_Player):

    max_depth: int

    def __init__(self, token: int):
        super().__init__(token)
        self.max_depth = 3
        assert self.max_depth > 0
    
    def get_move(self) -> tuple[int, int]:
        """
        Get best move using minmax algorithm with alpha beta pruning
        """
        start_time = time.time()
        _, best_move = self.__alpha_beta_pruned_minmax(player_token=self.token,
                                                       is_maximizing_player=True, current_depth=0)
        end_time = time.time()
        print(_)
        print(end_time - start_time)
        return best_move

    def __alpha_beta_pruned_minmax(self, player_token: int, is_maximizing_player: bool, current_depth: int,
                                   alpha: int = float('-inf'), beta: int = float('inf')) -> tuple[float, tuple[int, int]]:
        """
        Find next best state using minmax algorithm with alpha beta pruning

        Return the best state's score and the best tile position
        """
        pygame.event.clear()  # Trick computer into thinking events are being handled
        state_str = Board.get_board_string()
        if state_str in transposition_table:
            if current_depth in transposition_table[state_str]:
                return load(state_str, current_depth)
        successor_moves = sorted([(i, j) for j in range(Board.board_size) for i in range(Board.board_size) if Board.board[i, j] == UNOCCUPIED], key=lambda x: abs(x[0] - (Board.board_size - 1)/2) + abs(x[1] - (Board.board_size - 1)/2))

        if current_depth == 1:
            result = self.__evaluate_score(self.token, current_depth)
            if result == 9999: #it's a winning move
                return float('inf'), (None, None)

        if current_depth == self.max_depth or len(successor_moves) == 0:
            return self.__evaluate_score(self.token, current_depth), (None, None)
        
        opponent_token = 1 if player_token == 2 else 2

        if is_maximizing_player is True:
            result_value, result_move = float('-inf'), (None, None)
            for successor_move in successor_moves:
                s_i, s_j = successor_move
                Board.board[s_i, s_j] = player_token
                best_value, _ = self.__alpha_beta_pruned_minmax(opponent_token,
                                                                False, current_depth + 1,
                                                                alpha, beta)
                Board.board[s_i, s_j] = UNOCCUPIED
                if best_value == result_value and best_value == float('-inf'):
                    result_move = successor_move
                if best_value > result_value:
                    result_value = best_value
                    result_move = successor_move

                alpha = max(alpha, best_value)
                
                if beta <= best_value:  # how to fix this, prunes everything after finding victory
                    break
            store(state_str, current_depth, result_value, result_move)
            return result_value, result_move
        else:
            result_value, result_move = float('inf'), (None, None)
            for successor_move in successor_moves:
                s_i, s_j = successor_move
                Board.board[s_i, s_j] = player_token
                best_value, _ = self.__alpha_beta_pruned_minmax(opponent_token,
                                                                True, current_depth + 1,
                                                                alpha, beta)
                Board.board[s_i, s_j] = UNOCCUPIED
                if best_value == result_value and best_value == float('+inf'):
                    result_move = successor_move
                if best_value < result_value:
                    result_value = best_value
                    result_move = successor_move
                beta = min(beta, best_value)
                if best_value <= alpha:
                    break
            store(state_str, current_depth, result_value, result_move)
            return result_value, result_move
    
    # def __evaluate_score(self, player_token: int, num_turns: int):
    #     """
    #     Return heuristic score for a given board state
    #     """
    #     return random.randint(-10, 10)

    def __evaluate_score(self, player_token: int, num_turns: int):
        """
        Return heuristic score for a given board state
        """
        opponent_token = 1 if player_token == 2 else 2
        opponent_score = self.__get_dijkstra_score(opponent_token)
        player_score = self.__get_dijkstra_score(player_token)
        evaluation = opponent_score - player_score - num_turns
        if evaluation < -9000:
            pass #some logic to add points to the evaluation so its not dumb
        return evaluation

    def __get_dijkstra_score(self, player_token: int) -> float:
        """
        This is a heuristic function

        Return the minimal number of tiles needed to make a winning path on current state
        """
        source_node = (Board.board_size, 0)
        return self.__dijkstra(player_token, source_node)

    def __dijkstra(self, player_token: int, source_node: tuple[int, int]) -> float:
        """
        Calculate and return shortest distance from source node to opposite border
        """
        distances = [[10000 for _ in range(Board.board_size)] for _ in range(Board.board_size)]

        queue = [(i, j) for j in range(Board.board_size) for i in range(Board.board_size)]
        # sink_nodes = [(i, Board.board_size - 1) if player_token == 1 else (Board.board_size - 1, i) for i in range(Board.board_size)]
        sink_position = 1 if player_token == 1 else 0

        # start dijkstra for source node
        opponent_token = 1 if player_token == 2 else 2
        neighbors: list[tuple[int, int]]

        if player_token == PLAYER_1_TOKEN:
            neighbors = [(i, 0) for i in range(Board.board_size) if Board.board[i, 0] != opponent_token]
        else:
            neighbors = [(0, i) for i in range(Board.board_size) if Board.board[0, i] != opponent_token]
        
        for neighbor in neighbors:
                if neighbor in queue:
                    n_i, n_j = neighbor
                    new_distance = 0 if Board.board[n_i, n_j] == player_token else 1
                    if new_distance < distances[n_i][n_j]:
                        distances[n_i][n_j] = new_distance
                    if neighbor[sink_position] == Board.board_size - 1:
                        return distances[n_i][n_j]

        # continue dijsktra for other nodes
        while len(queue) > 0:
            i, j = self.__get_min_distance_pos_in_queue(queue, distances)
            if i is None:
                break
            queue.remove((i, j))

            for neighbor in self.__get_neighboring_nodes((i, j), player_token):
                if neighbor in queue:
                    n_i, n_j = neighbor
                    new_distance = distances[i][j] + (0 if Board.board[n_i, n_j] == player_token else 1)
                    if new_distance < distances[n_i][n_j]:
                        distances[n_i][n_j] = new_distance
                    if neighbor[sink_position] == Board.board_size - 1:
                        return distances[n_i][n_j]
            
        return 10000
                    
        
        # result = list()
        # for i, j in sink_nodes:
        #     result.append(distances[i][j])
        # return result

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
        opponent_token = 1 if player_token == 2 else 2

        return [(n_i, n_j) for (n_i, n_j) in neighbors_dict[current_node] if Board.board[n_i, n_j] != opponent_token]

        # if row + 1 < Board.board_size:
        #     if Board.board[row + 1, column] != opponent_token:
        #             result.append((row + 1, column))
            
        # else:
        #     pass

        # if 0 <= row - 1:
        #     if Board.board[row - 1, column] != opponent_token:
        #             result.append((row - 1, column))
        #     if column + 1 < Board.board_size:
        #         if Board.board[row - 1, column + 1] != opponent_token:
        #             result.append((row - 1, column + 1))
        # if 0 <= column - 1:
        #     if Board.board[row, column - 1] != opponent_token:
        #         result.append((row, column - 1))
        #     if row + 1 < Board.board_size:
        #         if Board.board[row + 1, column - 1] != opponent_token:
        #             result.append((row + 1, column - 1))


        # if column + 1 < Board.board_size:
        #     if Board.board[row, column + 1] != opponent_token:
        #         result.append((row, column + 1))
        
        # if row + 1 < Board.board_size:
        #     if Board.board[row + 1, column] != opponent_token:
        #         result.append((row + 1, column))
        # return result


