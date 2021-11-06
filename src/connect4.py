import random
import math

from board import Board
from renderer import Renderer
from minimax import Minimax

# Setup game

game_over = False

ROW_COUNT = 6
COLUMN_COUNT = 7
board = Board(ROW_COUNT, COLUMN_COUNT)
board.print()

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
PLAYER = 0
AI = 1
renderer = Renderer(ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE)
renderer.draw(board.get_state())

turn = random.randint(PLAYER, AI)

# Define RL algo

algo = Minimax()

# Gameplay loop

while not game_over:
	if turn == PLAYER:
		# Get frame and events from pygame graphics renderer
		clicked_col = renderer.handle_events()
		if clicked_col:
			if board.is_valid_location(clicked_col):
				row = board.get_next_open_row(clicked_col)
				board.drop_piece(row, clicked_col, PLAYER_PIECE)

				if board.is_winning_move(PLAYER_PIECE):
					print('Player won')
					game_over = True

				turn += 1
				turn = turn % 2

				board.print()
				renderer.draw(board.get_state())

	if turn == AI and not game_over:
		# Use RL to get the best next move
		col, minimax_score = algo.get_best_move(board, 5, -math.inf, math.inf, True)

		if board.is_valid_location(col):
			row = board.get_next_open_row(col)
			board.drop_piece(row, col, AI_PIECE)

			if board.is_winning_move(AI_PIECE):
				print('AI won')
				game_over = True

			board.print()
			renderer.draw(board.get_state())

			turn += 1
			turn = turn % 2

	# if game_over:
		# pygame.time.wait(3000)