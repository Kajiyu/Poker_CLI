import numpy as np
import os, sys
import glob
import random


class Card:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value
    
    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        elif self.value == other.value:
            return 0
        return 1
    
    def __str__(self):
        # Value
        text = ""
        if self.value < 0:
            return "Joker";
        elif self.value == 11:
            text = "J"
        elif self.value == 12:
            text = "Q"
        elif self.value == 13:
            text = "K"
        elif self.value == 14:
            text = "A"
        else:
            text = str(self.value)
        # Symbol
        if self.symbol == 0:    #D-Diamonds
            text += "D" 
        elif self.symbol == 1:  #H-Hearts
            text += "H"
        elif self.symbol == 2:  #S-Spade
            text += "S"
        else:   #C-Clubs
            text += "C"
            
        return text