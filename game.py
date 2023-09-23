import pygame, sys
from pygame.locals import *
from board import *
from player import *
<<<<<<< HEAD
from graphics import *
=======
>>>>>>> ae7030dff4adc72573dec5a5a6d7c50d9ae02e0e


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

<<<<<<< HEAD
    def start(self):
        """
        Start a round of Hex
        """
        self.game_graphics.draw_grid()
        pygame.display.update()
=======
BOARD: tuple[tuple[pygame.Rect]] # SHOULD BE REMOVED!!!
>>>>>>> ae7030dff4adc72573dec5a5a6d7c50d9ae02e0e

        player_turn = 0

<<<<<<< HEAD
        # Game loop
        while True:
=======
# Board should fit nicely in window
assert BOARD_WIDTH < WINDOW_WIDTH - 30
assert BOARD_HEIGHT < WINDOW_HEIGHT - 30

# Colors            #R   #G   #B
BLACK           = (  0,   0,   0)
WHITE           = (255, 255, 255)
PASTEL_BLUE     = ( 61, 232, 239)
DARK_PINK       = (195,  79, 244)
LIGHT_ORANGE    = (255, 181,  31) 
>>>>>>> ae7030dff4adc72573dec5a5a6d7c50d9ae02e0e

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

<<<<<<< HEAD
=======

def main():
    global DISPLAY_SURFACE, BOARD, HEX_IMAGE, TOKEN_IMAGE, TOKEN_IMAGE_1, TOKEN_IMAGE_2

    pygame.init()

    # Load, scale and color images
    HEX_IMAGE = pygame.image.load('Sprites\hex_border.png')
    HEX_IMAGE = pygame.transform.smoothscale(HEX_IMAGE, (TILE_WIDTH, TILE_WIDTH * HEX_IMAGE.get_height() / HEX_IMAGE.get_width()))
    HEX_IMAGE.fill(PASTEL_BLUE, special_flags=BLEND_RGB_ADD)
    TOKEN_IMAGE = pygame.image.load('Sprites\playing_token.png')
    TOKEN_IMAGE = pygame.transform.smoothscale(TOKEN_IMAGE, (TILE_WIDTH, TILE_WIDTH))
    TOKEN_IMAGE_1 = TOKEN_IMAGE.copy()
    TOKEN_IMAGE_1.fill(DARK_PINK, special_flags=BLEND_RGB_MULT)
    TOKEN_IMAGE_2 = TOKEN_IMAGE.copy()
    TOKEN_IMAGE_2.fill(LIGHT_ORANGE, special_flags=BLEND_RGB_MULT)

    # Initialize main window
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    DISPLAY_SURFACE.fill(BLACK)
    pygame.display.set_caption('Hex -- Version 1.0')
    pygame.display.set_icon(TOKEN_IMAGE)

    BOARD = create_board()
    draw_empty_board(DISPLAY_SURFACE)

    # main game loop
    while True: 
        # Events to be expected:
        # ESC or QUIT should close the game
        # If player's turn, click on board should place token or do nothing otherwise
        # Click on settings should pop up settings window (handled separately)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        if BOARD[i][j].collidepoint(mouse_x, mouse_y):
                            make_move(i, j)
                            break
            
>>>>>>> ae7030dff4adc72573dec5a5a6d7c50d9ae02e0e
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


<<<<<<< HEAD
    def __terminate(self):
        pygame.quit()
        sys.exit()
=======
def draw_empty_board(DISPLAY_SURFACE: pygame.Surface):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            DISPLAY_SURFACE.blit(HEX_IMAGE, BOARD[i][j])


def make_move(row_position: int, column_position: int):
    DISPLAY_SURFACE.blit(TOKEN_IMAGE_1 if random.randint(0, 1) == 0 else TOKEN_IMAGE_2, BOARD[row_position][column_position])


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
>>>>>>> ae7030dff4adc72573dec5a5a6d7c50d9ae02e0e
