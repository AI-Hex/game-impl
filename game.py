import sys
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
    player_turn: int

    def __init__(self, board_size: int, player_1: Player, player_2: Player):
        """
        Initialize necessary objects for a hex game
        """
        Game.game_board = Board(board_size)
        Game.game_graphics = Graphics(board_size)
        Game.player_1 = player_1
        Game.player_2 = player_2
        Game.players = [player_1, player_2]
        Game.player_turn = 0

    def start(self):
        """
        Start a round of Hex
        """
        Game.game_graphics.draw_grid()
        while True:  # Game loop

            if Game.players[Game.player_turn].is_ai() is True:
                self.__handle_ai_move()
            else:
                self.__handle_human_move()

            # Advance turn to the next player
            Game.player_turn = 1 - Game.player_turn

    @staticmethod
    def __check_for_quit(event: pygame.event.Event) -> bool:
        """
        Check if user wants to quit
        """
        if event.type == QUIT: 
            return True
        if event.type == KEYUP:
            if event.key == K_ESCAPE: 
                return True
        return False

    @staticmethod
    def __check_for_move(event: pygame.event.Event) -> bool:
        """
        Check if the player made a valid move (clicked a tile)
        """
        if event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            for i in range(Game.game_board.board_size):
                for j in range(Game.game_board.board_size):
                    if Game.game_graphics.click_board[i][j].collidepoint(click_x, click_y):
                        if not Game.game_board.is_tile_occupied((i, j)):
                            return True
                        return False
        return False

    @staticmethod
    def __check_for_win(player_turn: int):
        """
        Check and handle player win
        """
        if Game.game_board.check_victory() is True:
            Game.game_graphics.animate_win_path(Game.game_board.get_win_path(), player_turn + 1)
            while True:
                for event in pygame.event.get():
                    if Game.__check_for_quit(event) is True:
                        Game.__terminate()
                    if Game.__check_for_reset(event) is True:
                        Game.__reset_game()
                        return
                    if Game.__check_for_pause(event) is True:
                        Game.__pause_game()
                if Game.game_board.is_empty() is True:
                    return
        Game.game_graphics.draw_turn(1 - player_turn)  # If player hasn't won, display the turn of the next player

    @staticmethod
    def __check_for_reset(event: pygame.event.Event) -> bool:
        """
        Check requirements for resetting board 
        """
        Game.game_graphics.animate_reset_text()
        if event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            if Game.game_graphics.reset_text_box.collidepoint(click_x, click_y) is True:
                return True
        if event.type == KEYUP:
            if event.key == K_SPACE:
                return True
        return False

    @staticmethod
    def __translate_pos_to_move(click_pos: tuple[float, float]) -> tuple[int, int] | None:
        """
        Translate coordinates of mouse click to tile position if possible
        """
        click_x, click_y = click_pos
        for i in range(Game.game_board.board_size):
            for j in range(Game.game_board.board_size):
                if Game.game_graphics.click_board[i][j].collidepoint(click_x, click_y):
                    return i, j
        return None

    @staticmethod
    def __reset_game():
        """
        Handle reset of game board
        """
        Game.game_graphics.draw_grid()
        Game.game_board.clear_board()
        Game.player_turn = 1  # end the turn on the second player for the next player to be first player

    @staticmethod
    def __handle_ai_move():
        """
        Handle AI's turn to make a move on the board
        """
        tile_pos = Game.players[Game.player_turn].get_move()
        Game.game_board.make_move(tile_pos, Game.players[Game.player_turn].token)
        Game.game_graphics.draw_move(tile_pos, Game.players[Game.player_turn].token)
        Game.__check_for_win(Game.player_turn)

    @staticmethod
    def __handle_move(tile_pos: tuple[int, int]):
        """
        Handle player's made move on the board
        """
        Game.game_board.make_move(tile_pos, Game.players[Game.player_turn].token)
        Game.game_graphics.draw_move(tile_pos, Game.players[Game.player_turn].token)
        Game.__check_for_win(Game.player_turn)

    @staticmethod
    def __check_for_pause(event: pygame.event.Event) -> bool:
        """
        Check if settings menu should be opened
        """
        Game.game_graphics.animate_settings_text()
        if event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            if Game.game_graphics.settings_text_box.collidepoint(click_x, click_y):
                return True
        if event.type == KEYUP:
            if event.key == K_TAB:
                return True
        return False

    @staticmethod
    def __pause_game():
        """
        Set the game in a pause state and return safely from it 
        """
        Game.__handle_paused_game()
        Game.game_graphics.draw_board(Game.game_board.board)

    @staticmethod
    def __handle_paused_game():
        """
        Open settings menu and handle pause state
        """
        player_1_human_flag = Game.player_1.is_human()
        player_2_human_flag = Game.player_2.is_human()
        Game.game_graphics.draw_paused_game(player_1_human_flag, player_2_human_flag)

        while True: 
            for event in pygame.event.get():
                if Game.__check_for_quit(event) is True:
                    Game.__terminate()
                if event.type == MOUSEBUTTONUP:
                    click_x, click_y = event.pos
                    if Game.game_graphics.player_1_human_box.collidepoint(click_x, click_y) is True:
                        player_1_human_flag = True
                    if Game.game_graphics.player_1_ai_box.collidepoint(click_x, click_y) is True:
                        player_1_human_flag = False
                    if Game.game_graphics.player_2_human_box.collidepoint(click_x, click_y) is True:
                        player_2_human_flag = True
                    if Game.game_graphics.player_2_ai_box.collidepoint(click_x, click_y) is True:
                        player_2_human_flag = False
                    if Game.game_graphics.go_back_box.collidepoint(click_x, click_y) is True:
                        return
                    if Game.game_graphics.save_changes_box.collidepoint(click_x, click_y) is True:
                        Game.__change_players(player_1_human_flag, player_2_human_flag)
                        Game.__reset_game()
                        return
                    Game.game_graphics.draw_paused_game(player_1_human_flag, player_2_human_flag)

    @staticmethod
    def __change_players(player_1_human_flag: bool, player_2_human_flag: bool):
        """
        Instantiate new types for players chosen from selection screen
        """
        if player_1_human_flag is True:
            Game.player_1 = Human_Player(1)
        else:
            Game.player_1 = AI_Minmax_Graph_Player(1)
        if player_2_human_flag is True:
            Game.player_2 = Human_Player(2)
        else:
            Game.player_2 = AI_Minmax_Graph_Player(2)
        Game.players[0] = Game.player_1
        Game.players[1] = Game.player_2

    @staticmethod
    def __terminate():
        """
        Exit the game
        """
        pygame.quit()
        sys.exit()

    @staticmethod
    def __handle_human_move():
        """
        Handle initial player interactions with the active game board
        """
        while True:  # Player loop
            for event in pygame.event.get():
                if Game.__check_for_quit(event) is True:
                    Game.__terminate()
                if Game.__check_for_reset(event) is True:
                    Game.__reset_game()
                    return
                if Game.__check_for_move(event) is True:
                    Game.__handle_move(Game.__translate_pos_to_move(event.pos))
                    return
                if Game.__check_for_pause(event) is True:
                    Game.__pause_game()
                    return
