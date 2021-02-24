import mancala
import random


# random_player takes a player id and current board state and returns the id of the pit to play
# player_id is 0 or 1
# board is a list of ints representing the number of seeds in each of the 14 pits in the following layout:
#   12 11 10  9  8  7
# 13                  6
#    0  1  2  3  4  5
# player 0 can only play from pits 0 to 5
# player 1 can only play from pits 7 to 12

def random_player(player_id : int, board : [int]) -> int:
    if (player_id == 0):
        return random.randint(0, 5)
    return random.randint(7, 12)

def next_winning_move(player_id : int, board : [int]) -> int:
    if (player_id == 0):
        for pit_id in range(0, 6):
            new_board = board.copy()
            next_player, next_board = mancala.sow(pit_id, player_id, new_board)
            if mancala.game_is_over(next_board) and mancala.who_won(next_board) == player_id:
                return pit_id
        return random.randint(0, 5)

    for pit_id in range(7, 13):
        new_board = board.copy()
        next_player, next_board = mancala.sow(pit_id, player_id, new_board)
        if mancala.game_is_over(next_board) and mancala.who_won(next_board) == player_id:
            return pit_id
    return random.randint(7, 12)


mancala.run_simulations([random_player, next_winning_move], 1000, display_boards=False, print_statistics = True)
