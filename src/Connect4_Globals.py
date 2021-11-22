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
ep_outcomes_table_alpha = {'ep': [], 'one': [], 'two': [], 'three': [], 'four': []}
ep_outcomes_table_gamma = {'ep': [], 'one': [], 'two': [], 'three': [], 'four': []}
ep_outcomes_table_exp_coeff = {'ep': [], '0.8': [], '1': [], '1.4': [], '1.6': []}

def reset_alpha_gamma_tables():
    ep_outcomes_table_alpha = {'ep': [], 'one': [], 'two': [], 'three': [], 'four': []}
    ep_outcomes_table_gamma = {'ep': [], 'one': [], 'two': [], 'three': [], 'four': []}
    ep_outcomes_table_exp_coeff = {'ep': [], '0.8': [], '1': [], '1.4': [], '1.6': []}

    
def show_alpha_sensitivity():
    # Plot outcome vs games for different values of ALPHA (lr)
    plt.plot(ep_outcomes_table_alpha['ep'], ep_outcomes_table_alpha['one'], label="0.05")
    plt.plot(ep_outcomes_table_alpha['ep'], ep_outcomes_table_alpha['two'], label="0.25")
    plt.plot(ep_outcomes_table_alpha['ep'], ep_outcomes_table_alpha['three'], label="0.50")
    plt.plot(ep_outcomes_table_alpha['ep'], ep_outcomes_table_alpha['four'], label="0.75")
    plt.legend(loc=4) #bottom right
    plt.title('Connect Four learning rate alpha sensitivity')
    plt.ylabel('Game outcomes in %')
    plt.xlabel('Game number')
    plt.show()

def show_gamma_sensitivity():
    # Plot outcome vs games for different values of GAMMA (discount)
    plt.plot(ep_outcomes_table_gamma['ep'], ep_outcomes_table_gamma['one'], label="0.25")
    plt.plot(ep_outcomes_table_gamma['ep'], ep_outcomes_table_gamma['two'], label="0.50")
    plt.plot(ep_outcomes_table_gamma['ep'], ep_outcomes_table_gamma['three'], label="0.75")
    plt.plot(ep_outcomes_table_gamma['ep'], ep_outcomes_table_gamma['four'], label="0.98")
    plt.legend(loc=4) #bottom right
    plt.title('Connect Four discount gamma sensitivity')
    plt.ylabel('Game outcomes in %')
    plt.xlabel('Game number')
    plt.show()
 

def show_exp_coeff_sensitivity():
    # Plot outcome vs games for different values of exploration coefficient
    plt.plot(ep_outcomes_table_exp_coeff['ep'], ep_outcomes_table_exp_coeff['0.8'], label="0.8")
    plt.plot(ep_outcomes_table_exp_coeff['ep'], ep_outcomes_table_exp_coeff['1'], label="1")
    plt.plot(ep_outcomes_table_exp_coeff['ep'], ep_outcomes_table_exp_coeff['1.4'], label="1.4")
    plt.plot(ep_outcomes_table_exp_coeff['ep'], ep_outcomes_table_exp_coeff['1.6'], label="1.6")
    plt.legend(loc=4) #bottom right
    plt.title('Connect Four exploration coefficient sensitivity')
    plt.ylabel('Game outcomes in %')
    plt.xlabel('Game number')
    plt.show()

