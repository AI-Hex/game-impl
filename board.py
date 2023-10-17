import pygame, numpy
from graph import *

# State of tile pieces in board
UNOCCUPIED = 0
PLAYER_1_TOKEN = 1
PLAYER_2_TOKEN = 2

adjacent_neighbors_dict = dict()
neighbourhood_dict = dict()
transposition_table = dict()


def store(state: str, depth: int, eval: float, move: tuple[int, int]):
    if state not in transposition_table:
        transposition_table[state] = {}
    
    transposition_table[state][depth] = eval, move


def load(state: str, depth: int):
    if state not in transposition_table:
        return None, (None, None)

    if depth in transposition_table[state]:
        return transposition_table[state][depth]
    else:
        depths = transposition_table[state].keys()
        return transposition_table[state][min(depths)]


class Board(object):
    """
    Class containing data structures for the hex board
    """

    board: numpy.ndarray
    '''Keeps track of the tokens (or lack of tokens) on the board'''
    board_size: int
    graph: HexGraph
    hex_nodes_by_position: dict[tuple[int, int], HexNode]

    special_node_neighbors: list[list[tuple[int, int]]]
    special_node_left: SpecialHexNode
    special_node_top: SpecialHexNode
    special_node_right: SpecialHexNode
    special_node_bottom: SpecialHexNode

    def __init__(self, board_size: int):
        """
        Initialize an empty hex board
        """
        Board.board_size = board_size
        #Board.board = numpy.array([[UNOCCUPIED for _ in range(board_size)] for _ in range(board_size)])
        Board.create_initial_nodes_and_board()
        print(Board.graph.edges_matrix)
        for i in range(board_size):
            for j in range(board_size):
                adjacent_neighbors_dict[(i, j)] = self.get_neighboring_tiles((i, j))
        Board.special_node_neighbors = [
                [(i, 0) for i in range(board_size)],
                [(0, i) for i in range(board_size)],
                [(i, board_size - 1) for i in range(board_size)],
                [(board_size - 1, i) for i in range(board_size)]        
            ]
        Board.special_node_left = SpecialHexNode(None, None, PLAYER_1_TOKEN, 0)
        Board.special_node_top = SpecialHexNode(None, None, PLAYER_2_TOKEN, 1)
        Board.special_node_right = SpecialHexNode(None, None, PLAYER_1_TOKEN, 2)
        Board.special_node_bottom = SpecialHexNode(None, None, PLAYER_2_TOKEN, 3)

    @staticmethod
    def create_initial_nodes_and_board():
        new_board = list()
        created_nodes: list[HexNode] = list()
        edges_matrix: list[list[int]]
        Board.hex_nodes_by_position = dict()
        value_counter = 0
        for i in range(Board.board_size):
            new_board.append(list())
            for j in range(Board.board_size):
                new_board[i].append(UNOCCUPIED)
                new_node = HexNode(position=(i, j), node_value=value_counter)
                created_nodes.append(new_node)
                Board.hex_nodes_by_position[(i, j)] = new_node
                value_counter += 1
        Board.board = numpy.array(new_board)
        num_nodes = Board.board_size * Board.board_size
        edges_matrix = [[10000 for _ in range(num_nodes)] for _ in range(num_nodes)]
        Board.graph = HexGraph(board_size=Board.board_size, hex_nodes=created_nodes, edges_matrix=edges_matrix)
        Board.update_initial_edges()

    @staticmethod
    def update_initial_edges():
        nodes_list = Board.graph.hex_nodes
        num_nodes = Board.board_size * Board.board_size
        # counter = 0
        for node in nodes_list:
            node_value = node.node_value
            if 0 <= node_value - Board.board_size <= num_nodes - 1:
                Board.graph.update_edge_value(node_value, node_value - Board.board_size, 1, 1)
            if 0 <= node_value + Board.board_size <= num_nodes - 1:
                Board.graph.update_edge_value(node_value, node_value + Board.board_size, 1, 1)
            if node_value % Board.board_size != Board.board_size - 1:
                if 0 <= node_value - Board.board_size + 1 <= num_nodes - 1:
                    Board.graph.update_edge_value(node_value, node_value - Board.board_size + 1, 1, 1)
                if 0 <= node_value + 1 <= num_nodes - 1:
                    Board.graph.update_edge_value(node_value, node_value + 1, 1, 1)
            if node_value % Board.board_size != 0:
                if 0 <= node_value + Board.board_size - 1 <= num_nodes - 1:
                    Board.graph.update_edge_value(node_value, node_value + Board.board_size - 1, 1, 1)
                if 0 <= node_value - 1 <= num_nodes - 1:
                    Board.graph.update_edge_value(node_value, node_value - 1, 1, 1)
            # print(node.node_value)
            # print(self.graph.edges_matrix[counter])

    def to_string(self):
        return self.board.tostring()

    def clear_board(self):
        """
        Reset the board
        """
        self.create_initial_nodes_and_board()
        #Board.board = numpy.array([[UNOCCUPIED for _ in range(self.board_size)] for _ in range(self.board_size)])
    
    def is_empty(self):
        """
        Check if board is empty
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if Board.board[i, j] != UNOCCUPIED:
                    return False
        return True

    @staticmethod
    def make_move(tile_pos: tuple[int, int], player_token: int):
        """
        Place a player token on an unoccupied tile
        """
        row, column = tile_pos
        Board.board[row, column] = player_token
        node = Board.hex_nodes_by_position[tile_pos]
        node.status = player_token
        neighbour_positions = adjacent_neighbors_dict[tile_pos]
        for position in neighbour_positions:
            neighbour_node = Board.hex_nodes_by_position[position]
            if node.status == neighbour_node.status:
                Board.graph.update_edge_value(node.node_value, neighbour_node.node_value, 0, 0)
            elif neighbour_node.status == UNOCCUPIED:
                Board.graph.update_edge_value(node.node_value, neighbour_node.node_value, 1, 0)
            else: #neighbour_node.status == opponent_token:
                Board.graph.update_edge_value(node.node_value, neighbour_node.node_value, 10000, 10000)

    @staticmethod
    def remove_move(position: tuple[int, int]):
        Board.board[position[0], position[1]] = UNOCCUPIED
        node = Board.hex_nodes_by_position[position]
        neighbour_positions = adjacent_neighbors_dict[position]
        for position in neighbour_positions:
            neighbour_node = Board.hex_nodes_by_position[position]
            if node.status == neighbour_node.status: #It was set to 0 because they were the same color, now should be 1
                Board.graph.update_edge_value(node.node_value, neighbour_node.node_value, 0, 1)
            elif neighbour_node.status == UNOCCUPIED:
                Board.graph.update_edge_value(node.node_value, neighbour_node.node_value, 1, 1)
            else: #neighbour_node.status == opponent_token, it was set to inf if it was opponents tile, now should be 1
                Board.graph.update_edge_value(node.node_value, neighbour_node.node_value, 0, 1)
        node.status = UNOCCUPIED

    @staticmethod
    def find_all_neighbour_nodes(current_node: HexNode, player_token: int) -> list[HexNode]:
        positions_list = list()
        if current_node.is_special_node() == True:
            positions_list = Board.special_node_neighbors[current_node.special_node_value]
        else:
            positions_list = adjacent_neighbors_dict[current_node.position]
        resulting_list: list[HexNode] = list()
        for position in positions_list:
            node = Board.hex_nodes_by_position[position]
            if node.status == player_token or node.status == UNOCCUPIED:
                resulting_list.append(node)
        if current_node.is_special_node() == False:
            if current_node.position[1] == 0:
                resulting_list.append(Board.special_node_left)
            if current_node.position[0] == 0:
                resulting_list.append(Board.special_node_top)
            if current_node.position[1] == Board.board_size - 1:
                resulting_list.append(Board.special_node_right)
            if current_node.position[0] == Board.board_size - 1:
                resulting_list.append(Board.special_node_bottom)
        return resulting_list

    @staticmethod
    def get_available_nodes():
        list_available_nodes: list[HexNode] = list()
        for i in range(Board.board_size):
            for j in range(Board.board_size):
                if Board.board[i][j] == UNOCCUPIED:
                    node = Board.hex_nodes_by_position[(i, j)]
                    list_available_nodes.append(node)
        return list_available_nodes

    def is_tile_occupied(self, tile_pos: tuple[int, int]) -> bool:
        """
        Return whether the tile is occupied by a player's token
        """
        row, column = tile_pos
        return Board.board[row, column] != UNOCCUPIED

    @staticmethod
    def get_unoccupied_tiles() -> list[tuple[int, int]]:
        """
        Get all unoccupied tiles
        """
        return [(i, j) for j in range(Board.board_size) for i in range(Board.board_size) if Board.board[i, j] == UNOCCUPIED]

    @staticmethod
    def get_neighboring_tiles(tile_pos: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Return neighboring tiles of a given tile
        """
        result: list[tuple[int, int]]
        result = list()
        row, column = tile_pos
        if 0 <= row - 1:
            result.append((row - 1, column))
        if 0 <= row - 1 and column + 1 < Board.board_size:
            result.append((row - 1, column + 1))
        if 0 <= column - 1:
            result.append((row, column - 1))
        if column + 1 < Board.board_size:
            result.append((row, column + 1))
        if row + 1 < Board.board_size and 0 <= column - 1:
            result.append((row + 1, column - 1))
        if row + 1 < Board.board_size:
            result.append((row + 1, column))
        return result

    @staticmethod
    def get_neighboring_tiles_by_token(tile_pos: tuple[int, int], by_token: int | None = None) -> list[tuple[int, int]]:
        """
        Return neighboring tiles of a given tile

        Furthermore, filter by UNOCCUPIED, PLAYER_1_TOKEN, PLAYER_2_TOKEN or None
        """
        result = Board.get_neighboring_tiles(tile_pos)
        if by_token is None:
            return result
        if by_token == UNOCCUPIED:
            return [(i, j) for (i, j) in result if Board.board[i, j] == UNOCCUPIED]
        if by_token == PLAYER_1_TOKEN:
            return [(i, j) for (i, j) in result if Board.board[i, j] == PLAYER_1_TOKEN]
        if by_token == PLAYER_2_TOKEN:
            return [(i, j) for (i, j) in result if Board.board[i, j] == PLAYER_2_TOKEN]

    @staticmethod
    def __is_tile_on_right_border(tile_pos: tuple[int, int]) -> bool:
        """
        Check if tile is on the right border
        """
        row, column = tile_pos
        return column == Board.board_size - 1

    @staticmethod
    def __is_tile_on_bottom_border(tile_pos: tuple[int, int]) -> bool:
        """
        Check if tile is on the bottom border
        """
        row, column = tile_pos
        return row == Board.board_size - 1

    @staticmethod
    def __check_player_1_win() -> bool:
        """
        Check if player 1 wins
        """
        visited_tiles = [[False for _ in range(Board.board_size)] for _ in range(Board.board_size)]
        queue = list()
        for row in range(Board.board_size):
            if Board.board[row, 0] == PLAYER_1_TOKEN:
                queue.append((row, 0))
        while len(queue) > 0:
            i, j = queue.pop(0)
            if visited_tiles[i][j] is True:
                continue
            visited_tiles[i][j] = True
            if Board.__is_tile_on_right_border((i, j)) is True:
                return True
            queue.extend(Board.get_neighboring_tiles_by_token((i, j), PLAYER_1_TOKEN))
        return False

    @staticmethod
    def __check_player_2_win() -> bool:
        """
        Check if player 2 wins
        """
        visited_tiles = [[False for _ in range(Board.board_size)] for _ in range(Board.board_size)]
        queue = list()
        for column in range(Board.board_size):
            if Board.board[0, column] == PLAYER_2_TOKEN:
                queue.append((0, column))
        while len(queue) > 0:
            i, j = queue.pop(0)
            if visited_tiles[i][j] is True:
                continue
            visited_tiles[i][j] = True
            if Board.__is_tile_on_bottom_border((i, j)) is True:
                return True
            queue.extend(Board.get_neighboring_tiles_by_token((i, j), PLAYER_2_TOKEN))
        return False

    @staticmethod
    def check_victory() -> bool:
        """
        Check if one of the players won the game
        """
        if Board.__check_player_1_win() is True or Board.__check_player_2_win() is True:
            return True
        return False

    @staticmethod
    def __get_player_1_win_path() -> list[tuple[int, int]] | None:
        """
        Get the winning path for player 1
        """
        visited_tiles = [[False for _ in range(Board.board_size)] for _ in range(Board.board_size)]
        path, queue = list(), list()
        win_path_flag = False
        for row in range(Board.board_size):
            if win_path_flag is True:
                break
            else:
                path = list()  # last itteration was fruitless, continue with empty list
            if Board.board[row, 0] == PLAYER_1_TOKEN:
                queue.append((row, 0))
                while len(queue) > 0:
                    i, j = queue.pop(0)
                    if visited_tiles[i][j] is True:
                        continue
                    visited_tiles[i][j] = True
                    path.append((i, j))
                    if Board.__is_tile_on_right_border((i, j)) is True:
                        win_path_flag = True
                    queue.extend(Board.get_neighboring_tiles_by_token((i, j), PLAYER_1_TOKEN))
        if win_path_flag is True:
            return path
        return None

    @staticmethod
    def __get_player_2_win_path() -> list[tuple[int, int]] | None:
        """
        Get the winning path for player 2
        """
        visited_tiles = [[False for _ in range(Board.board_size)] for _ in range(Board.board_size)]
        path, queue = list(), list()
        win_path_flag = False
        for column in range(Board.board_size):
            if win_path_flag is True:
                break
            else:
                path = list()  # last itteration was fruitless, continue with empty list
            if Board.board[0, column] == PLAYER_2_TOKEN:
                queue.append((0, column))
                while len(queue) > 0:
                    i, j = queue.pop(0)
                    if visited_tiles[i][j] is True:
                        continue
                    visited_tiles[i][j] = True
                    path.append((i, j))
                    if Board.__is_tile_on_bottom_border((i, j)) is True:
                        win_path_flag = True
                    queue.extend(Board.get_neighboring_tiles_by_token((i, j), PLAYER_2_TOKEN))
        if win_path_flag is True:
            return path
        return None

    @staticmethod
    def get_win_path() -> list[tuple[int, int]] | None:
        """
        Get the path that won the game
        """
        if Board.__check_player_1_win() is True:
            return Board.__get_player_1_win_path()
        if Board.__check_player_2_win() is True:
            return Board.__get_player_2_win_path()
        return None

    @staticmethod
    def get_win_token() -> int | None:
        """
        Get winner
        """
        if Board.__check_player_1_win() is True:
            return PLAYER_1_TOKEN
        if Board.__check_player_2_win() is True:
            return PLAYER_2_TOKEN
        return None
    
    @staticmethod
    def get_board_string() -> str:
        result = ''
        for i in range(Board.board_size):
            for j in range(Board.board_size):
                result = result + str(Board.board[i, j])
        return result
        
