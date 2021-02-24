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

# tictactoe.play_game([tictactoe.human_player, random_player], should_display=True, start_player=0)

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

def score_board(player_id: int, board: [int]) -> int:
    game_state = tictactoe.game_state(board)
    opponent_id = (player_id + 1) % 2
    if game_state == player_id: 
        return 1 
    elif game_state == opponent_id: 
        return -1 
    else:
        return 0 

def minimax(player_id : int, curr_board: [int], depth: int, should_maximize: bool) -> int:
    # find the score of the board at this moment 
    # if we're at the bottom (depth == 0) or if the game is finished, return score 
    # if the game is not finished or not at the bottom of the tree:
    # find all the open spots
    # if we're maximizing, we play from player_id's turn 
        # get all possible boards after player_id's move
        # score them (recursively)
        # choose the max score and return it 
    # otherwise (if we are minimazing) 
        # get all possible turns after opponent's turn 
        # score them (recursively)
        # choose the minimum score and return it 
    return 0 

def minimax_player(player_id: int, curr_board: [int]) -> int:
    # find all the open spots 
    # generate all the possible game boards 
    # find the scores for each of those game boards (recursively)
    # pick the spot that produced max score 
    return 0

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
x_wins, o_wins, draws = tictactoe.run_simulations([always_pick_winner, always_pick_winner], 1000, x_always_starts=False)
print ("X won " + str(x_wins) + " times")
print ("O won " + str(o_wins) + " times")
print ("It was a draw " + str(draws) + " times")
'''