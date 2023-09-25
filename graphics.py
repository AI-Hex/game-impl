import pygame, random
from board import PLAYER_1_TOKEN, PLAYER_2_TOKEN
from pygame.locals import *


# Colors            #R   #G   #B
BLACK           = (  0,   0,   0)
WHITE           = (255, 255, 255)
BOARD_COLOR     = (0, 0, 0)
PLAYER_1_COLOR  = ( 61, 232, 239)
PLAYER_2_COLOR  = (255, 181,  31)

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
    pause_screen: pygame.Surface

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
        self.hex_image.fill(BOARD_COLOR, special_flags=BLEND_RGB_ADD)
        self.token_image = pygame.image.load('Sprites\playing_token.png')
        self.token_image = pygame.transform.smoothscale(self.token_image, (self.tile_width, self.tile_width))
        self.token_image_player_1 = self.token_image.copy()
        self.token_image_player_1.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_MULT)
        self.token_image_player_2 = self.token_image.copy()
        self.token_image_player_2.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_MULT)
        self.left_border = pygame.image.load('Sprites\left_border.png')
        self.left_border = pygame.transform.smoothscale(self.left_border, (self.tile_width, self.tile_width * self.left_border.get_height() / self.left_border.get_width()))
        self.left_border.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_ADD)
        self.right_border = pygame.image.load('Sprites\\right_border.png')
        self.right_border = pygame.transform.smoothscale(self.right_border, (self.tile_width, self.tile_width * self.right_border.get_height() / self.right_border.get_width()))
        self.right_border.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_ADD)
        self.top_border = pygame.image.load('Sprites\\top_border.png')
        self.top_border = pygame.transform.smoothscale(self.top_border, (self.tile_width, self.tile_width * self.top_border.get_height() / self.top_border.get_width()))
        self.top_border.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_ADD)
        self.bottom_border = pygame.image.load('Sprites\\bottom_border.png')
        self.bottom_border = pygame.transform.smoothscale(self.bottom_border, (self.tile_width, self.tile_width * self.bottom_border.get_height() / self.bottom_border.get_width()))
        self.bottom_border.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_ADD)

        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height), depth=32)
        pygame.display.set_caption('Hex')
        pygame.display.set_icon(self.token_image)

        self.pause_screen = pygame.image.load('Sprites\\pause_screen.png')

        self.fps_clock = pygame.time.Clock() 

    def draw_grid(self):
        """
        Draw an empty grid
        """
        self.display_surface.fill(WHITE)
        # Draw hex tiles
        for i in range(self.board_size):
            self.display_surface.blit(self.left_border, self.click_board[i][0].copy().move(-0.6 * self.tile_width, 0.3 * self.tile_width))
            self.display_surface.blit(self.right_border, self.click_board[i][self.board_size - 1].copy().move(0.6 * self.tile_width, -0.3 * self.tile_width))
            self.display_surface.blit(self.top_border, self.click_board[0][i].copy().move(-0.2 * self.tile_width, -0.65 * self.tile_width))
            self.display_surface.blit(self.bottom_border, self.click_board[self.board_size - 1][i].copy().move(0.2 * self.tile_width, 0.65 * self.tile_width))
            for j in range(self.board_size):
                self.display_surface.blit(self.hex_image, self.click_board[i][j])
        pygame.display.update()
    
    def draw_move(self, player_move: tuple[int], player_token: int):
        row, column = player_move
        if player_token == PLAYER_1_TOKEN:
            self.display_surface.blit(self.token_image_player_1, self.click_board[row][column])
        else:
            self.display_surface.blit(self.token_image_player_2, self.click_board[row][column])
        self.fps_clock.tick(FPS)
        pygame.display.update()

    def animate_win_path(self, path: list[tuple[int]], player_token: int):
        winner_token_image = self.token_image_player_1 if player_token == PLAYER_1_TOKEN else self.token_image_player_2
        for _ in range(4): # blink 4 times
            for (row, column) in path:
                self.display_surface.blit(self.token_image, self.click_board[row][column])
            self.fps_clock.tick(FPS)
            pygame.display.update()

            for (row, column) in path:
                self.display_surface.blit(winner_token_image, self.click_board[row][column])
            self.fps_clock.tick(FPS)
            pygame.display.update()

    def draw_board(self, board: list[list[int]]):
        self.draw_grid()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == PLAYER_1_TOKEN:
                    self.display_surface.blit(self.token_image_player_1, self.click_board[i][j])
                elif board[i][j] == PLAYER_2_TOKEN:
                    self.display_surface.blit(self.token_image_player_2, self.click_board[i][j])
        pygame.display.update()


    def draw_paused_game(self):
        self.display_surface.blit(self.pause_screen, (0, 0))
        pygame.display.update()
    
