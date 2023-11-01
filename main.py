from game import *


if __name__ == '__main__':
    pygame.init()
    game = Game(board_size=5, player_1=AI_Minmax_Player(1), player_2=AI_Minmax_Player(2))
    print(game.start_simulation(50))
