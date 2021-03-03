import random

player_strings = ["X", "O", " "]
possible_win_combinations = [
	[0, 1, 2],
	[3, 4, 5],
	[6, 7, 8],
	[0, 3, 6],
	[1, 4, 7],
	[2, 5, 8],
	[0, 4, 8],
	[2, 4, 6]
]

X_WIN = 0
O_WIN = 1
DRAW = 2
CONTINUE = 3

def display_board(board):
	print()
	print(" " + board[0] + " | " + board[1] + " | " + board[2])
	print(" ----------")
	print(" " + board[3] + " | " + board[4] + " | " + board[5])
	print(" ----------")
	print(" " + board[6] + " | " + board[7] + " | " + board[8])
	print()

def set_up():
	return [" "] * 9

def game_state(board):
	for possible_win in possible_win_combinations:
		if board[possible_win[0]] != " " and board[possible_win[0]] == board[possible_win[1]] and board[possible_win[0]] == board[possible_win[2]]:
			if board[possible_win[0]] == "X":
				return X_WIN
			else:
				return O_WIN

	empty_spots = list(filter(lambda x: x == " ", board))
	if len(empty_spots) == 0:
		return DRAW
	return CONTINUE

def play_turn(index, player_id, board):
	if board[index] != " ":
		return board

	new_board = board.copy()
	new_board[index] = player_strings[player_id]
	return new_board

def play_game(player_functions, should_display=False, start_player=0):
	board = set_up()

	player_id = start_player

	if should_display == True:
		print("First player: " + player_strings[player_id])
		display_board(board)

	curr_game_state = game_state(board)
	while curr_game_state == CONTINUE:
		if should_display == True:
			print(player_strings[player_id] + "'s turn")

		spot_to_play = player_functions[player_id](player_id, board)
		board = play_turn(spot_to_play, player_id, board)

		if should_display == True:
			display_board(board)

		player_id = (player_id + 1) % 2
		curr_game_state = game_state(board)

	if should_display == True:
		if curr_game_state == DRAW:
			print("Draw")
		else:
			print(player_strings[curr_game_state] + " won!")

	return curr_game_state

def get_number(prompt):
	possible_int = input(prompt)
	try:
		return int(possible_int)
	except ValueError:
		print("Invalid input")
		return get_number(prompt)

def human_player(player_id, board):
	row = get_number("Which row? ")
	column = get_number("Which column? ")
	return row * 3 + column

def run_simulations(player_functions, num_games, x_always_starts=False):
	outcomes = [0] * 3

	for i in range(0, num_games):
		start_player = i%2
		if x_always_starts:
			start_player = 0
		outcome = play_game(player_functions, should_display=False, start_player=start_player)
		outcomes[outcome] += 1

	return outcomes[0], outcomes[1], outcomes[2]
