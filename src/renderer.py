import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
SQUARESIZE = 100

class Renderer:
    def __init__(self, n_rows, n_cols, piece_a, piece_b):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.width = n_cols * SQUARESIZE
        self.height = (n_rows+1) * SQUARESIZE
        self.size = (self.width, self.height)
        self.radius = int(SQUARESIZE / 2 - 5)
        self.piece_a = piece_a # player piece
        self.piece_b = piece_b # AI piece

        pygame.init()
        self.font = pygame.font.SysFont("monospace", 75)
        self.screen = pygame.display.set_mode(self.size)
        self.draw_board()
        pygame.display.update()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(self.screen, RED, (posx, int(SQUARESIZE/2)), self.radius)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))

                # Ask for Player 1 Input
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                return col
                
        return None
    
    def handle_click(self, board):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('clicked!')
                pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
                # Ask for Player 1 Input
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if board.is_valid_location(col):
                    return col
            pygame.display.update()
        return None
    
    def handle_game_end(self, winner):
        label = self.font.render(winner + " wins!!", 1, YELLOW)
        self.screen.blit(label, (40,10))
        pygame.display.update()
        pygame.time.wait(3000)

    def draw_board(self):
        for c in range(self.n_cols):
            for r in range(self.n_rows):
                pygame.draw.rect(self.screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), self.radius)
        pygame.display.update()

    def draw(self, board_state):
        self.draw_board()

        for c in range(self.n_cols):
            for r in range(self.n_rows):
                if board_state[r][c] == self.piece_a:
                    pygame.draw.circle(self.screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int(r*SQUARESIZE+SQUARESIZE/2)), self.radius)
                elif board_state[r][c] == self.piece_b: 
                    pygame.draw.circle(self.screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int(r*SQUARESIZE+SQUARESIZE/2)), self.radius)
        pygame.display.update()