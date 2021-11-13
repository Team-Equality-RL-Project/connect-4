import numpy as np

EMPTY = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
PLAYER1 = 0
PLAYER2 = 1

class Board:
    def __init__(self, n_rows, n_cols, n_in_a_row):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_in_a_row = n_in_a_row
        self.state = np.zeros((n_rows, n_cols))
        self.prev_move = None
        self.prev_player = None
        self.current_player = None

    def get_opponent(self, piece):
        if piece == PLAYER1_PIECE:
            return PLAYER2_PIECE
        else:
            return PLAYER1_PIECE

    def drop_piece(self, row, col, piece):
        self.state[row][col] = piece
        self.prev_move = col
        self.prev_player = piece
        self.current_player = self.get_opponent(piece)

    def is_valid_location(self, col):
        return self.state[self.n_rows-1][col] == 0

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.n_cols):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def get_next_open_row(self, col):
        for r in range(self.n_rows):
            if self.state[r][col] == 0:
                return r

    # Make a deep copy of the class
    def copy(self):
        BoardCopy = type('Board', Board.__bases__, dict(Board.__dict__))
        b = BoardCopy(self.n_rows, self.n_cols, self.n_in_a_row)
        b.state = self.state.copy()
        return b

    def get_n_rows(self):
        return self.n_rows

    def get_n_cols(self):
        return self.n_cols
    
    def get_n_in_a_row(self):
        return self.n_in_a_row

    def get_state(self):
        return self.state

    def print(self):
        print(np.flip(self.state, 0))

    def is_winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.n_cols-3):
            for r in range(self.n_rows):
                if self.state[r][c] == piece and self.state[r][c+1] == piece and self.state[r][c+2] == piece and self.state[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.n_cols):
            for r in range(self.n_rows-3):
                if self.state[r][c] == piece and self.state[r+1][c] == piece and self.state[r+2][c] == piece and self.state[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.n_cols-3):
            for r in range(self.n_rows-3):
                if self.state[r][c] == piece and self.state[r+1][c+1] == piece and self.state[r+2][c+2] == piece and self.state[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.n_cols-3):
            for r in range(3, self.n_rows):
                if self.state[r][c] == piece and self.state[r-1][c+1] == piece and self.state[r-2][c+2] == piece and self.state[r-3][c+3] == piece:
                    return True
    
    def is_terminal_node(self, PLAYER1_PIECE, PLAYER2_PIECE):
        return self.is_winning_move(PLAYER1_PIECE) or self.is_winning_move(PLAYER2_PIECE) or len(self.get_valid_locations()) == 0