import copy

UNOCCUPIED = 0
PLAYER_1_TOKEN = 1
PLAYER_2_TOKEN = 2


class HexNode(object):
    position: tuple[int, int]
    status: int
    node_value: int

    def __init__(self, position: tuple[int, int], node_value: int, status: int = UNOCCUPIED):
        self.position = position
        self.status = status
        self.node_value = node_value

    def __copy__(self):
        new_node = HexNode(self.position, self.node_value, self.status)
        return new_node


class HexGraph(object):
    hex_nodes: list[HexNode]
    board_size: int
    edges_matrix: list[list[int]]

    def __init__(self, board_size: int, hex_nodes: list[HexNode], edges_matrix: list[list[int]]):
        self.board_size = board_size
        self.hex_nodes = hex_nodes
        self.edges_matrix = edges_matrix
        """
            The edges connecting the last column to the right node, and the last row to the bottom node have value 0
        """

    def __copy__(self):
        return HexGraph(self.board_size, copy.deepcopy(self.hex_nodes), copy.deepcopy(self.edges_matrix))


    def update_edge_value(self, node_value_1, node_value_2, new_distance):
        self.edges_matrix[node_value_1][node_value_2] = new_distance
        self.edges_matrix[node_value_2][node_value_1] = new_distance

    def get_first_column_tiles(self, player_token: int) -> list[HexNode]:
        return [node for node in self.hex_nodes if node.node_value % self.board_size == 0 and (node.status == player_token or node.status == UNOCCUPIED)]

    def get_first_row_tiles(self, player_token: int) -> list[HexNode]:
        return [node for node in self.hex_nodes if node.node_value < self.board_size and (node.status == player_token or node.status == UNOCCUPIED)]

