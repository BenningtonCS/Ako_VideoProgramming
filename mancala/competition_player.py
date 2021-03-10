import mancala
import random
import math

def random_player(player_id : int, board : [int]) -> int:
    if (player_id == 0):
        return random.randint(0, 5)
    return random.randint(7, 12)

def game_state(player_id: id, board: [int]) -> int:
    opponent_id = (player_id + 1) % 2
    if mancala.game_is_over(board) and mancala.who_won(board) == player_id:
        return 1
    elif mancala.game_is_over(board) and mancala.who_won(board) == opponent_id:
        return -1
    elif mancala.game_is_over(board) and mancala.who_won(board) == 2:
        return 2
    else:
        return 0

def score_board(player_id: int, board: [int]) -> (int, bool):
    game_state = mancala.get_score(player_id, board)
    return game_state, mancala.game_is_over(board)
    # This function is from Andrew's code!

def generate_next_board(player_id: int, board: [int], pit_to_play: int) -> [int]:
    next_player, next_board = mancala.sow(pit_to_play, player_id, board)
    return next_board

def get_full_pits (board: [int], player_id: int) -> int:
    if player_id == 0:
        result = []
        for i in range(0, 6):
            if board[i] != 0:
                result.append(i)
        
        return result
    else:
        result = []
        for i in range(7, 13):
            if board[i] != 0:
                result.append(i)
        
        return result

def playout(player_id: int, board : [int]) -> bool:
    score, is_finished = score_board(player_id, board)
    if is_finished:
        return score == 1
    next_board = board
    next_player = 1 - player_id 
    while not is_finished:
        pit_to_play = random_player(next_player, next_board)
        next_board = generate_next_board (next_player, next_board, pit_to_play)
        score, is_finished = score_board(player_id, next_board)
        next_player = 1 - next_player
    return score ==1

def monte_carlo_player(player_id : int, board : [int]) -> int:
    playable_pits = get_full_pits(board, player_id)
    possible_boards = list(map(lambda x: generate_next_board(player_id, board, x), playable_pits))
    num_simulations = 10
    wins=[sum ([1 for _ in range(num_simulations) if playout(player_id, board1)]) for board1 in possible_boards]
    index = max (range(len(playable_pits)), key = lambda i: wins [i])
    return playable_pits[-1]
    # worked on this one with Delaine! 

def competition_player (player_id : int, board : [int]) -> int:
    return monte_carlo_player(player_id, board)

mancala.run_simulations([random_player, competition_player], 100, display_boards = False, print_statistics = True)
