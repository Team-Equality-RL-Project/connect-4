import math
import random

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

class Minimax():
    def __init__(self):
        pass
    
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board_state, board_n_rows, board_n_cols, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board_state[:, board_n_cols//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(board_n_rows):
            row_array = [int(i) for i in list(board_state[r,:])]
            for c in range(board_n_cols-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(board_n_cols):
            col_array = [int(i) for i in list(board_state[:,c])]
            for r in range(board_n_rows-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(board_n_rows-3):
            for c in range(board_n_cols-3):
                window = [board_state[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(board_n_rows-3):
            for c in range(board_n_cols-3):
                window = [board_state[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def get_best_move(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = board.get_valid_locations()
        is_terminal = board.is_terminal_node(PLAYER_PIECE, AI_PIECE)
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.is_winning_move(AI_PIECE):
                    return (None, 100000000000000)
                elif board.is_winning_move(PLAYER_PIECE):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board.get_state(), board.get_n_rows(), board.get_n_cols(), AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                b_copy = board.copy()
                b_copy.drop_piece(row, col, AI_PIECE)
                new_score = self.get_best_move(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                b_copy = board.copy()
                b_copy.drop_piece(row, col, PLAYER_PIECE)
                new_score = self.get_best_move(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value