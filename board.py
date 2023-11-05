import numpy
from graph import *
from transpositionTable_hashing import *


adjacent_neighbors_dict = dict()
# special_adjacent_neighbours_dict: dict[str, list[tuple[int, int]]] = dict()
adjacent_neighbor_nodes_dict: dict[int, list[HexNode]] = dict()
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
    num_nodes: int
    graph: HexGraph
    hex_nodes_by_position: dict[tuple[int, int], HexNode]
    special_hex_nodes: dict[str, HexNode]
    two_distance_transposition_table_blue: Transposition_Table
    two_distance_transposition_table_orange: Transposition_Table
    dijkstra_transposition_table: Transposition_Table

    def __init__(self, board_size: int, already_existing_table: bool):
        """
        Initialize an empty hex board
        """
        Board.board_size = board_size
        num_nodes = board_size * board_size
        Board.num_nodes = num_nodes
        Board.create_initial_nodes_and_board()
        Board.two_distance_transposition_table_blue = Transposition_Table(already_existing_table=already_existing_table,
                                                               is_two_distance=True, is_blue=True, board_size=board_size)
        Board.two_distance_transposition_table_orange = Transposition_Table(already_existing_table=already_existing_table,
                                                                          is_two_distance=True, is_blue=False,
                                                                          board_size=board_size)
        Board.dijkstra_transposition_table = Transposition_Table(already_existing_table=already_existing_table, is_blue=True,
                                                               is_two_distance=False, board_size=board_size)
        for i in range(board_size):
            for j in range(board_size):
                adjacent_neighbors_dict[(i, j)] = self.get_neighboring_tiles((i, j))
                node = self.hex_nodes_by_position[(i, j)]
                adjacent_neighbor_nodes_dict[node.node_value] = self.get_neighbouring_nodes((i, j))
        #The neighbours for LEFT, TOP, RIGHT and DOWN node need to be added
        adjacent_neighbor_nodes_dict[num_nodes + UP] = list()
        adjacent_neighbor_nodes_dict[num_nodes + DOWN] = list()
        adjacent_neighbor_nodes_dict[num_nodes + LEFT] = list()
        adjacent_neighbor_nodes_dict[num_nodes + RIGHT] = list()
        list_nodes: list[HexNode] = Board.graph.hex_nodes
        for node in list_nodes:
            if node.node_value < board_size:
                adjacent_neighbor_nodes_dict[num_nodes + UP].append(node)
            elif num_nodes - board_size <= node.node_value < num_nodes:
                adjacent_neighbor_nodes_dict[num_nodes + DOWN].append(node)
            if node.node_value % board_size == 0 and node.node_value < num_nodes:
                adjacent_neighbor_nodes_dict[num_nodes + LEFT].append(node)
            elif node.node_value % board_size == board_size - 1:
                adjacent_neighbor_nodes_dict[num_nodes + RIGHT].append(node)

    @staticmethod
    def create_initial_nodes_and_board():
        new_board = list()
        created_nodes: list[HexNode] = list()
        edges_matrix: list[list[int]]
        Board.hex_nodes_by_position = dict()
        Board.special_hex_nodes = dict()
        board_size = Board.board_size
        value_counter = 0
        for i in range(board_size):
            new_board.append(list())
            for j in range(board_size):
                new_board[i].append(UNOCCUPIED)
                new_node = HexNode(position=(i, j), node_value=value_counter)
                created_nodes.append(new_node)
                Board.hex_nodes_by_position[(i, j)] = new_node
                value_counter += 1
        new_node = HexNode(None, value_counter + LEFT, PLAYER_1_TOKEN)
        Board.hex_nodes_by_position['L'] = new_node
        created_nodes.append(new_node)
        new_node = HexNode(None, value_counter + UP, PLAYER_2_TOKEN)
        Board.hex_nodes_by_position['U'] = new_node
        created_nodes.append(new_node)
        new_node = HexNode(None, value_counter + RIGHT, PLAYER_1_TOKEN)
        Board.hex_nodes_by_position['R'] = new_node
        created_nodes.append(new_node)
        new_node = HexNode(None, value_counter + DOWN, PLAYER_2_TOKEN)
        Board.hex_nodes_by_position['D'] = new_node
        created_nodes.append(new_node)
        Board.board = numpy.array(new_board)
        num_nodes = board_size * board_size + 4
        edges_matrix = [[10000 for _ in range(num_nodes)] for _ in range(num_nodes)]
        Board.graph = HexGraph(board_size=Board.board_size, hex_nodes=created_nodes, edges_matrix=edges_matrix)
        Board.update_initial_edges()

    @staticmethod
    def update_initial_edges():
        nodes_list = Board.graph.hex_nodes
        physical_nodes_num = Board.board_size * Board.board_size
        for node in nodes_list:
            node_value = node.node_value
            module_value = node_value % Board.board_size
            if node_value < physical_nodes_num:
                if 0 <= node_value - Board.board_size <= physical_nodes_num - 1:
                    Board.graph.update_edge_value(node_value, node_value - Board.board_size, 1, 1)
                if 0 <= node_value + Board.board_size <= physical_nodes_num - 1:
                    Board.graph.update_edge_value(node_value, node_value + Board.board_size, 1, 1)
                if module_value != Board.board_size - 1: #not last column
                    if 0 <= node_value - Board.board_size + 1 <= physical_nodes_num - 1:
                        Board.graph.update_edge_value(node_value, node_value - Board.board_size + 1, 1, 1)
                    if 0 <= node_value + 1 <= physical_nodes_num - 1:
                        Board.graph.update_edge_value(node_value, node_value + 1, 1, 1)
                else:  # last column
                    Board.graph.update_edge_value(node_value, physical_nodes_num + RIGHT, 0, 1)
                if module_value != 0: # not first column
                    if 0 <= node_value + Board.board_size - 1 <= physical_nodes_num - 1:
                        Board.graph.update_edge_value(node_value, node_value + Board.board_size - 1, 1, 1)
                    if 0 <= node_value - 1 <= physical_nodes_num - 1:
                        Board.graph.update_edge_value(node_value, node_value - 1, 1, 1)
                else:  # first column
                    Board.graph.update_edge_value(node_value, physical_nodes_num + LEFT, 0, 1)
                if 0 <= node_value < Board.board_size: #first row
                    Board.graph.update_edge_value(node_value, physical_nodes_num + UP, 0, 1)
                if physical_nodes_num - Board.board_size <= node_value < physical_nodes_num: #last row
                    Board.graph.update_edge_value(node_value, physical_nodes_num + DOWN, 0, 1)
            # print(node_value)
            # print(Board.graph.edges_matrix[node_value])

    def to_string(self):
        return self.board.tostring()

    def clear_board(self):
        """
        Reset the board
        """
        #self.create_initial_nodes_and_board()
        board_size = Board.board_size
        num_nodes = board_size * board_size + 4
        for i in range(board_size):
            for j in range(board_size):
                Board.board[i][j] = UNOCCUPIED
                node = Board.hex_nodes_by_position[(i, j)]
                node.status = UNOCCUPIED
        Board.graph.edges_matrix = [[10000 for _ in range(num_nodes)] for _ in range(num_nodes)]
        Board.update_initial_edges()
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
        resulting_list: list[HexNode] = list()
        neighbour_nodes = adjacent_neighbor_nodes_dict[current_node.node_value]
        for node in neighbour_nodes:
            if node.status == UNOCCUPIED or node.status == player_token:
                resulting_list.append(node)
        return resulting_list

    @staticmethod
    def get_available_nodes():
        list_available_nodes: list[HexNode] = list()
        all_nodes = Board.graph.hex_nodes
        for node in all_nodes:
            if node.status == UNOCCUPIED:
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
    def get_occupied_tiles(player_token: int) -> list[tuple[int, int]]:
        """
        Get all occupied tiles by player with player_token
        """
        return [(i, j) for j in range(Board.board_size) for i in range(Board.board_size) if Board.board[i, j] == player_token]
    
    @staticmethod
    def get_bridge_reward(player_token: int) -> float:
        reward: float = 0
        player_tiles = Board.get_occupied_tiles(player_token)
        for tile in player_tiles:
            i, j = tile
            # top bridge
            if Board.tile_in_board((i - 1, j)) and Board.tile_in_board((i - 1, j + 1)):
                if Board.board[i - 1, j] == UNOCCUPIED and Board.board[i - 1, j + 1] == UNOCCUPIED:
                    reward += 0.25
                    if Board.tile_in_board((i - 2, j + 1)):
                        if Board.board[i - 2, j + 1] == player_token:
                            reward += 0.25
                    elif player_token == PLAYER_2_TOKEN:
                        reward += 0.75
            # top right bridge
            if Board.tile_in_board((i - 1, j + 1)) and Board.tile_in_board((i, j + 1)):
                if Board.board[i - 1, j + 1] == UNOCCUPIED and Board.board[i, j + 1] == UNOCCUPIED:
                    reward += 0.25
                    if Board.tile_in_board((i - 1, j + 2)):
                        if Board.board[i - 1, j + 2] == player_token:
                            reward += 0.25
                    elif player_token == PLAYER_1_TOKEN:
                        reward += 0.75
            # top left bridge
            if Board.tile_in_board((i - 1, j)) and Board.tile_in_board((i, j - 1)):
                if Board.board[i - 1, j] == UNOCCUPIED and Board.board[i, j - 1] == UNOCCUPIED:
                    reward += 0.25
                    if Board.tile_in_board((i - 1, j - 1)):
                        if Board.board[i - 1, j - 1] == player_token:
                            reward += 0.25
                    else:
                        reward += 0.25
            # bottom bridge
            if Board.tile_in_board((i + 1, j)) and Board.tile_in_board((i + 1, j - 1)):
                if Board.board[i + 1, j] == UNOCCUPIED and Board.board[i + 1, j - 1] == UNOCCUPIED:
                    reward += 0.25
                    if Board.tile_in_board((i + 2, j - 1)):
                        if Board.board[i + 2, j - 1] == player_token:
                            reward += 0.25
                    elif player_token == PLAYER_2_TOKEN:
                        reward += 0.75
            # bottom right bridge
            if Board.tile_in_board((i + 1, j)) and Board.tile_in_board((i, j + 1)):
                if Board.board[i + 1, j] == UNOCCUPIED and Board.board[i, j + 1] == UNOCCUPIED:
                    reward += 0.25
                    if Board.tile_in_board((i + 1, j + 1)):
                        if Board.board[i + 1, j + 1] == player_token:
                            reward += 0.25
                    else:
                        reward += 0.25
            # bottom left bridge
            if Board.tile_in_board((i + 1, j - 1)) and Board.tile_in_board((i, j - 1)):
                if Board.board[i + 1, j - 1] == UNOCCUPIED and Board.board[i, j - 1] == UNOCCUPIED:
                    reward += 0.25
                    if Board.tile_in_board((i + 1, j - 2)):
                        if Board.board[i + 1, j - 2] == player_token:
                            reward += 0.25
                    elif player_token == PLAYER_1_TOKEN:
                        reward += 0.75
        return reward / len(player_tiles)

    @staticmethod
    def tile_in_board(tile_pos: tuple[int, int]) -> bool:
        i, j = tile_pos
        if 0 <= i < Board.board_size and 0 <= j < Board.board_size:
            return True
        return False

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

    def get_neighbouring_nodes(self, node_position: tuple[int, int]) -> list[HexNode]:
        adjacent_neighbor_positions = adjacent_neighbors_dict[node_position]
        all_neighbouring_nodes: list[HexNode] = list()
        for neighbor_position in adjacent_neighbor_positions:
            all_neighbouring_nodes.append(self.hex_nodes_by_position[neighbor_position])
        row = node_position[0]
        column = node_position[1]
        #if it is a node in the first row, TOP is also their neighbour
        if row == 0:
            all_neighbouring_nodes.append(self.hex_nodes_by_position['U'])
        #if it is a node in the last row, DOWN is also their neighbour
        elif row == Board.board_size - 1:
            all_neighbouring_nodes.append(self.hex_nodes_by_position['D'])
        # if it is a node in the first column, LEFT is also their neighbour
        if column == 0:
            all_neighbouring_nodes.append(self.hex_nodes_by_position['L'])
        # if it is a node in the last column, RIGHT is also their neighbour
        elif column == Board.board_size - 1:
            all_neighbouring_nodes.append(self.hex_nodes_by_position['R'])
        return all_neighbouring_nodes

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
