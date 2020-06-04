import pygame
import math
from FileManagement import *
from ModelVisualization import *
from Model import *
import time
from matplotlib import pyplot as plt

"""
Main.py
================================
testy oraz szybsze zapisywanie jednostek do pliku
"""

if __name__ == '__main__':
    wins = [[], []]
    for i in range(100):
        model = Battlefield(10, 10)
        while model.running:
            model.step()
        if model.who_won() == 0:
            wins[0].append(0)
        else:
            wins[1].append(1)

    plt.hist(wins, bins=[0, 1, 2], histtype='bar', align='mid', orientation='vertical', label="WINS", color=["#ff0000","#00aab2"])
    plt.show()
