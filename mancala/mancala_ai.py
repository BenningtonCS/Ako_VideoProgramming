import mancala
import random
import math

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

def expert_player(player_id : int, board : [int]) -> int:
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

def minimax(player_id : int, board: [int], depth: int, should_maximize: bool, alpha = float('-inf'), beta = float('inf')) -> int:
    curr_score, is_done = score_board(player_id, board)
    if depth == 0 or is_done:
        return curr_score * (depth + 1)
    playable_pits = get_full_pits(board, player_id)
    if should_maximize:
        max_score = float ('-inf')
        for pit in playable_pits:
            board1 = generate_next_board(player_id, board, pit)
            score = minimax(player_id, board1, depth - 1, False, alpha, beta)
            max_score = max(max_score, score)
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        return max_score
    else:
        min_score = float ('inf')
        for pit in playable_pits:
            board1 = generate_next_board((player_id + 1) % 2, board, pit)
            score = minimax(player_id, board1, depth - 1, True, alpha, beta)
            min_score = min(min_score, score)
            beta = min(beta, min_score)
        return min_score

def minimax_player(player_id : int, board : [int]) -> int:
    playable_pits = get_full_pits(board, player_id)
    possible_boards = list(map(lambda x: generate_next_board(player_id, board, x), playable_pits))
    # print(possible_boards)
    scored_boards = list(map(lambda x: minimax(player_id, x, 3, False), possible_boards))
    best_score = max(list(scored_boards))
    best_moves = [x for x, score in zip(playable_pits, scored_boards) if score == best_score]
    return random.choice(best_moves)

mancala.run_simulations([minimax_player, random_player], 100, display_boards = False, print_statistics = True)
