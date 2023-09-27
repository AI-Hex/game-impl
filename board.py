import pygame

# State of tile pieces in board
UNOCCUPIED = 0
PLAYER_1_TOKEN = 1
PLAYER_2_TOKEN = 2


class Board(object):
    board: list[list[int]]
    """Keeps track of the tokens (or lack of tokens) on the board"""
    board_size: int

    def __init__(self, board_size: int):
        """
        Initialize an empty hex board
        """
        self.board = [[UNOCCUPIED for _ in range(board_size)] for _ in range(board_size)]
        self.board_size = board_size

    def clear_board(self):
        """
        Reset the board
        """
        self.board = [[UNOCCUPIED for _ in range(self.board_size)] for _ in range(self.board_size)]

    def make_move(self, tile_pos: tuple[int, int], player_token: int):
        """
        Place a player token on an unoccupied tile
        """
        row, column = tile_pos
        self.board[row][column] = player_token

    def is_tile_occupied(self, tile_pos: tuple[int, int]) -> bool:
        """
        Return whether the tile is occupied by a player's token
        """
        row, column = tile_pos
        return self.board[row][column] != UNOCCUPIED

    def get_unoccupied_tiles(self) -> list[tuple[int, int]]:
        return [(i, j) for j in range(self.board_size) for i in range(self.board_size) if
                self.board[i][j] == UNOCCUPIED]

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
            return [(i, j) for (i, j) in result if self.board[i][j] == UNOCCUPIED]
        if by_token == PLAYER_1_TOKEN:
            return [(i, j) for (i, j) in result if self.board[i][j] == PLAYER_1_TOKEN]
        if by_token == PLAYER_2_TOKEN:
            return [(i, j) for (i, j) in result if self.board[i][j] == PLAYER_2_TOKEN]

    def __is_tile_on_right_border(self, tile_pos: tuple[int, int]) -> bool:
        row, column = tile_pos
        return column == self.board_size - 1

    def __is_tile_on_bottom_border(self, tile_pos: tuple[int, int]) -> bool:
        row, column = tile_pos
        return row == self.board_size - 1

    def __check_player_1_win(self) -> bool:
        visited_tiles = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        queue = list()
        for row in range(self.board_size):
            if self.board[row][0] == PLAYER_1_TOKEN:
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
        visited_tiles = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        queue = list()
        for column in range(self.board_size):
            if self.board[0][column] == PLAYER_2_TOKEN:
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
        visited_tiles = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        path, queue = list(), list()
        win_path_flag = False
        for row in range(self.board_size):
            if win_path_flag is True:
                break
            else:
                path = list()  # clear_board the path added from last wrong itteration
            if self.board[row][0] == PLAYER_1_TOKEN:
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
        visited_tiles = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        path, queue = list(), list()
        win_path_flag = False
        for column in range(self.board_size):
            if win_path_flag is True:
                break
            else:
                path = list()  # clear_board the path added from last wrong itteration
            if self.board[0][column] == PLAYER_2_TOKEN:
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
        if self.__check_player_1_win() is True:
            return self.__get_player_1_win_path()
        if self.__check_player_2_win() is True:
            return self.__get_player_2_win_path()
        return None

    def get_win_token(self) -> int | None:
        if self.__check_player_1_win() is True:
            return PLAYER_1_TOKEN
        if self.__check_player_2_win() is True:
            return PLAYER_2_TOKEN
        return None
