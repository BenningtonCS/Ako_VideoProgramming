import tictactoe
import random
# player functions take 2 parameters 
# player_id which is 0 (X) and 1 (O)
# curr_board which is list of 9 strings ex: [" ", "O", "X"...]
# the function returns the index of the slot the player will play in 

def get_open_spots (curr_board: [int]) -> int:
    return [x for x in range(len(curr_board)) if curr_board[x] == " "]
# to make AI that randomly fills in the spots with X or O 
# function random_player takes in player_id, which is integer, and curr_board which is an index, and returns an int
def random_player (player_id: int, curr_board: [int]) -> int:  
    # first, find all the open slots 
    open_spots = get_open_spots(curr_board)
    # The len() function returns the number of items in an object.
    # When the object is a string, the len() function returns the number of characters in the string.

    # then choose a random one to play in 
    return random.choice(open_spots)

def always_pick_winner (player_id: int, curr_board: [int]) -> int:
    # if you can play the winning move, always do so 
    # otherwise, play randomly 
    open_spots = get_open_spots(curr_board)
    # for each of these open spaces, try to make the move, and look at the satet of the board 
    for spot in open_spots:
        new_board = curr_board.copy()
        new_board[spot] = tictactoe.player_strings[player_id]
        state = tictactoe.game_state(new_board)
        if state == player_id: 
            return spot

    return random.choice(open_spots)

def score_board(player_id: int, board: [int]) -> (int, bool):
    game_state = tictactoe.game_state(board)
    opponent_id = (player_id + 1) % 2
    if game_state == player_id: 
        return 1, True
    elif game_state == opponent_id: 
        return -1, True
    elif game_state == tictactoe.DRAW:
        return 0, True 
    else: 
        return 0, False

def generate_possible_boards(player_id: int, curr_board: [int], spot_to_play: int) -> [int]:
    new_board = curr_board.copy()
    new_board[spot_to_play] = tictactoe.player_strings[player_id]
    return new_board

def minimax(player_id : int, curr_board: [int], depth: int, should_maximize: bool, alpha = float('-inf'), beta = float('inf')) -> int:
    # find the score of the board at this moment 
    curr_score, is_done = score_board(player_id, curr_board)
    # if we're at the bottom (depth == 0) or if the game is finished, return score 
    if depth == 0 or is_done:
        return curr_score * (depth + 1)
    
    # if the game is not finished or not at the bottom of the tree:
    # find all the open spots
    open_spots = get_open_spots(curr_board)
    # if we're maximizing, we play from player_id's turn 
    if should_maximize:
        max_score = float ('-inf')
        # get all possible boards after player_id's move
        for spot in open_spots:
            board = generate_possible_boards(player_id, curr_board, spot)
            # score them (recursively)
            score = minimax(player_id, board, depth - 1, False, alpha, beta)
            max_score = max(max_score, score)
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        # choose the max score and return it 
        return max_score
    # otherwise (if we are minimazing)
    else:
        min_score = float ('inf')
        # get all possible turns after opponent's turn 
        for spot in open_spots:
            board = generate_possible_boards((player_id + 1) % 2, curr_board, spot)
            # score them (recursively)
            score = minimax(player_id, board, depth - 1, True, alpha, beta)
            min_score = min(min_score, score)
            beta = min(beta, min_score)
        # choose the minimum score and return it 
        return min_score

def minimax_player(player_id: int, curr_board: [int]) -> int:
    # find all the open spots
    open_spots = get_open_spots(curr_board) 
    # generate all the possible game boards 
    possible_boards = list(map(lambda x: generate_possible_boards(player_id, curr_board, x), open_spots))
    # find the scores for each of those game boards (recursively)
    scored_boards = list(map(lambda x: minimax(player_id, x, 9, False), possible_boards))

    # pick the spot that produced max score 
    best_score = max(list(scored_boards))
    best_moves = [x for x, score in zip(open_spots, scored_boards) if score == best_score]
    return random.choice(best_moves)

#tictactoe.play_game([minimax_player, random_player], should_display=True, start_player=0)
'''
print (score_board(0, ["X", "X", "X",
                       "O", " ", " ",
                       "O", "O", " "]))

print (score_board(0, ["X", "O", "X",
                       "X", "O", "O",
                       "O", "X", "X"]))

print (score_board(0, ["O", "X", "X",
                       "O", "X", " ",
                       "O", "O", " "]))
'''


x_wins, o_wins, draws = tictactoe.run_simulations([minimax_player, always_pick_winner], 3, x_always_starts=False)
print ("X won " + str(x_wins) + " times")
print ("O won " + str(o_wins) + " times")
print ("It was a draw " + str(draws) + " times")
