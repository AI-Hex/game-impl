from game import *


if __name__ == '__main__':
    pygame.init()
    game = Game(board_size=4, player_1=AI_Minmax_Player(1), player_2=Human_Player(2))
    game.start()