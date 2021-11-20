from Connect4_Globals import *

class Player():
    """A class that represents a player in the game"""
    
    def __init__(self, coin_type):
        """
        Initialize a player with their coin type
        """
        self.coin_type = coin_type
        
    def complete_move(self):
        """
        A method to make a move and update any learning parameters if any
        """
        pass
    
    def get_coin_type(self):
        """
        Return the coin type of the player
        """
        return self.coin_type
    
    def set_coin_type(self, coin_type):
        """
        Set the coin type of a player
        """
        self.coin_type = coin_type
        
class HumanPlayer(Player):
    """A class that represents a human player in the game"""
    
    def __init__(self, coin_type):
        """
        Initialize a human player with their coin type
        """
        Player.__init__(self, coin_type)
        
class RandomPlayer(Player):
    """A class that represents a computer that selects random moves based on the moves available"""
    
    def __init__(self, coin_type):
        """
        Initialize the computer player
        """
        Player.__init__(self, coin_type)
        
    def choose_action(self, state, actions, coin, board, game_logic, background):
        """
        Choose a random action based on the available actions
        """
        return random.choice(actions)
                
    def learn(self, board, actions, chosen_action, game_over, game_logic):
        """
        The random player does not learn from its actions
        """
        pass