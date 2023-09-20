import pygame, sys, random
from pygame.locals import *


WINDOW_WIDTH = 800 # Default: 800
WINDOW_HEIGHT = 600 # Default: 600

BOARD_SIZE = 11 # Default: 11
BOARD_WIDTH = 512 # Default: 512

BOARD: tuple[tuple[pygame.Rect]]

BOARD_WIDTH_IN_TILES = (3 * BOARD_SIZE - 1) / 2
TILE_WIDTH = int(BOARD_WIDTH / BOARD_WIDTH_IN_TILES) 
BOARD_HEIGHT = BOARD_SIZE * TILE_WIDTH

# COLORS            #R   #G   #B
BLACK           = (  0,   0,   0)
WHITE           = (255, 255, 255)
PASTEL_BLUE     = ( 61, 232, 239)
DARK_PINK       = (195,  79, 244)
LIGHT_ORANGE    = (255, 181,  31) 

FPS = 4

# Board should fit nicely in window
assert BOARD_WIDTH < WINDOW_WIDTH - 30
assert BOARD_HEIGHT < WINDOW_HEIGHT - 30

HEX_IMAGE = pygame.image.load('Sprites\hex_border.png')
HEX_IMAGE = pygame.transform.smoothscale(HEX_IMAGE, (TILE_WIDTH, HEX_IMAGE.get_height() * TILE_WIDTH / HEX_IMAGE.get_width()))
HEX_IMAGE.fill(PASTEL_BLUE, special_flags=BLEND_RGB_ADD)

TOKEN_IMAGE = pygame.image.load('Sprites\playing_token.png')
TOKEN_IMAGE = pygame.transform.smoothscale(TOKEN_IMAGE, (TILE_WIDTH, TILE_WIDTH))

TOKEN_IMAGE_1 = TOKEN_IMAGE.copy()
TOKEN_IMAGE_1.fill(DARK_PINK, special_flags=BLEND_RGB_MULT)

TOKEN_IMAGE_2 = TOKEN_IMAGE.copy()
TOKEN_IMAGE_2.fill(LIGHT_ORANGE, special_flags=BLEND_RGB_MULT)

def main():
    global DISPLAY_SURFACE, BOARD

    pygame.init()

    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    DISPLAY_SURFACE.fill(BLACK)
    pygame.display.set_caption('Hex -- Version 1.0')
    pygame.display.set_icon(TOKEN_IMAGE)

    BOARD = create_board()
    draw_empty_board(DISPLAY_SURFACE)
    # DISPLAY_SURFACE.blit(pygame.transform.smoothscale(GAME_BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0,0))
    while True: # main game loop

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
            
            pygame.display.update()


def create_board() -> tuple[tuple[pygame.Rect]]:
    initial_board = list()

    for i in range(BOARD_SIZE):
        initial_board.append(list())
        for j in range(BOARD_SIZE):
            initial_board[i].append(pygame.Rect((
                (WINDOW_WIDTH - BOARD_WIDTH) / 2 + j * TILE_WIDTH + i * TILE_WIDTH / 2,
                (WINDOW_HEIGHT - BOARD_HEIGHT) / 2 + i * TILE_WIDTH
            ), (TILE_WIDTH, TILE_WIDTH)))
        
    return tuple([tuple(row) for row in initial_board])


def draw_empty_board(DISPLAY_SURFACE: pygame.Surface):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            DISPLAY_SURFACE.blit(HEX_IMAGE, BOARD[i][j])
            # pygame.draw.rect(DISPLAY_SURFACE, PASTEL_BLUE, BOARD[i][j], width=1)


def make_move(row_position: int, column_position: int):
    DISPLAY_SURFACE.blit(TOKEN_IMAGE_1 if random.randint(0, 1) == 0 else TOKEN_IMAGE_2, BOARD[row_position][column_position])
    # pygame.draw.rect(DISPLAY_SURFACE, MAGENTA_PINK if random.randint(0, 1) == 0 else LIGHT_ORANGE, BOARD[row_position][column_position])


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
