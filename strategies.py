from graph import *
from board import *

max_depth = 3

class Strategy(object):

    def start_dijkstra(self, player: int, board: Board) -> int:
        source_nodes: list[HexNode]
        if player == 1: #player goal is to connect left and right side of the board
            source_nodes = board.graph.get_first_column_tiles(player)
        else: #players goal is to connect top and bottom side of the board
            source_nodes = board.graph.get_first_row_tiles(player)
        min_distance: int
        resulting_min_distance = float("inf")
        for source_node in source_nodes:
            current_distances = self.dijkstra(source_node, board, player)
            curr_min = min(current_distances)
            if curr_min < resulting_min_distance:
                resulting_min_distance = curr_min
        return resulting_min_distance

    def find_node_with_min_distance(self, list_nodes: list[HexNode], distances: list[int]) -> HexNode:
        min = float("inf")
        found_node = list_nodes[0]
        for node in list_nodes:
            if distances[node.node_value] < min:
                min = distances[node.node_value]
                found_node = node
        return found_node

    def dijkstra(self, source: HexNode, board: Board, player: int) -> list[int]:
        distances: list[int]
        queue: list[HexNode]
        distances = list()
        queue = list()
        for node in board.graph.hex_nodes:
            distances.append(float("inf"))
            queue.append(node)
        distances[source.node_value] = 0

        while len(queue) > 0:
            current_node = self.find_node_with_min_distance(queue, distances)
            queue.remove(current_node)

            neighbours = board.find_all_neighbour_nodes(current_node, player)
            for neighbour in neighbours:
                if neighbour in queue:
                    new_distance = distances[current_node.node_value] + board.graph.edges_matrix[current_node.node_value][neighbour.node_value]
                    if new_distance < distances[neighbour.node_value]:
                        distances[neighbour.node_value] = new_distance

        return distances

    def evaluate_score(self, board: Board, player_token: int):
        opponent_player = 1 if player_token == 2 else 2
        opponent_score = self.start_dijkstra(opponent_player, board)
        current_player_score = self.start_dijkstra(player_token, board)
        return opponent_score - current_player_score

    def get_moves(self, board: Board): #get_unoccupied_tiles
        return board.get_available_nodes()

    def alpha_beta_pruned_minimax(self, depth: int, isMaximizingPlayer: bool, alpha: int, beta: int, board: Board, player_token: int, max_depth: int = 3):
        successors = self.get_moves(board)
        if depth == max_depth or len(successors) == 0:
            return self.evaluate_score(board, player_token)

        new_player_token = 1 if player_token == 2 else 2

        if isMaximizingPlayer:
            best_value = float("-inf")
            for successor in successors:
                new_board: Board
                new_board = board.__copy__()
                new_board.make_move(successor.position, player_token)
                value = self.alpha_beta_pruned_minimax(depth=depth + 1, isMaximizingPlayer=False, alpha=alpha, beta=beta,
                                                       board=new_board, player_token=new_player_token)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value

        else:
            best_value = float("inf")
            for successor in successors:
                new_board: Board
                new_board = board.__copy__()
                new_board.make_move(successor.position, player_token)
                value = self.alpha_beta_pruned_minimax(depth=depth + 1, isMaximizingPlayer=True, alpha=alpha, beta=beta,
                                                       board=new_board, player_token=new_player_token)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value
