from Connect4_Globals import *

class ColumnFullException(Exception):
    """An exception that will be thrown if a column of the board is full"""
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)   
    
class Slot():
    """A class that represents a single slot on the board"""
    SIZE=80
    def __init__(self, row_index, col_index, width, height, x1, y1):
        """
        Initialize a slot in a given position on the board
        """
        self.content = 0
        self.row_index = row_index
        self.col_index = col_index
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width*2, height*2))
        self.x_pos = x1
        self.y_pos = y1
        
    def get_location(self):
        """ 
        Return the location of the slot on the game board
        """
        return (self.row_index, self.col_index)
    
    def get_position(self):
        """
        Return the x and y positions of the top left corner of the slot on 
        the screen
        """
        return (self.x_pos, self.y_pos)
    
    def set_coin(self, coin):
        """
        Set a coin in the slot, which can be one of two colors
        """
        self.content = coin.get_coin_type()
        
    def check_slot_fill(self):
        """
        Return true iff a coin is placed in the slot
        """
        return (self.content != 0)
    
    def get_content(self):
        """
        Return what is stored in the slot, 0 if it is empty
        """
        return self.content
        
    def draw(self, background):
        """
        Draws a slot on the screen
        """
        pygame.draw.rect(self.surface, GREEN, (0, 0, self.width, self.height))
        pygame.draw.rect(self.surface, WHITE, (1,1,self.width - 2,self.height - 2))
        self.surface = self.surface.convert()
        background.blit(self.surface, (self.x_pos, self.y_pos))

class Board():
    """A class to represent the connect 4 board"""
    
    MARGIN_X = 300
    MARGIN_Y = 150
    
    def __init__(self, num_rows, num_columns):
        """
        Initialize a board with num_rows rows and num_columns columns
        """
        self.container = [[Slot(i, j, Slot.SIZE, Slot.SIZE, 
                                j*Slot.SIZE + Board.MARGIN_X, 
                                i*Slot.SIZE + Board.MARGIN_Y) for j in range(num_columns)] for i in range(num_rows)]
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.n_in_a_row = 4
        self.total_slots = num_rows * num_columns
        self.num_slots_filled = 0
        self.last_visited_nodes = []
        self.last_value = 0
        
        self.state = [[0 for j in range(num_columns)] for i in range(num_rows)]
        self.prev_state = None
        self.prev_move = (None, None, None)

        self.prev_move_col = None
        self.prev_player = None
        self.current_player = None
        # initialize the internal graph representation of the board
        # where every node is connected to all the other nodes in the 8 
        # directions surrounding it to which it already contains pointers
        self.representation = [[SlotTrackerNode() for j in range(num_columns)] for i in range(num_rows)]
        for i in range(num_rows):
            prev_row_index = i - 1
            next_row_index = i + 1
            for j in range(num_columns):
                prev_col_index = j - 1
                next_col_index = j + 1
                current_node = self.representation[i][j]
                if prev_row_index >= 0 and prev_col_index >=0:
                    current_node.top_left = self.representation[prev_row_index][prev_col_index]
                if prev_row_index >=0:
                    current_node.top = self.representation[prev_row_index][j]
                if prev_row_index >=0 and next_col_index < num_columns:
                    current_node.top_right = self.representation[prev_row_index][next_col_index]
                if prev_col_index >= 0:
                    current_node.left = self.representation[i][prev_col_index]
                    
                if next_col_index < num_columns:
                    current_node.right = self.representation[i][next_col_index]
                if next_row_index < num_rows and prev_col_index >= 0:
                    current_node.bottom_left = self.representation[next_row_index][prev_col_index]
                    
                if next_row_index < num_rows:
                    current_node.bottom = self.representation[next_row_index][j]
                if next_row_index < num_rows and next_col_index < num_columns:
                    current_node.bottom_right = self.representation[next_row_index][next_col_index]    
    
    def draw(self, background):
        """
        Method to draw the entire board on the screen
        """
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                self.container[i][j].draw(background)
                
    def get_slot(self, row_index, col_index):
        """
        Return a slot on the board given its row and column indices
        """
        return self.container[row_index][col_index]
    
    def check_column_fill(self, col_num):
        """
        Return True iff the column col_num on the board is filled up
        """
        for i in range(len(self.container)):
            # if a slot isn't filled then the column is not filled
            if not self.container[i][col_num].check_slot_fill():
                return False
        return True
    
    def insert_coin(self, coin, background, game_logic):
        """
        Insert the coin in the board and update board state and
        internal representation
        """
        col_num = coin.get_column()
        if not self.check_column_fill(col_num):
            row_index = self.determine_row_to_insert(col_num)
            self.container[row_index][col_num].set_coin(coin)
            if (self.prev_move[0] == None):
                self.prev_state = [[0 for j in range(self.num_columns)] for i in range(self.num_rows)]
            else:
                (prev_row, prev_col, value) = self.prev_move
                self.prev_state[prev_row][prev_col] = value
            self.prev_move = (row_index, col_num, coin.get_coin_type())    
            self.state[row_index][col_num] = coin.get_coin_type()
            self.update_slot_tracker(row_index, col_num, coin.get_coin_type())
            self.num_slots_filled += 1
            self.last_value = coin.get_coin_type()
            coin.drop(background, row_index)
            
        else:
            raise ColumnFullException('Column is already filled!')
        
        result = game_logic.check_game_over()
        
        return result
        
    def drop_piece(self, row, col, piece):
        self.state[row][col] = piece
        self.prev_move = col
        self.prev_player = piece
        self.current_player = 2 if piece == 1 else 1 
        
    def determine_row_to_insert(self, col_num):
        """
        Determine the row in which the coin can be dropped into
        """
        for i in range(len(self.container)):
            if self.container[i][col_num].check_slot_fill():
                return (i - 1)
        
        return self.num_rows - 1
                
    def get_dimensions(self):
        """
        Return the dimensions of the board
        """
        return (self.num_rows, self.num_columns)
    
    def get_n_in_a_row(self):
        return self.n_in_a_row
    
    def check_board_filled(self):
        """
        Return true iff the board is completely filled
        """
        return (self.total_slots == self.num_slots_filled)
            
    def get_representation(self):
        """
        Return the internal graph representation of the board
        """
        return self.representation
    
    def get_available_actions(self):
        """
        Return the available moves
        """
        actions = []
        for i in range(self.num_columns):
            if (not self.check_column_fill(i)):
                actions.append(i)
        return actions
    
    def copy(self):
        BoardCopy = type('Board', Board.__bases__, dict(Board.__dict__))
        b = BoardCopy(self.num_rows, self.num_columns)
        b.state = copy.deepcopy(self.state)
        b.prev_move_col = self.prev_move_col
        b.prev_player = self.prev_player
        b.current_player = self.current_player
        return b
    
    def is_winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.num_columns-3):
            for r in range(self.num_rows):
                if self.state[r][c] == piece and self.state[r][c+1] == piece and self.state[r][c+2] == piece and self.state[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.num_columns):
            for r in range(self.num_rows-3):
                if self.state[r][c] == piece and self.state[r+1][c] == piece and self.state[r+2][c] == piece and self.state[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.num_columns-3):
            for r in range(self.num_rows-3):
                if self.state[r][c] == piece and self.state[r+1][c+1] == piece and self.state[r+2][c+2] == piece and self.state[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.num_columns-3):
            for r in range(3, self.num_rows):
                if self.state[r][c] == piece and self.state[r-1][c+1] == piece and self.state[r-2][c+2] == piece and self.state[r-3][c+3] == piece:
                    return True
    
    def is_terminal_node(self, PLAYER1_PIECE, PLAYER2_PIECE):
        return self.is_winning_move(PLAYER1_PIECE) or self.is_winning_move(PLAYER2_PIECE) or len(self.get_available_actions()) == 0
    
    def get_state(self):
        """
        Return the 2d list numerical representation of the board
        """
        result = tuple(tuple(x) for x in self.state)
        
        return result
    
    def get_prev_state(self):
        """
        Return the previous state of the board
        """
        result = tuple(tuple(x) for x in self.prev_state)
        
        return result
    
    def get_last_filled_information(self):
        """
        Return the last visited nodes during the update step of the scores
        within the internal graph representation and also return the last 
        coin type inserted into the board
        """
        return (self.last_visited_nodes, self.last_value)
    
    def update_slot_tracker(self, i, j, coin_type):
        """
        Update the internal graph representation based on the latest insertion
        into the board
        """
        self.last_visited_nodes = []
        start_node = self.representation[i][j]
        start_node.value = coin_type
        self.traverse(start_node, coin_type, i, j, self.last_visited_nodes)
        # reset all the nodes as if it hadn't been visited
        for indices in self.last_visited_nodes:
            self.representation[indices[0]][indices[1]].visited = False
            
        
    def traverse(self, current_node, desired_value, i, j, visited_nodes):
        """
        Recursively update the scores of the relevant nodes based on its
        adjacent nodes (slots). If a coin type 1 is inserted into the board in 
        some position i, j, then update all adjacent slots that contain 1 with
        an updated score reflecting how many slots have 1 in a row in the top
        left, top right, etc directions
        """
        current_node.visited = True
        visited_nodes.append((i,j))
        if current_node.top_left:
            top_left_node = current_node.top_left
            if top_left_node.value == desired_value:
                current_node.top_left_score = top_left_node.top_left_score + 1
                if not top_left_node.visited:
                    self.traverse(top_left_node, desired_value, i - 1, j - 1, visited_nodes)
        if current_node.top:
            top_node = current_node.top
            if top_node.value == desired_value:
                current_node.top_score = top_node.top_score + 1
                if not top_node.visited:
                    self.traverse(top_node, desired_value, i - 1, j, visited_nodes)  
        if current_node.top_right:
            top_right_node = current_node.top_right
            if top_right_node.value == desired_value:
                current_node.top_right_score = top_right_node.top_right_score + 1
                if not top_right_node.visited:
                    self.traverse(top_right_node, desired_value, i - 1, j + 1, visited_nodes)          

        if current_node.left:
            left_node = current_node.left
            if left_node.value == desired_value:
                current_node.left_score = left_node.left_score + 1
                if not left_node.visited:
                    self.traverse(left_node, desired_value, i, j - 1, visited_nodes)    
                    
        if current_node.right:
            right_node = current_node.right
            if right_node.value == desired_value:
                current_node.right_score = right_node.right_score + 1
                if not right_node.visited:
                    self.traverse(right_node, desired_value, i, j + 1, visited_nodes)
                    
        if current_node.bottom_left:
            bottom_left_node = current_node.bottom_left
            if bottom_left_node.value == desired_value:
                current_node.bottom_left_score = bottom_left_node.bottom_left_score + 1
                if not bottom_left_node.visited:
                    self.traverse(bottom_left_node, desired_value, i + 1, j - 1, visited_nodes)
        
        if current_node.bottom:
            bottom_node = current_node.bottom
            if bottom_node.value == desired_value:
                current_node.bottom_score = bottom_node.bottom_score + 1
                if not bottom_node.visited:
                    self.traverse(bottom_node, desired_value, i + 1, j, visited_nodes)
                    
        if current_node.bottom_right:
            bottom_right_node = current_node.bottom_right
            if bottom_right_node.value == desired_value:
                current_node.bottom_right_score = bottom_right_node.bottom_right_score + 1
                if not bottom_right_node.visited:
                    self.traverse(bottom_right_node, desired_value, i + 1, j + 1, visited_nodes)

class Coin():
    """A class that represents the coin pieces used in connect 4"""
    
    RADIUS = 30
    
    def __init__(self, coin_type):
        """
        Initialize a coin with a given coin_type 
        (integer that represents its color)
        """
        self.coin_type = coin_type
        self.surface = pygame.Surface((Slot.SIZE - 3, Slot.SIZE - 3))
        if (self.coin_type == 1):
            self.color = BLUE
        else:
            self.color = RED
    
    def set_position(self, x1, y1):
        """
        Set the position of the coin on the screen
        """
        self.x_pos = x1
        self.y_pos = y1
        
    def set_column(self, col):
        """
        Set the column on the board in which the coin belongs
        """
        self.col = col
        
    def get_column(self):
        """
        Get the column on the board in which the coin belongs in
        """
        return self.col
    
    def set_row(self, row):
        """
        Set the row on the board where the coin is
        """
        self.row = row
        
    def get_row(self):
        """
        Get the row on the board in which the coin belongs
        """
        return self.row
    
    def move_right(self, background, step=1):
        """
        Move the coin to the column that is right of its current column
        """
        self.set_column(self.col + 1)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos + step * Slot.SIZE, self.y_pos)
        self.draw(background)
            
    def move_left(self, background):
        """
        Move the coin to the column that is left of its current column
        """
        self.set_column(self.col - 1)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos - Slot.SIZE, self.y_pos)
        self.draw(background)  
            
    def drop(self, background, row_num):
        """
        Drop the coin to the bottom most possible slot in its column
        """
        self.set_row(row_num)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos, self.y_pos + ((self.row + 1) * Slot.SIZE))
        self.surface.fill((255,255,255))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.draw(background) 
            
    def get_coin_type(self):
        """
        Return the coin type
        """
        return self.coin_type
    
    def draw(self, background):
        """
        Draw the coin on the screen
        """
        pygame.draw.circle(self.surface, self.color, (Slot.SIZE // 2, Slot.SIZE // 2), Coin.RADIUS)
        self.surface = self.surface.convert()
        background.blit(self.surface, (self.x_pos, self.y_pos))    

class SlotTrackerNode():
    """A class that that represents the node in the internal graph 
    representation of the game board"""
    
    def __init__(self):
        """
        Initialize the SlotTrackerNode with pointers to Nodes in all 
        8 directions surrounding along with a score count in each direction
        """
        self.top_left = None
        self.top_right = None
        self.top = None
        self.left = None
        self.right = None
        self.bottom_left = None
        self.bottom = None
        self.bottom_right = None       
        self.top_left_score = 1
        self.top_right_score = 1
        self.top_score = 1
        self.left_score = 1
        self.right_score = 1
        self.bottom_left_score = 1
        self.bottom_score = 1
        self.bottom_right_score = 1
        self.value = 0
        self.visited = False