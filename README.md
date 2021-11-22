## CMPE 260 Reinforcement Learning
####  Project: Connect Four

####  Project Summary: 
Connect Four is a two player game in which players select different colored circular pieces, take turns to drop them in a 
6x7 grid. The first player to place four of their pieces consecutively in a row, column, or a diagonal line wins. A 
computer’s agent can learn to play Connect Four using reinforcement learning techniques, compete against human opponents 
and place pieces to win the game.

#### Team Members: Abhishek Bais, Haley Feng, Princy Joy, Shannon Phu

#### Game Details
The game can be played in three modes, namely
   1. SinglePlayer Mode - Human Player vs QLearning Player
   2. MultiPlayer Mode  - Human Player vs Human Player
   3. Trainer Mode      - Computer Player vs Computer Player 
  
   where,
   1. Human Player      - Accepts user input
   2. Computer Player   - Is of 5 types namely:
      i. Random         - Picks next move randomly from available locations
     ii. QLearner       - Picks next move based on QLearning
    iii. SarsaLearner   - Picks next move based on SarsaLearning
     iv. MonteCarlo     - Picks next move based on MonteCarlo algorithm
      v. Minimax        - Picks next move based on Minimax algorithm

Baseline hyper parameters for QLearner, SarsaLearner players are 
   1. QLearner, SarsaLearner epsilon - 0.2 
   2. QLearner, SarsaLearner alpha   - 0.3
   3. QLearner, SarsaLearner gamma   - 0.9
   
Sensitivity Analysis via hyper parameter tuning is performed on QLeaner in battles against Random Move player with
   1. alpha   = [0.05, 0.25, 0.5, 0.75], epsilon = 0.2, gamma = 0.9
   2. gamma   = [0.25, 0.5, 0.75, 0.98], epsilon = 0.2, alpha = 0.3
 
The algorithms used by different Computer Players are briefly described below
    1. QLearner
      Uses a reinforcement learning off-policy value based scheme based on the Bellman's equation to learn value of optimal 
      policy regardless of action

   2. SarsaLearner
      Uses a reinforcement learning on-policy value based scheme to learn the value of the optimal policy based on action  
      derived from the current policy

   3. MonteCarlo
      Uses Reinforcement Learning to learn directly game experiences without using any prior Markov Decision Process knowledge

   4. Minimax algorithm
      Uses a backtracking, recursive algorithm used in game theory to make moves that result in maximum immediate gain

#### Source File Structure
The Connect4_Globals.py defines the global variables used by the game. 
It includes
   1. Board size
   2. Color of coins 

The Connect4_Utilities.py defines utlity classes used by the game. 
It includes
   1. Slot                -  A position on the board
   2. Board               -  The 6x7 connect 4 playground
   3. Coin                -  A piece to play the game 
   4. SlotTrackerNode     -  A class that represents a internal node in the graph representation of the board
   5. ColumnFullException -  A class used to throw exceptions should coins drop in filled board positions

The Connect4_Players.py defines the players who can play the game. 
The Connect4_RLPlayers.py defines the types of computer players who can play the game. 
It includes
   1. Human Player       - Accepts user input
   2. Computer Player    - Is of 5 types namely:
      i.   Random        - Picks next move randomly from available locations
     ii.  QLearner       - Picks next move based on QLearning
    iii. SarsaLearner    - Picks next move based on SarsaLearning
     iv.  MonteCarlo     - Picks next move based on MonteCarlo algorithm
      v.   Minimax       - Picks next move based on Minimax algorithm
    
The Connect4_GameLogic.py defines the game logic.
It includes 
  1. Game winning cond.  - A sequence of 4 coins in a row (horizontal, vertical or diagonal)
  2. Game state          - Check whether the game is over?
  3. Game outcome        - Determine who won the game (red coin or blue coin) player or tie 

The Connect4_GameView.py configures the game.
It includes
  1. Game Menu           - The game graphic 
  2. Game Play Mode      - Pick the mode of play (SingePlayer, MultiPlayer or Trainer)  
  3. Game Setup and Play - Sets up the game between players and starts the game  

#### To play the game
Run src/Connect4_Play.ipynb

The following battles will be performed between different players 
For each of these games the different Computer Players will be configured with default hyper parameters 
  1. Qlearner     vs Random Move Player
  2. SarsaLearner vs Random Move Player
  3. Qlearner     vs SarsaLeaner Player
  4. MonteCarlo   vs Random Move Player
  5. MonteCarlo   vs Qlearner Player
  6. MonteCarlo   vs SarsaLearner Player
  7. Minimax      vs Random Move Player
  8. Minimax      vs Qlearner Player
  9. Minimax      vs SarsaLearner Player
  
 The Sensitivity Analysis is performed by battling Qlearner, SarsaLearner for different values of hyperparamers
  1. Qlearner vs Random Move Player for different hyper params (alpha, gamma) 
  2. SarsaLearner vs Random Move Player for different hyper params (alpha, gamma)
   
   Alpha sensitivity analysis is performed for
    i. alpha   = [0.05, 0.25, 0.5, 0.75]
   ii. epsilon = 0.2
   iii.gamma   = 0.9
   
   Gamma sensitivity analysis is performed for
    i. alpha   = 0.3
   ii. epsilon = 0.2
   iii.gamma   = [0.25, 0.5, 0.75, 0.98]

#### Sprints
The 260_sprint_backlog.xlsx.pdf contains the team's weekly sprints 
 
#### Deliverables
The deliverables directory contains
 1. Project_Presentation.ppt.pdf - The team project presentation
 2. Project_Report.pdf           - The team project report
 3. Connect4.mp3                 - The team presentation video
 
#### References:
1. https://github.com/ShekMaha/connect4-reinforcement-learning
2. https://github.com/KeithGalli/Connect4-Python