import copy

# State of tile pieces in board
UNOCCUPIED = 0
PLAYER_1_TOKEN = 1
PLAYER_2_TOKEN = 2

# Position of special nodes
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3


class HexNode(object):

    def __init__(self, position: tuple[int, int], node_value: int | None, status: int = UNOCCUPIED):
        self.position: tuple[int, int] = position
        self.status: int = status
        self.node_value: int = node_value

        # Variables used in the two distance evaluation function
        self.td_value: int | None = None  # distance from source node to this current node
        self.td_neighbour_values_list: list[int] = list()   # list of distances from source node to neighbor nodes of current node

    def __copy__(self):
        return HexNode(self.position, self.node_value, self.status)


class HexGraph(object):

    hex_nodes: list[HexNode]
    board_size: int
    edges_matrix: list[list[int]]

    def __init__(self, board_size: int, hex_nodes: list[HexNode], edges_matrix: list[list[int]]):
        self.board_size = board_size
        self.hex_nodes = hex_nodes
        self.edges_matrix = edges_matrix
        # The edges connecting the last column to the right node, and the last row to the bottom node have value 0
        
    def __copy__(self):
        return HexGraph(self.board_size, copy.deepcopy(self.hex_nodes), copy.deepcopy(self.edges_matrix))

    def update_edge_value(self, node_value_1: int, node_value_2: int, new_distance_for_1: int, new_distance_for_2: int):
        """
        Update the path cost from two nodes
        """
        self.edges_matrix[node_value_1][node_value_2] = new_distance_for_1
        self.edges_matrix[node_value_2][node_value_1] = new_distance_for_2

    def get_first_column_tiles(self, player_token: int) -> list[HexNode]:
        return [node for node in self.hex_nodes if node.node_value % self.board_size == 0 and node.status in [player_token, UNOCCUPIED]]

    def get_first_row_tiles(self, player_token: int) -> list[HexNode]:
        return [node for node in self.hex_nodes if node.node_value < self.board_size and node.status in [player_token, UNOCCUPIED]]

    def reset_td_values(self):
        """
        Reset the values used in two distance heuristic for self node
        """
        for node in self.hex_nodes:
            node.td_value = None
            node.td_neighbour_values_list = list()
            