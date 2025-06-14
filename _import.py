import pygame
import random
import os
import sys
from collections import Counter 
from score_category import ScoreCategory
from score_category import Ones, Twos, Threes, Fours, Fives, Sixes, ThreeOfAKind, FourOfAKind, FullHouse, SmallStraight, LargeStraight, Yahtzee,Chance
# Globalne stałe
WIDTH, HEIGHT = 1800, 1000

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TRANSPARENT = (0, 0, 0, 0)
GOLD = (183, 147, 60)
YELLOW = (212, 175, 55) 


