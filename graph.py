import copy

UNOCCUPIED = 0
PLAYER_1_TOKEN = 1
PLAYER_2_TOKEN = 2


class HexNode(object):

    def __init__(self, position: tuple[int, int], node_value: int | None, status: int = UNOCCUPIED):
        self.position: tuple[int, int] = position
        self.status: int = status
        self.node_value: int = node_value
        # Used in the two distance evaluation function
        self.td_value: int | None = None
        self.td_neighbour_values_list: list[int] = list()

    def __copy__(self):
        new_node = HexNode(self.position, self.node_value, self.status)
        return new_node

    def is_special_node(self):
        return False


class SpecialHexNode(HexNode):

    def __init__(self, position: tuple[int, int], node_value: int | None, status: int = UNOCCUPIED,
                 special_node_identifier: str = 'L'):
        super(SpecialHexNode, self).__init__(position, node_value, status)
        # If it is a special node, special_node_identifier will have one of the following values: L, R, U, D.
        self.special_node_identifier: str = special_node_identifier

    def is_special_node(self):
        return True


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

    def update_edge_value(self, node_value_1, node_value_2, new_distance_for_1, new_distance_for_2):
        self.edges_matrix[node_value_1][node_value_2] = new_distance_for_1
        self.edges_matrix[node_value_2][node_value_1] = new_distance_for_2

    def get_first_column_tiles(self, player_token: int) -> list[HexNode]:
        return [node for node in self.hex_nodes if node.node_value % self.board_size == 0 and (node.status == player_token or node.status == UNOCCUPIED)]

    def get_first_row_tiles(self, player_token: int) -> list[HexNode]:
        return [node for node in self.hex_nodes if node.node_value < self.board_size and (node.status == player_token or node.status == UNOCCUPIED)]

    def reset_td_values(self):
        for node in self.hex_nodes:
            node.td_value = None
            node.td_neighbour_values_list = list()