import numpy as np
import os, sys
import glob
import random


class PlayerBase:
    '''The base class for player-bots
    '''
    def __init__(self, player_id, points=1000):
        self.points = points
        self.is_fold = False
        self.is_all_in = False
        self.is_lose = False
        self.is_checked = False
        self.player_cards = []
        self.player_id = player_id
    
    def take_action(self, dealer):
        '''Actions:
            - 0: Fold
            - 1: Call/Check
            - 2: Bet/Raise
            - 3: All-in
        '''
        pass
    
    def update_points(self, d_points):
        self.points = self.points + d_points
    
    def init_for_next_game(self):
        self.player_cards = []
        self.is_fold = False
        if self.points > 0:
            self.is_all_in = False
        else:
            self.is_all_in = True
            self.is_lose = True
            

class ManualPlayer(PlayerBase):
    ''' For user-input
    '''
    def __init__(self, player_id, points=1000):
        super().__init__(player_id=player_id, points=points)
    
    def take_action(self, dealer):
        print("This is your turn.")
        print("Your cards: ")
        print(self.player_cards[0], self.player_cards[1])
        action = int(input('Enter your action: '))
        if action == 2:
            d_points = int(input('Enter the points you add: '))
        elif action == 3:
            d_points = self.points
            self.is_all_in = True
        elif action == 0:
            self.is_fold = True
            d_points = 0
        else:
            d_points = dealer.current_base_points
        return action, d_points


class RandomPlayer(PlayerBase):
    ''' For user-input
    '''
    def __init__(self, player_id, points=1000):
        super().__init__(player_id=player_id, points=points)
    
    def take_action(self, dealer):
        action = random.randint(0, 3)
        if action == 2:
            if dealer.current_base_points == self.points:
                d_points = self.points
            elif dealer.current_base_points > self.points:
                d_points = self.points
            else:
                d_points = random.randint(dealer.current_base_points, self.points - 1)
        elif action == 3:
            d_points = self.points
            self.is_all_in = True
        elif action == 0:
            self.is_fold = True
            d_points = 0
        else:
            d_points = dealer.current_base_points
        return action, d_points


class ChickenPlayer(PlayerBase):
    '''
    '''
    def __init__(self, player_id, points=1000):
        super().__init__(player_id=player_id, points=points)


class StupidPlayer(PlayerBase):
    '''
    '''
    def __init__(self, player_id, points=1000):
        super().__init__(player_id=player_id, points=points)