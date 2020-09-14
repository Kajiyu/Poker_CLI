import numpy as np
import os, sys
import glob
import random

from dealer import Dealer
from card import Card
from player import RandomPlayer, ManualPlayer


def check_action(action, player, dealer, d_value = 0):
    '''Actions:
            - 0: Fold
            - 1: Call/Check
            - 2: Bet/Raise
            - 3: All-in
        '''
    if action == 2: #Bet/Raise
        if d_value < player.points:
            if d_value > dealer.current_base_points:
                return 1
            else:
                return 0
        else:
            return 0
    elif action == 1:
        if d_value < player.points:
            return 1
        else:
            return 0
    else:
        return 1


n_players =  int(input("Enter the number of players (including you)"))
players = []
players.append(ManualPlayer(player_id=0))
for i in range(1, n_players):
    players.append(RandomPlayer(player_id=i))

dealer = Dealer()

is_game_finished = False
while is_game_finished is False:
    dealer.start_game(players)
    ## First action (Decide whether to join the current game or not)
    is_all_checked = False
    while is_all_checked is False:
        for player in players:
            if player.is_fold or player.is_all_in or player.is_lose:
                pass
            else:
                f_action = 0
                while f_action == 0:
                    _action, d_value = player.take_action(dealer)
                    f_action = check_action(_action, player, dealer, d_value=d_value)
                player.is_checked = True
                print("Player", player.player_id, ":", _action, d_value)
                if _action == 2:
                    dealer.current_base_points = d_value
                    for _player in players:
                        if player.player_id != _player.player_id:
                            _player.is_checked = False
                elif _action == 3:
                    if dealer.current_base_points < d_value:
                        dealer.current_base_points = d_value
                        for _player in players:
                            if player.player_id != _player.player_id:
                                _player.is_checked = False
        n_checked = 0
        for player in players:
            if player.is_fold or player.is_all_in or player.is_lose:
                player.is_checked = True
            if player.is_checked:
                n_checked += 1
        if n_checked == len(players):
            is_all_checked = True
            for player in players:
                if player.is_fold or player.is_lose:
                    pass
                elif player.is_all_in:
                    _point = player.points
                    if _point > 0:
                        player.update_points((-1)*_point)
                        dealer.point_pool += _point
                else:
                    player.update_points((-1)*dealer.current_base_points)
                    dealer.point_pool += dealer.current_base_points
    for player in players:
        print(player.player_id, ":", player.points)
    print(dealer.current_base_points, dealer.point_pool)
    for i in range(5):
        dealer.add_common_cards()
        is_all_checked = False
        while is_all_checked is False:
            for player in players:
                if player.is_fold or player.is_all_in or player.is_lose:
                    pass
                else:
                    f_action = 0
                    while f_action == 0:
                        _action, d_value = player.take_action(dealer)
                        f_action = check_action(_action, player, dealer, d_value=d_value)
                    player.is_checked = True
                    print("Player", player.player_id, ":", _action, d_value)
                    if _action == 2:
                        dealer.current_base_points = d_value
                        for _player in players:
                            if player.player_id != _player.player_id:
                                _player.is_checked = False
                    elif _action == 3:
                        if dealer.current_base_points < d_value:
                            dealer.current_base_points = d_value
                            for _player in players:
                                if player.player_id != _player.player_id:
                                    _player.is_checked = False
            n_checked = 0
            for player in players:
                if player.is_fold or player.is_all_in or player.is_lose:
                    player.is_checked = True
                if player.is_checked:
                    n_checked += 1
            if n_checked == len(players):
                is_all_checked = True
                for player in players:
                    if player.is_fold or player.is_lose:
                        pass
                    elif player.is_all_in:
                        _point = player.points
                        if _point > 0:
                            player.update_points((-1)*_point)
                            dealer.point_pool += _point
                    else:
                        player.update_points((-1)*dealer.current_base_points)
                        dealer.point_pool += dealer.current_base_points
        for player in players:
            print(player.player_id, ":", player.points)
    joining_players = []
    for player in players:
        if player.is_fold or player.is_lose:
            pass
        else:
            joining_players.append(player)
    results = dealer.determine_score(joining_players)
    winners = dealer.determine_winner(results)
    if len(winners) == 1:
        print("Winning player ID :", joining_players[winners[0]].player_id)
        players[joining_players[winners[0]].player_id].points += dealer.point_pool
    else:
        print("Tied Winning player ID :")
        for _winner in winners:
            print(joining_players[_winner].player_id)
            players[joining_players[_winner].player_id].points += int(dealer.point_pool/len(winners))
    print("Total Bedded points:", dealer.point_pool)
    n_losers = 0
    for player in players:
        player.init_for_next_game()
        print(player.player_id, ":", player.points, player.is_lose)
        if player.is_lose:
            n_losers += 1
    if n_losers > n_players - 2:
        is_game_finished = True
        print("Finished")
    else:
        dealer.reset()
        print("Go to next game.", "\n")