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

class MancalaNode:
    def __init__(self, player_id: int, board: [int], parent = None, pit = -1 ):
        self.player_id = player_id
        self.board = board
        self.parent = parent 
        self.pit = pit
        self.children = [] 
        self.wins = 0 
        self.pulls = 0
    
    def is_leaf(self):
        return self.children == []
    
    def add_child(self, player_id: int, board: [int], pit: int):
        self.children.append(MancalaNode(self, 1 - player_id, board, pit))

    def find_best_ucb(self):
        return max(self.children, key = lambda child: calculate_upper_confidence_bound(child.wins, child.pulls, 2, self.pulls))

    def record_play(self, did_score: bool, board: [int] ):
        current_store_value = board[13]

        if board[13] == current_store_value +1:
            self.wins += 1
        if self.parent:
            self.parent.record_play(not did_score)

def calculate_upper_confidence_bound(wins: int, pulls: int, c: float, t: float) -> float:
    if pulls == 0:
        return float ('inf')
    return wins/pulls + c * math.sqrt(math.log(t) / pulls)

    #game_state = mancala.get_score(mancala_node_player.player_id, mancala_node_board.board )
    #return game_state, mancala.game_is_over(board)

def monte_carlo_complicated_player(player_id : int, board : [int]) -> int:
    root = MancalaNode(1 - player_id, board)

    num_simulations = 10 
    for _ in range (num_simulations):
        curr_node = root
        while not curr_node.is_leaf():
            curr_node = curr_node.find_best_ucb()
            print("Current Node",curr_node)
        score, is_finished = score_board(curr_node.player_id, curr_node.board) 
        print("Player_ID : ",curr_node.player_id, "Current Board",curr_node.board)
        if not is_finished:
            playable_pits = get_full_pits(curr_node.board, curr_node.player_id)
            possible_boards = list(map(lambda x: generate_next_board(1 - curr_node.player_id, curr_node.board, x), playable_pits))
            for board1, pit in zip(possible_boards, playable_pits):
                curr_node.add_child(player_id, board1, pit)
        curr_node = random.choice(curr_node.children)
    did_score = playout(curr_node.player_id, curr_node.board)
    curr_node.record_play(did_score)

    winning_child = max(root.children, key = lambda child: child.wins / child.pulls)
    return winning_child.pit


def competition_player (player_id : int, board : [int]) -> int:
    return monte_carlo_player(player_id, board)

mancala.run_simulations([random_player, monte_carlo_complicated_player], 100, display_boards = False, print_statistics = True)


''' def score_board_Monte_Carlo(player_id: int, board: [int]) -> (int, bool):
    mancala_node_board = MancalaNode(player_id,board)
    mancala_node_player = MancalaNode(player_id,board)
    
    def generate_next_board_monte_carlo(player_id: int, board: [int], pit_to_play: int) -> [int]:
    boards = []
    for i in range(5):
       next_board = mancala.sow(pit_to_play, player_id, board)
       boards.append[next_board]

    return boards
'''
