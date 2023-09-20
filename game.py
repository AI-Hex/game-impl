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

    def start(self):
        """
        Start a round of Hex
        """
        self.game_graphics.draw_grid()
        pygame.display.update()

        player_turn = 0

        # Game loop
        while True:

            if self.players[player_turn].is_ai() == True:
                tile_pos = self.players[player_turn].get_move(self.game_board)
                if tile_pos != None and self.game_board.occupies(tile_pos) == False:
                    self.game_board.make_move(tile_pos, self.players[player_turn].token)
                    self.game_graphics.draw_move(tile_pos, self.players[player_turn].token)
            else:
                # Player loop
                while True:
                    self.__check_for_quit()
                    tile_pos = self.__check_for_move()
                    if tile_pos != None and self.game_board.occupies(tile_pos) == False:
                        self.game_board.make_move(tile_pos, self.players[player_turn].token)
                        self.game_graphics.draw_move(tile_pos, self.players[player_turn].token)
                        break

            pygame.display.update()
            # Advance turn to the next player
            player_turn = 1 - player_turn
        
    def __check_for_quit(self):
        """
        Exit the program if user requests to quit
        """
        for event in pygame.event.get(QUIT):
            self.__terminate()
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                self.__terminate()
    
    def __check_for_move(self) -> tuple[int] | None:
        """
        Check if the player made a move (clicked a tile)

        Return the coordinates of the tile that the player clicked (if possible)
        """
        for event in pygame.event.get(MOUSEBUTTONUP):
            click_x, click_y = event.pos
            for i in range(self.game_board.board_size):
                for j in range(self.game_board.board_size):
                    if self.game_graphics.click_board[i][j].collidepoint(click_x, click_y):
                        return (i, j)
        return None


    def __terminate(self):
        pygame.quit()
        sys.exit()
