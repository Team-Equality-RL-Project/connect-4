# Import libraries
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pygame
import random
import time
import numpy as np
import copy
import math

# Board and Coin related global variables
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BOARD_SIZE = (6,7)

# Sensitivity Analysis tables
ep_rewards_table_alpha = {'ep': [], 'one': [], 'two': [], 'three': [], 'four': []}
ep_rewards_table_gamma = {'ep': [], 'one': [], 'two': [], 'three': [], 'four': []}

def reset_alpha_gamma_tables():
    ep_rewards_table_alpha = {'ep': [], 'one': [], 'two': [], 'three': [], 'four': []}
    ep_rewards_table_gamma = {'ep': [], 'one': [], 'two': [], 'three': [], 'four': []}
    
def show_alpha_sensitivity():
    # Plot Rewards vs episodes for different values of ALPHA (lr)
    plt.plot(ep_rewards_table_alpha['ep'], ep_rewards_table_alpha['one'], label="0.05")
    plt.plot(ep_rewards_table_alpha['ep'], ep_rewards_table_alpha['two'], label="0.25")
    plt.plot(ep_rewards_table_alpha['ep'], ep_rewards_table_alpha['three'], label="0.50")
    plt.plot(ep_rewards_table_alpha['ep'], ep_rewards_table_alpha['four'], label="0.75")
    plt.legend(loc=4) #bottom right
    plt.title('Connect Four learning rate alpha sensitivity')
    plt.ylabel('Game outcomes in %')
    plt.xlabel('Game number')
    plt.show()

def show_gamma_sensitivity():
    # Plot Rewards vs episodes for different values of GAMMA (discount)
    plt.plot(ep_rewards_table_gamma['ep'], ep_rewards_table_gamma['one'], label="0.98")
    plt.plot(ep_rewards_table_gamma['ep'], ep_rewards_table_gamma['two'], label="0.75")
    plt.plot(ep_rewards_table_gamma['ep'], ep_rewards_table_gamma['three'], label="0.50")
    plt.plot(ep_rewards_table_gamma['ep'], ep_rewards_table_gamma['four'], label="0.25")
    plt.legend(loc=4) #bottom right
    plt.title('Connect Four learning rate gamma sensitivity')
    plt.ylabel('Game outcomes in %')
    plt.xlabel('Game number')
    plt.show()
 