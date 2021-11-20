from Connect4_Globals import *
from Connect4_Players import Player, RandomPlayer

class ComputerPlayer(Player):
    """A class that represents an AI player in the game"""
    
    def __init__(self, coin_type, player_type, epsilon=0.2, alpha=0.3, gamma=0.9):
        """
        Initialize an AI with the proper type which are one of Random, 
        Q learner and Sarsa learner
        """
        if (player_type == "qlearner"):
            self.player = QLearningPlayer(coin_type, epsilon, alpha, gamma)
        elif (player_type == "sarsalearner"):
            self.player = SarsaLearningPlayer(coin_type, epsilon, alpha, gamma)
        elif (player_type == "montecarlo"):
            self.player = MonteCarloPlayer(coin_type)
        elif (player_type == "minimax"):
            self.player = MiniMaxPlayer(coin_type)
        else:
            self.player = RandomPlayer(coin_type)
            
    def complete_move(self, coin, board, game_logic, background):
        """
        Move the coin and decide which slot to drop it in and learn from the
        chosen move
        """
        actions = board.get_available_actions()
        state = board.get_state()
        chosen_action = self.choose_action(state, actions, coin, board, game_logic, background)
        coin.move_right(background, chosen_action)
        coin.set_column(chosen_action)
        game_over = board.insert_coin(coin, background, game_logic)
        self.player.learn(board, actions, chosen_action, game_over, game_logic)
        
        return game_over
    
    def get_coin_type(self):
        """
        Return the coin type of the AI player
        """
        return self.player.get_coin_type()
    
    def choose_action(self, state, actions, coin=None, board=None, game_logic=None, background=None):
        """
        Choose an action (which slot to drop in) based on the state of the
        board
        """
        return self.player.choose_action(state, actions, coin, board, game_logic, background)
        
class QLearningPlayer(Player):
    """A class that represents an AI using Q-learning algorithm"""
    
    def __init__(self, coin_type, epsilon=0.2, alpha=0.3, gamma=0.9):
        """
        Initialize a Q-learner with parameters epsilon, alpha and gamma
        and its coin type
        """
        Player.__init__(self, coin_type)
        self.q = {}
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards 
        
    def getQ(self, state, action):
        """
        Return a probability for a given state and action where the greater
        the probability the better the move
        """
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 1.0
        return self.q.get((state, action))    
        
    def choose_action(self, state, actions, coin, board, game_logic, background):
        """
        Return an action based on the best move recommendation by the current
        Q-Table with a epsilon chance of trying out a new move
        """
        current_state = state

        if random.random() < self.epsilon: # explore!
            chosen_action = random.choice(actions)
            return chosen_action

        qs = [self.getQ(current_state, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        return actions[i]
    
    def learn(self, board, actions, chosen_action, game_over, game_logic):
        """
        Determine the reward based on its current chosen action and update
        the Q table using the reward recieved and the maximum future reward
        based on the resulting state due to the chosen action
        """
        reward = 0
        if (game_over):
            win_value = game_logic.get_winner()
            if win_value == 0:
                reward = 0.5
            elif win_value == self.coin_type:
                reward = 1
            else:
                reward = -2
        prev_state = board.get_prev_state()
        prev = self.getQ(prev_state, chosen_action)
        result_state = board.get_state()
        maxqnew = max([self.getQ(result_state, a) for a in actions])
        self.q[(prev_state, chosen_action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)

class SarsaLearningPlayer(Player):
    """A class that represents an AI using Sarsa-learning algorithm"""
    
    def __init__(self, coin_type, epsilon=0.2, alpha=0.3, gamma=0.9):
        """
        Initialize a sarsa-learner with parameters epsilon, alpha and gamma
        and its coin type
        """
        Player.__init__(self, coin_type)
        self.q = {}
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards 
        
    def getQ(self, state, action):
        """
        Return a probability for a given state and action where the greater
        the probability the better the move
        """
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 1.0
        return self.q.get((state, action))    
        
    def choose_action(self, state, actions, coin, board, game_logic, background):
        """
        Return an action based on the best move recommendation by the current
        Q-Table with a epsilon chance of trying out a new move
        """
        current_state = state

        if random.random() < self.epsilon: # explore!
            chosen_action = random.choice(actions)
            return chosen_action

        qs = [self.getQ(current_state, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        return actions[i]
    def learn(self, board, actions, chosen_action, game_over, game_logic):
        """
        Determine the reward based on its current chosen action and update
        the Q table using the reward recieved and the exploring future reward
        based on the resulting state due to the chosen action
        """
        reward = 0
        if (game_over):
            win_value = game_logic.get_winner()
            if win_value == 0:
                reward = 0.5
            elif win_value == self.coin_type:
                reward = 1
            else:
                reward = -2
        prev_state = board.get_prev_state()
        prev = self.getQ(prev_state, chosen_action)
        result_state = board.get_state()
        qnew = self.getQ(result_state, chosen_action)
        self.q[(prev_state, chosen_action)] = prev + self.alpha * ((reward + self.gamma*qnew) - prev)

class MiniMaxPlayer(Player):
    def __init__(self, coin_type):
        Player.__init__(self, coin_type) # coin type is 1 or 2
        self.EMPTY = 0
        self.AI_PIECE = self.coin_type
        if self.AI_PIECE == 1:
            self.PLAYER_PIECE = 2
        else:
            self.PLAYER_PIECE = 1
        
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYER_PIECE 
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2
        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4
        return score  

    def score_position(self, board, piece):
        (board_n_rows, board_n_cols) = board.get_dimensions()
        board_state = np.asarray(board.get_state()) # convert tuple into numpy array
        n_in_a_row = board.get_n_in_a_row()
        score = 0
        ## Score center column
        center_array = [int(i) for i in list(board_state[:, board_n_cols//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(board_n_rows):
            row_array = [int(i) for i in list(board_state[r,:])]
            for c in range(board_n_cols-3):
                window = row_array[c:c+n_in_a_row]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(board_n_cols):
            col_array = [int(i) for i in list(board_state[:,c])]
            for r in range(board_n_rows-3):
                window = col_array[r:r+n_in_a_row]
                score += self.evaluate_window(window, piece)

        ## Score positive sloped diagonal
        for r in range(board_n_rows-3):
            for c in range(board_n_cols-3):
                window = [board_state[r+i][c+i] for i in range(n_in_a_row)]
                score += self.evaluate_window(window, piece)

        for r in range(board_n_rows-3):
            for c in range(board_n_cols-3):
                window = [board_state[r+3-i][c+i] for i in range(n_in_a_row)]
                score += self.evaluate_window(window, piece)
        return score  

    def choose_action(self, state, actions, coin, board, game_logic, background):
        minmax_algo = self.minmax(actions, coin, board, 6, -math.inf, math.inf, True, game_logic, background)
        next_action = minmax_algo[0]
        if next_action == None:
            return random.choice(actions)
        return next_action
        
    def minmax(self, actions, coin, board, depth, alpha, beta, maximizingPlayer, game_logic, background):
        AI_PIECE = self.AI_PIECE
        PLAYER_PIECE = self.PLAYER_PIECE            
        valid_locations = actions
        
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
                value = self.score_position(board, AI_PIECE)
                return (None, value)
                
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.determine_row_to_insert(col)
                b_copy = board.copy()
                b_copy.drop_piece(row, col, AI_PIECE)
                new_score = self.minmax(actions, coin, b_copy, depth-1, alpha, beta, False, game_logic, background)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (column, value)

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.determine_row_to_insert(col)
                b_copy = board.copy()
                b_copy.drop_piece(row, col, PLAYER_PIECE)
                new_score = self.minmax(actions, coin, b_copy, depth-1, alpha, beta, True, game_logic, background)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (column, value)
        
    def learn(self, board, actions, chosen_action, game_over, game_logic):
        """
        A method to make a move and update any learning parameters if any
        """
        pass 

# Adapted from: http://mcts.ai/code/python.html by Christopher Yong
# https://replit.com/talk/challenge/Connect-4-AI-using-Monte-Carlo-Tree-Search/10640
# https://jyopari.github.io/MCTS

class Node:
    def __init__(self, piece, board, parent=None, move=None):
        self.board = board.copy()
        self.parent = parent
        self.move = move
        self.untriedMoves = board.get_available_actions()
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.player = piece 
        
    # return child with largest UCT value
    def selection(self):
        # Upper Confidence bounds applied to Trees
        # uct = Xj + sqrt(In(N)/Nj)
        # Xj is the win ratio for a child node
        # N is the number of times the parent node has been visited
        # Nj is the number of times the child node has been visited.
        # Xj represents exploitation, as it is a large value when the win rate is high
        # Second term represents exploration, as it is large when the number of visits for that node have been low.
        uct = lambda x: x.wins / x.visits + np.sqrt(2 * np.log(self.visits) / x.visits)
        return sorted(self.childNodes, key=uct)[-1]

    # return child when move is taken
    # remove move from current node
    def expand(self, move, board):
        child = Node(piece=board.prev_player, 
                     board=board,
                     parent=self,
                     move=move)
        self.untriedMoves.remove(move)
        self.childNodes.append(child)
        return child

    def update(self, result):
        self.wins += result
        self.visits += 1

class MonteCarloPlayer(Player):
    """A class that represents an AI using montecarlo algorithm"""
    
    def __init__(self, coin_type):
        """
        Initialize a montecarlo player with coin type
        """
        self.currentNode = None
        Player.__init__(self, coin_type)
        self.cur_player = self.coin_type
        self.prev_player = 2 if self.cur_player == 1 else 1  
    
    def choose_action(self, state, actions, coin, board, game_logic, background):
        board.prev_player = self.prev_player
        board.current_player = self.cur_player

        self.currentNode = Node(piece=board.prev_player,board=board)
        return self.mcts(actions, board, 20000, self.currentNode, coin, game_logic, background, 5)

    def mcts(self, actions, board, itermax, currentNode, coin, game_logic, background, timeout=5):
        rootnode = Node(piece=board.prev_player,board=board)
        if currentNode is not None: rootnode = currentNode

        start = time.perf_counter()
        for i in range(itermax):
            node = rootnode
            state = board.copy()
            
            # selection
            while node.untriedMoves == [] and node.childNodes != []:
                # keep going down the tree based on best UCT values until terminal or unexpanded node
                
                node = node.selection()
                row = state.determine_row_to_insert(node.move)
                state.drop_piece(row, node.move, state.current_player)

            # expand
            if node.untriedMoves != []:
                col = random.choice(node.untriedMoves)
                row = state.determine_row_to_insert(col)
                state.drop_piece(row, col, state.current_player)
                node = node.expand(col, state)

            # rollout
            while state.get_available_actions():
                col = random.choice(state.get_available_actions())
                row = state.determine_row_to_insert(col)
                state.drop_piece(row, col, state.current_player)
                if state.is_winning_move(state.prev_player):
                    break    

            # backpropagate
            while node is not None:
                node.update(self.result(actions, state, node.player))
                node = node.parent

            duration = time.perf_counter() - start
            if duration > timeout: break

        win_ratio = lambda x: x.wins / x.visits
        sortedChildNodes = sorted(rootnode.childNodes, key=win_ratio)[::-1]
        return sortedChildNodes[0].move

    def result(self, actions, board, piece):
        opp_player = 2 if piece == 1 else 1  
        if board.is_winning_move(piece):  # player wins
            return 1
        elif board.is_winning_move(opp_player):  # opponent wins
            return 0
        elif len(board.get_available_actions()) == 0:  # draw
            return 0.5
    
    def learn(self, board, actions, chosen_action, game_over, game_logic):
        """
        A method to make a move and update any learning parameters if any
        """
        pass