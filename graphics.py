import pygame, random
from board import PLAYER_1_TOKEN, PLAYER_2_TOKEN
from pygame.locals import *


# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (0, 0, 0)
PLAYER_1_COLOR = (61, 232, 239)
PLAYER_2_COLOR = (255, 181,  31)
HOVER_TEXT_COLOR = (39, 156, 170)

# PURPLE AND GREEN
# PLAYER_1_COLOR = (168, 134, 250)
# PLAYER_2_COLOR = (34, 250, 114)
# HOVER_TEXT_COLOR = (61, 232, 239)

# ORANGE AND BLUE
# PLAYER_1_COLOR = (61, 232, 239)
# PLAYER_2_COLOR = (255, 181,  31)
# HOVER_TEXT_COLOR = (255, 215, 0)


class Graphics(object):
    """
    Class to display objects to game window
    """

    window_width: int 
    window_height: int 

    board_width: int
    board_height: int
    board_width_in_tiles: int
    tile_width: int

    board_size: int
    click_board: tuple[tuple[pygame.Rect, ...], ...]
    '''Contains collision area of hex tiles clickable for the player'''

    display_surface: pygame.Surface
    '''Contains elements to be displayed on the window'''

    hex_image: pygame.Surface
    token_image: pygame.Surface
    token_image_player_1: pygame.Surface
    token_image_player_2: pygame.Surface
    pause_screen: pygame.Surface

    fps: int

    def __init__(self, board_size: int):
        """
        Initialize the graphics for the game
        """
        self.window_width = 800 # Default: 800
        self.window_height = 600 # Default: 600

        self.board_size = board_size

        self.board_width = 512 # Default: 512
        self.board_width_in_tiles = int((3 * self.board_size - 1) / 2)
        self.tile_width = int(self.board_width / self.board_width_in_tiles) 
        self.board_height = self.board_size * self.tile_width

        self.click_board = tuple([tuple([pygame.Rect((
                    (self.window_width - self.board_width) / 2 + j * self.tile_width + i * self.tile_width / 2,
                    (self.window_height - self.board_height) / 2 + i * self.tile_width
                ), (self.tile_width, self.tile_width)) for j in range(self.board_size)]) for i in range(self.board_size)])
        
        # Load, scale and color images
        self.hex_image = pygame.image.load('Sprites\\hex_border.png')
        self.hex_image = pygame.transform.smoothscale(self.hex_image, (self.tile_width, self.tile_width * self.hex_image.get_height() / self.hex_image.get_width()))
        self.hex_image.fill(BOARD_COLOR, special_flags=BLEND_RGB_ADD)
        self.token_image = pygame.image.load('Sprites\\playing_token.png')
        self.token_image = pygame.transform.smoothscale(self.token_image, (self.tile_width, self.tile_width))
        self.token_image_player_1 = self.token_image.copy()
        self.token_image_player_1.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_MULT)
        self.token_image_player_2 = self.token_image.copy()
        self.token_image_player_2.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_MULT)
        self.left_border = pygame.image.load('Sprites\\left_border.png')
        self.left_border = pygame.transform.smoothscale(self.left_border, (2.5 * self.tile_width, 2.5 * self.tile_width * self.left_border.get_height() / self.left_border.get_width()))
        self.left_border.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_MULT)
        self.right_border = pygame.image.load('Sprites\\right_border.png')
        self.right_border = pygame.transform.smoothscale(self.right_border, (2.5 * self.tile_width, 2.5 * self.tile_width * self.right_border.get_height() / self.right_border.get_width()))
        self.right_border.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_MULT)
        self.top_border = pygame.image.load('Sprites\\top_border.png')
        self.top_border = pygame.transform.smoothscale(self.top_border, (self.tile_width, self.tile_width * self.top_border.get_height() / self.top_border.get_width()))
        self.top_border.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_MULT)
        self.bottom_border = pygame.image.load('Sprites\\bottom_border.png')
        self.bottom_border = pygame.transform.smoothscale(self.bottom_border, (self.tile_width, self.tile_width * self.bottom_border.get_height() / self.bottom_border.get_width()))
        self.bottom_border.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_MULT)
        self.bottom_right_border = pygame.image.load('Sprites\\bottom_right_border.png')
        self.bottom_right_border = pygame.transform.smoothscale(self.bottom_right_border, (2.5 * self.tile_width, 2.5 * self.tile_width * self.bottom_right_border.get_height() / self.bottom_right_border.get_width()))
        self.bottom_right_border.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_MULT)
        self.bottom_right_border_2 = pygame.image.load('Sprites\\bottom_right_border_2.png')
        self.bottom_right_border_2 = pygame.transform.smoothscale(self.bottom_right_border_2, (2.5 * self.tile_width, 2.5 * self.tile_width * self.bottom_right_border_2.get_height() / self.bottom_right_border_2.get_width()))
        self.bottom_right_border_2.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_MULT)
        self.top_left_border = pygame.image.load('Sprites\\top_left_border.png')
        self.top_left_border = pygame.transform.smoothscale(self.top_left_border, (2.5 * self.tile_width, 2.5 * self.tile_width * self.top_left_border.get_height() / self.top_left_border.get_width()))
        self.top_left_border.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_MULT)
        self.top_left_border_2 = pygame.image.load('Sprites\\top_left_border_2.png')
        self.top_left_border_2 = pygame.transform.smoothscale(self.top_left_border_2, (2.5 * self.tile_width, 2.5 * self.tile_width * self.top_left_border_2.get_height() / self.top_left_border_2.get_width()))
        self.top_left_border_2.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_MULT)
        self.bottom_left_border = pygame.image.load('Sprites\\bottom_left_border.png')
        self.bottom_left_border = pygame.transform.smoothscale(self.bottom_left_border, (2.5 * self.tile_width, 2.5 * self.tile_width * self.bottom_left_border.get_height() / self.bottom_left_border.get_width()))
        self.bottom_left_border.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_MULT)
        self.bottom_left_border_2 = pygame.image.load('Sprites\\bottom_left_border_2.png')
        self.bottom_left_border_2 = pygame.transform.smoothscale(self.bottom_left_border_2, (2.5 * self.tile_width, 2.5 * self.tile_width * self.bottom_left_border_2.get_height() / self.bottom_left_border_2.get_width()))
        self.bottom_left_border_2.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_MULT)
        self.top_right_border = pygame.image.load('Sprites\\top_right_border.png')
        self.top_right_border = pygame.transform.smoothscale(self.top_right_border, (2.5 * self.tile_width, 2.5 * self.tile_width * self.top_right_border.get_height() / self.top_right_border.get_width()))
        self.top_right_border.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_MULT)
        self.top_right_border_2 = pygame.image.load('Sprites\\top_right_border_2.png')
        self.top_right_border_2 = pygame.transform.smoothscale(self.top_right_border_2, (2.5 * self.tile_width, 2.5 * self.tile_width * self.top_right_border_2.get_height() / self.top_right_border_2.get_width()))
        self.top_right_border_2.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_MULT)
        self.reset_text = pygame.image.load('Sprites\\reset_text.png')
        self.settings_text = pygame.image.load('Sprites\\settings_text.png')

        self.hover_reset_text = self.reset_text.copy()
        self.hover_reset_text.fill(HOVER_TEXT_COLOR, special_flags=BLEND_RGB_ADD)
        self.reset_text_box = pygame.Rect(40, 15, 132, 62)
        self.hover_settings_text = self.settings_text.copy()
        self.hover_settings_text.fill(HOVER_TEXT_COLOR, special_flags=BLEND_RGB_ADD)
        self.settings_text_box = pygame.Rect(580, 15, 184, 62)

        self.selection_arrow = pygame.image.load('Sprites\\selection_arrow.png')
        self.selection_arrow_2 = pygame.image.load('Sprites\\selection_arrow_2.png')
        self.player_1_human_box = pygame.Rect(82, 208, 129, 43)
        self.player_1_ai_box = pygame.Rect(163, 310, 45, 43)
        self.player_2_human_box = pygame.Rect(590, 208, 129, 43)
        self.player_2_ai_box = pygame.Rect(590, 310, 45, 43)
        self.go_back_box = pygame.Rect(42, 530, 153, 45) 
        self.save_changes_box = pygame.Rect(494, 530, 257, 53)
        self.player_1_turn_text = pygame.image.load('Sprites\\player_1_turn_text.png')
        self.player_1_turn_text.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_ADD)
        self.player_2_turn_text = pygame.image.load('Sprites\\player_2_turn_text.png')
        self.player_2_turn_text.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_ADD)
        self.player_1_wins_text = pygame.image.load('Sprites\\player_1_wins_text.png')
        self.player_1_wins_text.fill(PLAYER_1_COLOR, special_flags=BLEND_RGB_ADD)
        self.player_2_wins_text = pygame.image.load('Sprites\\player_2_wins_text.png')
        self.player_2_wins_text.fill(PLAYER_2_COLOR, special_flags=BLEND_RGB_ADD)
        self.player_turn_box = pygame.Rect(0, 680, self.player_1_turn_text.get_width(), self.player_1_turn_text.get_height())

        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height), depth=32)
        pygame.display.set_caption('Hex')
        pygame.display.set_icon(self.token_image)

        self.pause_screen = pygame.image.load('Sprites\\pause_screen.png')

        self.fps_clock = pygame.time.Clock() 
        self.fps = 5

    def draw_grid(self):
        """
        Draw an empty grid
        """
        self.display_surface.fill(WHITE)

        # Draw text
        self.display_surface.blit(self.reset_text, (0, 0))
        self.display_surface.blit(self.settings_text, (self.window_width - self.settings_text.get_width(), 0))
        self.display_surface.blit(self.player_1_turn_text, (0, 535))

        # Draw hex tiles not on border
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.display_surface.blit(self.hex_image, self.click_board[i][j])
        
        # Draw hex tiles on border but not on corner
        for i in range(1, self.board_size-1):
            self.display_surface.blit(self.left_border, self.click_board[i][0].copy().move(-1.5 * self.tile_width, 0))
            self.display_surface.blit(self.right_border, self.click_board[i][self.board_size - 1])
            self.display_surface.blit(self.top_border, self.click_board[0][i].copy().move(0, -0.75 * self.tile_width))
            self.display_surface.blit(self.bottom_border, self.click_board[self.board_size - 1][i])
        
        # Draw corners
        self.display_surface.blit(self.bottom_right_border, self.click_board[self.board_size - 1][self.board_size - 1])
        self.display_surface.blit(self.bottom_right_border_2, self.click_board[self.board_size - 1][self.board_size - 1])
        self.display_surface.blit(self.top_left_border, self.click_board[0][0].copy().move(-1.5 * self.tile_width, -0.75 * self.tile_width))
        self.display_surface.blit(self.top_left_border_2, self.click_board[0][0].copy().move(-1.5 * self.tile_width, -0.75 * self.tile_width))
        self.display_surface.blit(self.bottom_left_border, self.click_board[self.board_size - 1][0].copy().move(-1.5 * self.tile_width, 0))
        self.display_surface.blit(self.bottom_left_border_2, self.click_board[self.board_size - 1][0].copy().move(-1.5 * self.tile_width, 0))
        self.display_surface.blit(self.top_right_border, self.click_board[0][self.board_size - 1].copy().move(0, -0.75 * self.tile_width))
        self.display_surface.blit(self.top_right_border_2, self.click_board[0][self.board_size - 1].copy().move(0, -0.75 * self.tile_width))

        pygame.display.update()
    
    def draw_move(self, player_move: tuple[int, int], player_token: int):
        """
        Draw player's token on the board
        """
        row, column = player_move
        if player_token == PLAYER_1_TOKEN:
            self.display_surface.blit(self.token_image_player_1, self.click_board[row][column])
        else:
            self.display_surface.blit(self.token_image_player_2, self.click_board[row][column])
        self.fps_clock.tick(self.fps)
        pygame.display.update()
    
    def draw_turn(self, player_turn: int):
        """
        Display current player's turn
        """
        pygame.draw.rect(self.display_surface, WHITE, (0, 535, self.player_1_turn_text.get_width(), self.player_1_turn_text.get_height()))
        if player_turn == 0:
            self.display_surface.blit(self.player_1_turn_text, (0, 535))
        else:
            self.display_surface.blit(self.player_2_turn_text, (0, 535))
        pygame.display.update()

    def animate_win_path(self, path: list[tuple[int, int]], player_token: int):
        """
        Display flash animation for winning path of player's tokens
        """
        winner_token_image = self.token_image_player_1 if player_token == PLAYER_1_TOKEN else self.token_image_player_2
        pygame.draw.rect(self.display_surface, WHITE, (0, 535, self.player_1_turn_text.get_width(), self.player_1_turn_text.get_height()))
        if player_token == PLAYER_1_TOKEN:
            self.display_surface.blit(self.player_1_wins_text, (0, 535))
        else:
            self.display_surface.blit(self.player_2_wins_text, (0, 535))
        for _ in range(4):  # blink 4 times
            for (row, column) in path:
                self.display_surface.blit(self.token_image, self.click_board[row][column])
            self.fps_clock.tick(self.fps)
            pygame.display.update()

            for (row, column) in path:
                self.display_surface.blit(winner_token_image, self.click_board[row][column])
            self.fps_clock.tick(self.fps)
            pygame.display.update()

    def draw_board(self, board: list[list[int, int]]):
        """
        Draw board with tokens
        """
        self.draw_grid()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == PLAYER_1_TOKEN:
                    self.display_surface.blit(self.token_image_player_1, self.click_board[i][j])
                elif board[i][j] == PLAYER_2_TOKEN:
                    self.display_surface.blit(self.token_image_player_2, self.click_board[i][j])
        pygame.display.update()

    def draw_paused_game(self, player_1_human_flag: bool, player_2_human_flag: bool):
        """
        Draw settings menu
        """
        self.display_surface.blit(self.pause_screen, (0, 0))
        if player_1_human_flag is True:
            self.display_surface.blit(self.selection_arrow, (240, 214))
        else:
            self.display_surface.blit(self.selection_arrow, (240, 312))
        if player_2_human_flag is True:
            self.display_surface.blit(self.selection_arrow_2, (518, 214))
        else:
            self.display_surface.blit(self.selection_arrow_2, (518, 312))
        pygame.display.update()

    def animate_reset_text(self):
        """
        Display hover animation for reset text
        """
        hover_x, hover_y = pygame.mouse.get_pos()
        pygame.draw.rect(self.display_surface, WHITE, (0, 0, self.reset_text.get_width(), self.reset_text.get_height()))
        if self.reset_text_box.collidepoint(hover_x, hover_y) is True:
            self.display_surface.blit(self.hover_reset_text, (0, 0))
        else:
            self.display_surface.blit(self.reset_text, (0, 0))
        pygame.display.update()

    def animate_settings_text(self):
        """
        Display hover animation for settings text
        """
        hover_x, hover_y = pygame.mouse.get_pos()
        pygame.draw.rect(self.display_surface, WHITE, (self.window_width - self.settings_text.get_width(), 0, self.settings_text.get_width(), self.settings_text.get_height()))
        if self.settings_text_box.collidepoint(hover_x, hover_y) is True:
            self.display_surface.blit(self.hover_settings_text, (self.window_width - self.settings_text.get_width(), 0))
        else:
            self.display_surface.blit(self.settings_text, (self.window_width - self.settings_text.get_width(), 0))
        pygame.display.update()
