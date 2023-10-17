import pygame, sys, random, copy, numpy, time
from board import *
from graph import *


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
            result = self.__evaluate_score(self.token, current_depth, True)
            if result == 9999: #it's a winning move
                return float('inf'), (None, None)

        if current_depth == self.max_depth or len(successor_moves) == 0:
            #return self.__get_two_distance_score(SpecialHexNode(None, None, self.token, 1), SpecialHexNode(None, None, self.token, 3), self.token), (None, None)
             return self.__evaluate_score(self.token, current_depth, True), (None, None)
        
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

    def __evaluate_score(self, player_token: int, num_turns: int, is_two_distance_evaluation: bool):
        """
        Return heuristic score for a given board state
        """
        opponent_token = 1 if player_token == 2 else 2
        if is_two_distance_evaluation:
            opponent_score = self.__get_two_distance_score(Board.special_node_left if opponent_token == 1 else Board.special_node_top, 
                                                           Board.special_node_right if opponent_token == 1 else Board.special_node_bottom, opponent_token)
            player_score = self.__get_two_distance_score(Board.special_node_left if player_token == 1 else Board.special_node_top, 
                                                         Board.special_node_right if player_token == 1 else Board.special_node_bottom, player_token)
            return opponent_score - player_score
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
        sink_position = 1 if player_token == 1 else 0  # Denotes if algoritm should move towards last column or last row

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

        return [(n_i, n_j) for (n_i, n_j) in adjacent_neighbors_dict[current_node] if Board.board[n_i, n_j] != opponent_token]

    def find_chain(self, player, current_node) -> set[HexNode]:
        chain_set: set[HexNode] = set()
        visited: list[HexNode] = list()
        chain_set.add(current_node)
        visited.append(current_node)
        neighbouring_nodes: list[HexNode] = Board.find_all_neighbour_nodes(current_node, player)
        while len(neighbouring_nodes) > 0:
            neighbour_node = neighbouring_nodes.pop(0)
            if neighbour_node not in visited and neighbour_node.status == player:
                chain_set.add(neighbour_node)
                neighbouring_nodes.extend(Board.find_all_neighbour_nodes(neighbour_node, player))
            visited.append(neighbour_node)
        return chain_set

    def find_neighbourhood_nodes(self, starting_node, player_token):
        resulting_set: set[HexNode] = set()
        #First add the direct neighbour positions
        chain_for_node = self.find_chain(player_token, starting_node)
        print("Start: ", starting_node.position, "CHAIN: ", [node.position for node in chain_for_node])
        for node in chain_for_node:
            
            neighbours = Board.find_all_neighbour_nodes(node, UNOCCUPIED)
            print("NEIGHBORS", [node.position for node in neighbours])
            for neighbour in neighbours:
                resulting_set.add(neighbour)
        return resulting_set

    def __get_two_distance_score(self, node_one_position: HexNode, node_two_position: HexNode, player_token: int):
        print("----------------START OF TWO DISTANCE--------------------")
        print("BOARD", Board.board)
        queue: list[HexNode] = list()
        start_node = node_one_position
        end_node = node_two_position
        print("START NODE ", start_node.position)
        neighbourhood_nodes = self.find_neighbourhood_nodes(start_node, player_token)
        print("NEIGHBORS F START: ", [node.position for node in neighbourhood_nodes])
        for neighbour in neighbourhood_nodes:
            neighbour.td_value = 1
            neighbour.td_neighbour_values_list.extend([0, 0])
            queue.append(neighbour)
        while len(queue) > 0:
            current_node = queue.pop(0)
            current_neighbourhood_nodes = self.find_neighbourhood_nodes(current_node, player_token)
            print("Now in queue ", current_node.position, " with neighbors ", [node.position for node in current_neighbourhood_nodes])
            for neighbour in current_neighbourhood_nodes:
                print(neighbour.td_value, neighbour.position)
                if neighbour.td_value == None:
                    print("hi", neighbour.is_special_node())
                    if neighbour.is_special_node() == True and neighbour != end_node:
                        continue
                    print("BYE")
                    neighbour.td_neighbour_values_list.append(min(current_node.td_neighbour_values_list) + 1)
                    if len(neighbour.td_neighbour_values_list) > 1:
                        neighbour.td_value = max(neighbour.td_neighbour_values_list) + 1
                        print(neighbour.td_value, "gi")
                        queue.append(neighbour)
        if end_node.td_value != None:
            evaluation = end_node.td_value
            print("FINAL VALUE", end_node.td_value)
            for i, j in Board.hex_nodes_by_position:
                node = Board.hex_nodes_by_position[(i, j)]
                node.td_value = None
                node.td_neighbour_values_list.clear()
            Board.special_node_top.td_value, Board.special_node_right.td_value, Board.special_node_bottom.td_value, Board.special_node_left.td_value = None, None, None, None
            Board.special_node_left.td_neighbour_values_list.clear()
            Board.special_node_top.td_neighbour_values_list.clear()
            Board.special_node_right.td_neighbour_values_list.clear()
            Board.special_node_bottom.td_neighbour_values_list.clear()
            return evaluation
        return 10000




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

class AI_Minmax_Graph_Player(AI_Player):
    max_depth = 3

    def start_dijkstra(self, player: int) -> int:
        source_nodes: list[HexNode]
        if player == 1:  # player goal is to connect left and right side of the board
            source_nodes = Board.graph.get_first_column_tiles(player)
        else:  # players goal is to connect top and bottom side of the board
            source_nodes = Board.graph.get_first_row_tiles(player)
        min_distance: int
        resulting_min_distance = float("inf")
        for source_node in source_nodes:
            current_distances = self.dijkstra(source_node, player)
            curr_min = min(current_distances)
            if curr_min < resulting_min_distance:
                resulting_min_distance = curr_min
        return resulting_min_distance

    def find_node_with_min_distance(self, list_nodes: list[HexNode], distances: list[int]) -> HexNode:
        minimum = float("inf")
        found_node = list_nodes[0]
        for node in list_nodes:
            if distances[node.node_value] < minimum:
                minimum = distances[node.node_value]
                found_node = node
        return found_node

    def dijkstra(self, source: HexNode, player_token: int) -> list[int]:
        distances: list[int]
        queue: list[HexNode]
        distances = list()
        queue = list()
        for node in Board.graph.hex_nodes:
            distances.append(float("inf"))
            queue.append(node)
        distances[source.node_value] = 0 if source.status == player_token else 1
        #distances[source.node_value] = 1

        while len(queue) > 0:
            current_node = self.find_node_with_min_distance(queue, distances)
            queue.remove(current_node)

            neighbours = Board.find_all_neighbour_nodes(current_node, player_token)
            for neighbour in neighbours:
                if neighbour in queue:
                    new_distance = distances[current_node.node_value] + \
                                   Board.graph.edges_matrix[current_node.node_value][neighbour.node_value]
                    if new_distance < distances[neighbour.node_value]:
                        distances[neighbour.node_value] = new_distance
        board_size: int = Board.board_size
        if player_token == PLAYER_1_TOKEN: # last column
            resulting_distances = [distances[i] for i in range(len(distances)) if i % board_size == board_size - 1]
        else: #last row
            num_nodes = board_size * board_size
            resulting_distances = [distances[i] for i in range(num_nodes - board_size, num_nodes)]
        return resulting_distances

    def evaluate_score(self, player_token: int, num_turns: int):
        opponent_player = 1 if player_token == 2 else 2
        opponent_score = self.start_dijkstra(opponent_player)
        player_score = self.start_dijkstra(player_token)
        evaluation = opponent_score - player_score - num_turns
        return evaluation

    def get_moves(self):  # get_unoccupied_tiles
        return Board.get_available_nodes()

    def alpha_beta_pruned_minimax(self, depth: int, isMaximizingPlayer: bool, alpha: int, beta: int,
                                  player_token: int, max_depth: int = 3):
        pygame.event.clear()
        successors = self.get_moves()

        if depth == max_depth or len(successors) == 0:
            return self.evaluate_score(self.token, depth)

        if depth == 1:
            result = self.evaluate_score(self.token, depth)
            if result == 9999: #it's a winning move
                return float('inf')

        new_player_token = 1 if player_token == 2 else 2

        if isMaximizingPlayer:
            best_value = float("-inf")
            for successor in successors:
                #new_board: Board
                #new_board = board.__copy__()
                #new_board.make_move(successor.position, player_token)
                Board.make_move(successor.position, player_token)
                value = self.alpha_beta_pruned_minimax(depth=depth + 1, isMaximizingPlayer=False, alpha=alpha,
                                                       beta=beta, player_token=new_player_token)
                Board.remove_move(successor.position)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value

        else:
            best_value = float("inf")
            for successor in successors:
                #new_board: Board
                #new_board = board.__copy__()
                #new_board.make_move(successor.position, player_token)
                Board.make_move(successor.position, player_token)
                value = self.alpha_beta_pruned_minimax(depth=depth + 1, isMaximizingPlayer=True, alpha=alpha,
                                                       beta=beta, player_token=new_player_token)
                Board.remove_move(successor.position)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    def __init__(self, token: int):
        super().__init__(token)

    def get_opponent_token(self):
        return 1 if self.token == 2 else 2

    def find_max_value_move(self, minimax_results: list[float]) -> int:
        maximum: float = max(minimax_results)

        return minimax_results.index(maximum)

    def get_move(self) -> tuple[int, int]:
        unoccupied_tiles = Board.get_unoccupied_tiles()
        possible_states: list[Board] = list()
        #strategy: AI_Minmax_Graph_Player.Strategy = self.Strategy()
        minmax_results: list[float] = list()
        dijkstra_results: list[float] = list()
        for tile in unoccupied_tiles:
            #new_board: Board
            #new_board = board.__copy__()
            #new_board.make_move(tile, self.token)
            #possible_states.append(new_board)
            Board.make_move(tile, self.token)
            value = self.alpha_beta_pruned_minimax(depth=1, isMaximizingPlayer=False, alpha=float("-inf"),
                                                   beta=float("inf"),
                                                   player_token=self.get_opponent_token(), max_depth=3)
            minmax_results.append(value)
            Board.remove_move(tile)
        # return sorted(list(zip(minmax_results, unoccupied_tiles)))[0][1]
        index: int = self.find_max_value_move(minmax_results)
        #print(Board.graph.edges_matrix)
        #print(dijkstra_results[index])
        return unoccupied_tiles[index]