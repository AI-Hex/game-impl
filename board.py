import pygame, numpy

# State of tile pieces in board
UNOCCUPIED = 0
PLAYER_1_TOKEN = 1
PLAYER_2_TOKEN = 2

move_list = {}


def store(depth, state, move, score):
    """Store record in the table

    Args:
        depth (int): Search depth
        state (HexBoard): Board state
        move (tuple): Best move for the board state
        score (int): Score assigned to that state
    """
    if state not in move_list:
        move_list[state] = {}

    move_list[state][depth] = (move, score)


def lookup(depth, state) -> tuple[float, tuple[int, int]]:
    """Checks if TT contains a record for the given state

    Args:
        depth (int): Search depth
        state (HexBoard): Board state

    Returns:
        int: 0: no entry found, 1: state found but lower than desired depth, 2:state found at desired depth
        tuple: Best move for the state
        int: Assigned score of the state
    """

    if state in move_list:
        # State was already stored
        if depth in move_list[state]:
            # State of current depth was found so return move of that one
            return move_list[state][depth][1], move_list[state][depth][0]
        else:
            # State was not found on this depth -> return False but still give best move found.
            depths = [d for d in move_list[state]]

            if len(depths) == 0:
                return None, (None, None)  # if No entries found at all

            maxdepth = numpy.max(depths)  # take only max depth

            return move_list[state][maxdepth][1], move_list[state][maxdepth][0]  # Return the best move for max depth

    return None, (None, None)


class Board(object):
    """
    Class containing data structures for the hex board
    """

    board: numpy.ndarray
    '''Keeps track of the tokens (or lack of tokens) on the board'''
    board_size: int

    def __init__(self, board_size: int):
        """
        Initialize an empty hex board
        """
        self.board = numpy.array([[UNOCCUPIED for _ in range(board_size)] for _ in range(board_size)])
        self.board_size = board_size

    def to_string(self):
        return self.board.tostring()

    def clear_board(self):
        """
        Reset the board
        """
        self.board = numpy.array([[UNOCCUPIED for _ in range(self.board_size)] for _ in range(self.board_size)])
    
    def is_empty(self):
        """
        Check if board is empty
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] != UNOCCUPIED:
                    return False
        return True

    def make_move(self, tile_pos: tuple[int, int], player_token: int):
        """
        Place a player token on an unoccupied tile
        """
        row, column = tile_pos
        self.board[row, column] = player_token

    def is_tile_occupied(self, tile_pos: tuple[int, int]) -> bool:
        """
        Return whether the tile is occupied by a player's token
        """
        row, column = tile_pos
        return self.board[row, column] != UNOCCUPIED

    def get_unoccupied_tiles(self) -> list[tuple[int, int]]:
        """
        Get all unoccupied tiles
        """
        return [(i, j) for j in range(self.board_size) for i in range(self.board_size) if self.board[i, j] == UNOCCUPIED]

    def get_neighboring_tiles(self, tile_pos: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Return neighboring tiles of a given tile
        """
        result: list[tuple[int, int]]
        result = list()
        row, column = tile_pos
        if 0 <= row - 1:
            result.append((row - 1, column))
        if 0 <= row - 1 and column + 1 < self.board_size:
            result.append((row - 1, column + 1))
        if 0 <= column - 1:
            result.append((row, column - 1))
        if column + 1 < self.board_size:
            result.append((row, column + 1))
        if row + 1 < self.board_size and 0 <= column - 1:
            result.append((row + 1, column - 1))
        if row + 1 < self.board_size:
            result.append((row + 1, column))
        return result

    def get_neighboring_tiles_by_token(self, tile_pos: tuple[int, int], by_token: int | None = None) -> list[tuple[int, int]]:
        """
        Return neighboring tiles of a given tile

        Furthermore, filter by UNOCCUPIED, PLAYER_1_TOKEN, PLAYER_2_TOKEN or None
        """
        result = self.get_neighboring_tiles(tile_pos)
        if by_token is None:
            return result
        if by_token == UNOCCUPIED:
            return [(i, j) for (i, j) in result if self.board[i, j] == UNOCCUPIED]
        if by_token == PLAYER_1_TOKEN:
            return [(i, j) for (i, j) in result if self.board[i, j] == PLAYER_1_TOKEN]
        if by_token == PLAYER_2_TOKEN:
            return [(i, j) for (i, j) in result if self.board[i, j] == PLAYER_2_TOKEN]

    def __is_tile_on_right_border(self, tile_pos: tuple[int, int]) -> bool:
        """
        Check if tile is on the right border
        """
        row, column = tile_pos
        return column == self.board_size - 1

    def __is_tile_on_bottom_border(self, tile_pos: tuple[int, int]) -> bool:
        """
        Check if tile is on the bottom border
        """
        row, column = tile_pos
        return row == self.board_size - 1

    def __check_player_1_win(self) -> bool:
        """
        Check if player 1 wins
        """
        visited_tiles = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        queue = list()
        for row in range(self.board_size):
            if self.board[row, 0] == PLAYER_1_TOKEN:
                queue.append((row, 0))
        while len(queue) > 0:
            i, j = queue.pop(0)
            if visited_tiles[i][j] is True:
                continue
            visited_tiles[i][j] = True
            if self.__is_tile_on_right_border((i, j)) is True:
                return True
            queue.extend(self.get_neighboring_tiles_by_token((i, j), PLAYER_1_TOKEN))
        return False

    def __check_player_2_win(self) -> bool:
        """
        Check if player 2 wins
        """
        visited_tiles = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        queue = list()
        for column in range(self.board_size):
            if self.board[0, column] == PLAYER_2_TOKEN:
                queue.append((0, column))
        while len(queue) > 0:
            i, j = queue.pop(0)
            if visited_tiles[i][j] is True:
                continue
            visited_tiles[i][j] = True
            if self.__is_tile_on_bottom_border((i, j)) is True:
                return True
            queue.extend(self.get_neighboring_tiles_by_token((i, j), PLAYER_2_TOKEN))
        return False

    def check_victory(self) -> bool:
        """
        Check if one of the players won the game
        """
        if self.__check_player_1_win() is True or self.__check_player_2_win() is True:
            return True
        return False

    def __get_player_1_win_path(self) -> list[tuple[int, int]] | None:
        """
        Get the winning path for player 1
        """
        visited_tiles = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        path, queue = list(), list()
        win_path_flag = False
        for row in range(self.board_size):
            if win_path_flag is True:
                break
            else:
                path = list()  # last iteration was fruitless, continue with empty list
            if self.board[row, 0] == PLAYER_1_TOKEN:
                queue.append((row, 0))
                while len(queue) > 0:
                    i, j = queue.pop(0)
                    if visited_tiles[i][j] is True:
                        continue
                    visited_tiles[i][j] = True
                    path.append((i, j))
                    if self.__is_tile_on_right_border((i, j)) is True:
                        win_path_flag = True
                    queue.extend(self.get_neighboring_tiles_by_token((i, j), PLAYER_1_TOKEN))
        if win_path_flag is True:
            return path
        return None

    def __get_player_2_win_path(self) -> list[tuple[int, int]] | None:
        """
        Get the winning path for player 2
        """
        visited_tiles = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        path, queue = list(), list()
        win_path_flag = False
        for column in range(self.board_size):
            if win_path_flag is True:
                break
            else:
                path = list()  # last itteration was fruitless, continue with empty list
            if self.board[0, column] == PLAYER_2_TOKEN:
                queue.append((0, column))
                while len(queue) > 0:
                    i, j = queue.pop(0)
                    if visited_tiles[i][j] is True:
                        continue
                    visited_tiles[i][j] = True
                    path.append((i, j))
                    if self.__is_tile_on_bottom_border((i, j)) is True:
                        win_path_flag = True
                    queue.extend(self.get_neighboring_tiles_by_token((i, j), PLAYER_2_TOKEN))
        if win_path_flag is True:
            return path
        return None

    def get_win_path(self) -> list[tuple[int, int]] | None:
        """
        Get the path that won the game
        """
        if self.__check_player_1_win() is True:
            return self.__get_player_1_win_path()
        if self.__check_player_2_win() is True:
            return self.__get_player_2_win_path()
        return None

    def get_win_token(self) -> int | None:
        """
        Get winner
        """
        if self.__check_player_1_win() is True:
            return PLAYER_1_TOKEN
        if self.__check_player_2_win() is True:
            return PLAYER_2_TOKEN
        return None

