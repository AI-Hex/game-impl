import pygame, random
from board import PLAYER_1_TOKEN, PLAYER_2_TOKEN
from pygame.locals import *


# Colors            #R   #G   #B
BLACK           = (  0,   0,   0)
WHITE           = (255, 255, 255)
PASTEL_BLUE     = ( 61, 232, 239)
DARK_PINK       = (195,  79, 244)
LIGHT_ORANGE    = (255, 181,  31)

FPS = 4


class Graphics(object):

    window_width: int 
    window_height: int 

    board_width: int
    board_height: int
    board_width_in_tiles: int
    tile_width: int

    board_size: int
    click_board: tuple[tuple[pygame.Rect]] 
    '''Contains collision area of hex tiles clickable for the player'''

    display_surface: pygame.Surface
    '''Contains elements to be displayed on the window'''

    hex_image: pygame.Surface
    token_image: pygame.Surface
    token_image_player_1: pygame.Surface
    token_image_player_2: pygame.Surface

    def __init__(self, board_size: int):
        """
        Initialize the graphics for the game
        """
        self.window_width = 800 # Default: 800
        self.window_height = 600 # Default: 600

        self.board_size = board_size

        self.board_width = 512 # Default: 512
        self.board_width_in_tiles = (3 * self.board_size - 1) / 2
        self.tile_width = int(self.board_width / self.board_width_in_tiles) 
        self.board_height = self.board_size * self.tile_width

        self.click_board = tuple([tuple([pygame.Rect((
                    (self.window_width - self.board_width) / 2 + j * self.tile_width + i * self.tile_width / 2,
                    (self.window_height - self.board_height) / 2 + i * self.tile_width
                ), (self.tile_width, self.tile_width)) for j in range(self.board_size)]) for i in range(self.board_size)])
        
        # Load, scale and color images
        self.hex_image = pygame.image.load('Sprites\hex_border.png')
        self.hex_image = pygame.transform.smoothscale(self.hex_image, (self.tile_width, self.tile_width * self.hex_image.get_height() / self.hex_image.get_width()))
        self.hex_image.fill(PASTEL_BLUE, special_flags=BLEND_RGB_ADD)
        self.token_image = pygame.image.load('Sprites\playing_token.png')
        self.token_image = pygame.transform.smoothscale(self.token_image, (self.tile_width, self.tile_width))
        self.token_image_player_1 = self.token_image.copy()
        self.token_image_player_1.fill(DARK_PINK, special_flags=BLEND_RGB_MULT)
        self.token_image_player_2 = self.token_image.copy()
        self.token_image_player_2.fill(LIGHT_ORANGE, special_flags=BLEND_RGB_MULT)
        
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Hex')
        pygame.display.set_icon(self.token_image)

    def draw_grid(self):
        self.display_surface.fill(BLACK)
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.display_surface.blit(self.hex_image, self.click_board[i][j])
    
    def draw_move(self, player_move: tuple[int], player_token: int):
        row, column = player_move
        if player_token == PLAYER_1_TOKEN:
            self.display_surface.blit(self.token_image_player_1, self.click_board[row][column])
        else:
            self.display_surface.blit(self.token_image_player_2, self.click_board[row][column])
