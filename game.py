import pygame, sys
from pygame.locals import *
from board import *
from player import *
from graphics import *


class Game(object):
    """
    Class consisting of all elements required for the game of hex
    """
    
    game_board: Board
    game_graphics: Graphics
    player_1: Player
    player_2: Player
    players: list[Player]

    def __init__(self, board_size: int, player_1: Player, player_2: Player):
        """
        Initialize necessary objects for a hex game
        """
        Game.game_board = Board(board_size)
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
        """
        if event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            for i in range(self.game_board.board_size):
                for j in range(self.game_board.board_size):
                    if self.game_graphics.click_board[i][j].collidepoint(click_x, click_y):
                        if self.game_board.is_tile_occupied((i, j)) == False:
                            return True
                        return False
        return False

    def __check_for_win(self, player_turn: int):
        """
        Check and handle player win
        """
        if self.game_board.check_victory() is True:
            self.game_graphics.animate_win_path(self.game_board.get_win_path(), player_turn + 1)
            #print(move_list)
            while True:
                for event in pygame.event.get():
                    if self.__check_for_quit(event) is True:
                        self.__terminate()
                    if self.__check_for_reset(event) is True:
                        self.__reset_game()
                        return
                    if self.__check_for_pause(event) is True:
                        self.__pause_game()
                if self.game_board.is_empty() is True:
                    return
        self.game_graphics.draw_turn(1 - player_turn)  # If player hasn't won, display the turn of the next player

    def __check_for_reset(self, event: pygame.event.Event) -> bool:
        """
        Check requirements for resetting board 
        """
        self.game_graphics.animate_reset_text()
        if event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            if self.game_graphics.reset_text_box.collidepoint(click_x, click_y) is True:
                return True
        if event.type == KEYUP:
            if event.key == K_SPACE:
                return True
        return False
    
    def __translate_pos_to_move(self, click_pos: tuple[float, float]) -> tuple[int, int] | None:
        """
        Translate coordinates of mouse click to tile position if possible
        """
        click_x, click_y = click_pos
        for i in range(self.game_board.board_size):
            for j in range(self.game_board.board_size):
                if self.game_graphics.click_board[i][j].collidepoint(click_x, click_y):
                    return i, j
        return None

    def __reset_game(self):
        """
        Handle reset of game board
        """
        self.game_graphics.draw_grid()
        self.game_board.clear_board()
        self.player_turn = 1  # end the turn on the second player

    def __handle_ai_move(self):
        """
        Handle AI's turn to make a move on the board
        """
        tile_pos = self.players[self.player_turn].get_move()
        assert tile_pos != None
        if tile_pos is not None and not self.game_board.is_tile_occupied(tile_pos):
            self.game_board.make_move(tile_pos, self.players[self.player_turn].token)
            self.game_graphics.draw_move(tile_pos, self.players[self.player_turn].token)
        self.__check_for_win(self.player_turn)

    def __handle_move(self, tile_pos: tuple[int, int]):
        """
        Handle player's made move on the board
        """
        self.game_board.make_move(tile_pos, self.players[self.player_turn].token)
        self.game_graphics.draw_move(tile_pos, self.players[self.player_turn].token)
        self.__check_for_win(self.player_turn)

    def __check_for_pause(self, event: pygame.event.Event) -> bool:
        """
        Check if settings menu should be openned
        """
        self.game_graphics.animate_settings_text()
        if event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            if self.game_graphics.settings_text_box.collidepoint(click_x, click_y):
                return True
        if event.type == KEYUP:
            if event.key == K_TAB:
                return True
        return False
    
    def __pause_game(self):
        """
        Set the game in a pause state and return safely from it 
        """
        self.__handle_paused_game()
        self.game_graphics.draw_board(self.game_board.board)

    def __handle_paused_game(self):
        """
        Open settings menu and handle pause state
        """
        player_1_human_flag = self.player_1.is_human()
        player_2_human_flag = self.player_2.is_human()
        self.game_graphics.draw_paused_game(player_1_human_flag, player_2_human_flag)

        while True: 
            for event in pygame.event.get():
                if self.__check_for_quit(event) is True:
                    self.__terminate()
                if event.type == MOUSEBUTTONUP:
                    click_x, click_y = event.pos
                    if self.game_graphics.player_1_human_box.collidepoint(click_x, click_y) is True:
                        player_1_human_flag = True
                    if self.game_graphics.player_1_ai_box.collidepoint(click_x, click_y) is True:
                        player_1_human_flag = False
                    if self.game_graphics.player_2_human_box.collidepoint(click_x, click_y) is True:
                        player_2_human_flag = True
                    if self.game_graphics.player_2_ai_box.collidepoint(click_x, click_y) is True:
                        player_2_human_flag = False
                    if self.game_graphics.go_back_box.collidepoint(click_x, click_y) is True:
                        return
                    if self.game_graphics.save_changes_box.collidepoint(click_x, click_y) is True:
                        self.__change_players(player_1_human_flag, player_2_human_flag)
                        self.__reset_game()
                        return
                    self.game_graphics.draw_paused_game(player_1_human_flag, player_2_human_flag)

    def __change_players(self, player_1_human_flag: bool, player_2_human_flag: bool):
        if player_1_human_flag is True:
            self.player_1 = Human_Player(1)
        else:
            self.player_1 = AI_Random_Player(1)
        if player_2_human_flag is True:
            self.player_2 = Human_Player(2)
        else:
            self.player_2 = AI_Random_Player(2)            
        self.players[0] = self.player_1
        self.players[1] = self.player_2

    def __terminate(self):
        """
        Exit the game
        """
        pygame.quit()
        sys.exit()

    def __handle_human_move(self):
        """
        Handle initial player interactions with the active game board
        """
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
                    return
