from game import *


if __name__ == '__main__':
    pygame.init()
    game = Game(board_size=6, player_1=Human_Player(1), player_2=AI_Random_Player(2))
    game.start()