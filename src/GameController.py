# CMPE 260 Reinforcement Learning
## Connect 4 game - GameController class
##
## This class implements the connect 4 game
## It accepts a game playing player strategy and plays the game with it
## 
## Reference: https://github.com/KeithGalli/Connect4-Python
### Team Members: Abhishek Bais, Haley Feng, Princy Joy, Shannon Phu

# Import libraries and requisite classes
import pygame
import sys
import math
import board, renderer, minimax
import random
import math
from board import Board, PLAYER_PIECE, AI_PIECE, PLAYER, AI
from renderer import Renderer

# Implement the GameController class
class GameController:
    # Set the game playing strategy
    def __init__(self, algo):
        self.algo = algo
    
    # Play the game using the set strategy
    def playGame(self):
        game_over = False
        ROW_COUNT = 6
        COLUMN_COUNT = 7
        N_IN_A_ROW = 4
        board = Board(ROW_COUNT, COLUMN_COUNT, N_IN_A_ROW)
        board.print()
        renderer = Renderer(ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE)
        renderer.draw(board.get_state())
        turn = random.randint(PLAYER, AI)
        
        # Gameplay loop
        while not game_over:
            # Player's turn
            # Get frame and events from pygame graphics renderer. Get the column clicked by the player
            if turn == PLAYER:
                curr_piece = PLAYER_PIECE
                col = renderer.handle_events()

            # AI's turn
            # Use RL to get the best next move
            if turn == AI and not game_over:
                curr_piece = AI_PIECE
                col, minimax_score = self.algo.get_best_move(board, 5, -math.inf, math.inf, True)

            # Drop piece for current move
            if col != None and board.is_valid_location(col):
                row = board.get_next_open_row(col)
                board.drop_piece(row, col, curr_piece)

                if board.is_winning_move(curr_piece):
                    print(curr_piece, 'won')
                    game_over = True

                board.print()
                renderer.draw(board.get_state())

                turn += 1
                turn = turn % 2

            if game_over:
                if curr_piece == PLAYER_PIECE:
                    winner = 'PLAYER'
                else:
                    winner = 'AI'

                # Prints out who won and waits 3 seconds before closing game
                renderer.handle_game_end(winner)