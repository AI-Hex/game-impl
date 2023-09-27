import pygame, sys
from pygame.locals import *
from board import *
from player import *
from graphics import *


class Game(object):
    
    game_board: Board
    game_graphics: Graphics
    player_1: Player
    player_2: Player
    players: list[Player]

    def __init__(self, board_size: int, player_1: Player, player_2: Player):
        """
        Initialize necessary objects for a hex game
        """
        self.game_board = Board(board_size)
        self.game_graphics = Graphics(board_size)
        self.player_1 = player_1
        self.player_2 = player_2
        self.players = [player_1, player_2]
        self.player_turn = 0

    def start(self):
        """
        Start a round of Hex
        """
        self.game_graphics.draw_grid()

        # Game loop
        while True:

            if self.players[self.player_turn].is_ai() is True:
                self.__handle_ai_move()
            else:
                self.__handle_human_move()

            # Advance turn to the next player
            self.player_turn = 1 - self.player_turn

    def __check_for_quit(self, event: pygame.event.Event) -> bool:
        """
        Check if user wants to quit
        """
        if event.type == QUIT: 
            return True
        if event.type == KEYUP:
            if event.key == K_ESCAPE: 
                return True
        return False
    
    def __check_for_move(self, event: pygame.event.Event) -> bool:
        """
        Check if the player made a valid move (clicked a tile)

        Return the row and column of the tile that the player clicked (if possible)
        """
        if event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            for i in range(self.game_board.board_size):
                for j in range(self.game_board.board_size):
                    if self.game_graphics.click_board[i][j].collidepoint(click_x, click_y):
                        if self.game_board.is_tile_occupied((i, j)) is False:
                            return True
                        return False
        return False

    def __check_for_win(self, player_turn: int):
        if self.game_board.check_victory() is True:
            self.game_graphics.animate_win_path(self.game_board.get_win_path(), player_turn + 1)
            pygame.time.wait(1000)
            self.__terminate()

    def __check_for_reset(self, event: pygame.event.Event) -> bool:
        if event.type == KEYUP:
            if event.key == K_SPACE:
                return True
        return False
    
    def __translate_pos_to_move(self, click_pos: tuple[float, float]) -> tuple[int, int] | None:
        click_x, click_y = click_pos
        for i in range(self.game_board.board_size):
            for j in range(self.game_board.board_size):
                if self.game_graphics.click_board[i][j].collidepoint(click_x, click_y):
                    return i, j
        return None

    def __reset_game(self):
        self.game_graphics.draw_grid()
        self.game_board.clear_board()
        self.player_turn = 1  # end the turn on the second player

    def __handle_ai_move(self):
        tile_pos = self.players[self.player_turn].get_move(self.game_board)
        if tile_pos is not None and self.game_board.is_tile_occupied(tile_pos) is False:
            self.game_board.make_move(tile_pos, self.players[self.player_turn].token)
            self.game_graphics.draw_move(tile_pos, self.players[self.player_turn].token)
        self.__check_for_win(self.player_turn)

    def __handle_move(self, tile_pos: tuple[int, int]):
        self.game_board.make_move(tile_pos, self.players[self.player_turn].token)
        self.game_graphics.draw_move(tile_pos, self.players[self.player_turn].token)
        self.__check_for_win(self.player_turn)

    def __check_for_pause(self, event: pygame.event.Event) -> bool:
        if event.type == KEYUP:
            if event.key == K_TAB:
                return True
        return False
    
    def __pause_game(self):
        self.game_graphics.draw_paused_game()
        while True:
            # handle pause
            pygame.time.wait(2000)
            break
        # exit pause
        self.game_graphics.draw_board(self.game_board.board)

    def __terminate(self):
        pygame.quit()
        sys.exit()

    def __handle_human_move(self):
        # Player loop
        while True:
            for event in pygame.event.get():
                if self.__check_for_quit(event) is True:
                    self.__terminate()
                if self.__check_for_reset(event) is True:
                    self.__reset_game()
                    return
                if self.__check_for_move(event) is True:
                    self.__handle_move(self.__translate_pos_to_move(event.pos))
                    return
                if self.__check_for_pause(event) is True:
                    self.__pause_game()

    # """ GARBAGE CODE """
    # # checking if neighboring cells work
    # def __handle_human_move_test(self, player_turn: int):
    #     # Player loop
    #     while True:
    #         self.__check_for_quit()
    #         tile_pos = self.__check_for_move()
    #         if tile_pos is not None and self.game_board.is_tile_occupied(tile_pos) is False:
    #             self.game_board.make_move(tile_pos, self.players[player_turn].token)
    #             self.game_graphics.draw_move(tile_pos, self.players[player_turn].token)
    #             all_neighbors = self.game_board.get_neighboring_tiles_by_token(tile_pos, UNOCCUPIED)
    #             for neighbor in all_neighbors:
    #                 self.game_board.make_move(neighbor, self.players[player_turn].token)
    #                 self.game_graphics.draw_move(neighbor, self.players[player_turn].token)
    #             break
    #     self.__check_for_win(player_turn)
