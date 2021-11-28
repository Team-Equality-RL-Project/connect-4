## CMPE 260 Reinforcement Learning
#### Course Instructor: Prof. Jahan Ghofraniha
#### Term Project: Connect Four
#### Team Members: Abhishek Bais, Haley Feng, Princy Joy, Shannon Phu

####  Project Summary: 
Connect Four is a two player game in which players select different colored circular pieces, take turns to drop them in a 
6x7 grid. The first player to place four of their pieces consecutively in a row, column, or a diagonal line wins. A 
computer agent can learn to play Connect Four using reinforcement learning techniques, compete against human opponents 
and place pieces to win the game.

#### Problem Statement:
1. Simulate a real-life Connect Four game playing experience for a human player against a computer player
2. Train reinforcement learning guided computer players implementing the following algorithms to play the game
     i. Monte Carlo Algorithm
    ii. Q Learning Algorithm
   iii. Sarsa Learning Algorithm
where, the training is done via N battles computer player that makes random moves and via battles against a
computer player that implements a game theory guided algorithm named Minimax.
3. Compare and contrast the performance of the reinforcement learning guided computer players on win-rate
   and efficiency (average play time).

#### Game Details:
The game can be played in three modes, namely
   1. SinglePlayer Mode - Human Player vs Computer Player
   2. MultiPlayer Mode  - Human Player vs Human Player
   3. Trainer Mode      - Reinforcement Learning Guided Computer Player vs Computer Player (Random), Computer Player (Minimax)
  
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
   
To get best results, hyper parameter tuning was performed on Q Leaner, Sarsa Learner for
   1. alpha or learning rate for values [0.05, 0.25, 0.5, 0.75], with epsilon = 0.2
   2. gamma or discount factor for values [0.25, 0.5, 0.75, 0.98], with epsilon = 0.2 on top of alpha tuning

To get best results, hyper parameter tuning was performed on Monte Carlo learner for
   1. Exploration coefficient for values [0.8, 1, 1.4, 1.6]
The Monte Carlo is a tree-search algorithm and the exploration coefficient controls the amount of search to perform
   1. Smaller Exploration Coefficient values lead to greater exploitation i.e., visited nodes are revisited
   2. Large Exploration Coefficient values lead to greater exploration i.e., new nodes are visited

The Sensitivity Analysis was performed by battling Qlearner, SarsaLearner, and Monte Carlo Player for different 
values of hyperparamers against a Computer Agent that made random moves.

#### Algorithms Implemented:
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
      Uses a backtracking, recursive algorithm commonly used in game theory to make moves that result in maximum immediate gain

#### Battles performed:
The following battles will be performed to train the different reinforcement learning guided computer players
  1. Qlearner     vs Random Move Player
  2. Qlearner     vs Minimax Player
  3. SarsaLearner vs Random Move Player
  4. SarsaLearner vs Minimax Player
  5. MonteCarlo   vs Random Move Player
  6. MonteCarlo   vs Minimax Player
  
  In addition, the different reinforcement learning guided computer players were also battled against each other
  to compare and contrast their performance measured in terms of win-rate and efficiency (average play time).
  
#### Source File Structure
The [Connect4_Globals.py](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/src/Connect4_Globals.py) defines the global variables used by the game. 
It includes
   1. Board size
   2. Color of coins 

The [Connect4_Utilities.py](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/src/Connect4_Utilities.py) defines utlity classes used by the game. 
It includes
   1. Slot                -  A position on the board
   2. Board               -  The 6x7 connect 4 playground
   3. Coin                -  A piece to play the game 
   4. SlotTrackerNode     -  A class that represents a internal node in the graph representation of the board
   5. ColumnFullException -  A class used to throw exceptions should coins drop in filled board positions

The [Connect4_Players.py](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/src/Connect4_Players.py) defines the players who can play the game.   
The [Connect4_RLPlayers.py](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/src/Connect4_RLPlayers.py) defines the types of computer players who can play the game. These includes  
   1. Human Player       - Accepts user input  
   2. Computer Player    - These are of 5 types namely:  
      i.   Random        - Picks next move randomly from available locations  
     ii.  QLearner       - Picks next move based on QLearning  
    iii. SarsaLearner    - Picks next move based on SarsaLearning  
     iv.  MonteCarlo     - Picks next move based on MonteCarlo algorithm  
      v.   Minimax       - Picks next move based on Minimax algorithm  
    
The [Connect4_GameLogic.py](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/src/Connect4_GameLogic.py) defines the game logic.
It includes 
  1. Game winning cond.  - A sequence of 4 coins in a row (horizontal, vertical or diagonal)
  2. Game state          - Check whether the game is over?
  3. Game outcome        - Determine who won the game (red coin or blue coin) player or tie 

The [Connect4_GameView.py](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/src/Connect4_GameView.py) configures the game.
It includes
  1. Game Menu           - The game graphic 
  2. Game Play Mode      - Pick the mode of play (SingePlayer, MultiPlayer or Trainer)  
  3. Game Setup and Play - Sets up the game between players and starts the game  

#### To play the game
Run [src/Connect4_Play.ipynb](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/src/Connect4_Play.ipynb)

#### Sprints
The [Team Sprint](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/sprints/260_sprint_backlog.xlsx.pdf) contains the team's weekly sprints 
 
#### Deliverables
The deliverables directory contains
 1. [Project Presentation](https://github.com/Team-Equality-RL-Project/connect-4/blob/master/deliverables/Project_Presentation.pptx.pdf) - The team project presentation
 2. Project_Report.pdf           - The team project report
 3. Project_Video.mp4            - The team presentation video
 
#### References:
1. https://github.com/ShekMaha/connect4-reinforcement-learning
2. https://github.com/KeithGalli/Connect4-Python
