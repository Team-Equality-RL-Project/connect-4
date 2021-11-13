import numpy as np
import copy
import time
import random

# Adapted from: http://mcts.ai/code/python.html by Christopher Yong
# https://replit.com/talk/challenge/Connect-4-AI-using-Monte-Carlo-Tree-Search/10640
# https://jyopari.github.io/MCTS

class Node:
    def __init__(self, piece, board, parent=None, move=None):
        self.board = copy.deepcopy(board)
        self.parent = parent
        self.move = move
        self.untriedMoves = board.get_valid_locations()
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


###################################

class MonteCarloTreeSearch():
    def __init__(self):
        pass


    def get_best_move(self, board):
        self.currentNode = Node(piece=board.current_player, board=board)
        return self.mcts(board, 20000, self.currentNode, 5)


    def mcts(self, board, itermax, currentNode, timeout=5):
        rootnode = Node(piece=board.prev_player, board=board)
        if currentNode is not None: rootnode = currentNode

        start = time.perf_counter()
        for i in range(itermax):
            node = rootnode
            state = copy.deepcopy(board)

            # selection
            while node.untriedMoves == [] and node.childNodes != []:
                # keep going down the tree based on best UCT values until terminal or unexpanded node
                node = node.selection()
                row = state.get_next_open_row(node.move)
                state.drop_piece(row, node.move, state.current_player)

            # expand
            if node.untriedMoves != []:
                col = random.choice(node.untriedMoves)
                row = state.get_next_open_row(col)
                state.drop_piece(row, col, state.current_player)
                node = node.expand(col, state)

            # rollout
            while state.get_valid_locations():
                col = random.choice(state.get_valid_locations())
                row = state.get_next_open_row(col)
                state.drop_piece(row, col, state.current_player)
                if state.is_winning_move(state.prev_player):
                    break

            # backpropagate
            while node is not None:
                node.update(self.result(state, node.player))
                node = node.parent

            duration = time.perf_counter() - start
            if duration > timeout: break

        win_ratio = lambda x: x.wins / x.visits
        sortedChildNodes = sorted(rootnode.childNodes, key=win_ratio)[::-1]
        return sortedChildNodes[0].move


    def goto_childNode(self, node, board, move, piece):
        for child in node.childNodes:
            if child.move == move:
                return child
        return Node(piece=piece, board=board)


    def result(self, board, piece):
        if board.is_winning_move(piece):  # player wins
            return 1
        elif board.is_winning_move(board.get_opponent(piece)):  # opponent wins
            return 0
        elif len(board.get_valid_locations()) == 0:  # draw
            return 0.5
