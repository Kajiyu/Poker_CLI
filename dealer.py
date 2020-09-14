import numpy as np
import os, sys
import glob
import random

from card import Card


class Dealer:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.common_cards = []
        self.card_pool = []
        self.current_base_points = 0
        self.point_pool = 0
        for i in range(2, 15):
            for j in range(4):
                _card = Card(j, i)
                self.card_pool.append(_card)
    
    def start_game(self, players):
        '''
            Keyword argument:
                - players: a list of players
            Returns:
                - 
        '''
        for player in players:
            first_card = self.card_pool.pop(random.randrange(len(self.card_pool)))
            second_card = self.card_pool.pop(random.randrange(len(self.card_pool)))
            player.player_cards.append(first_card)
            player.player_cards.append(second_card)
            print(first_card, second_card)
    
    def add_common_cards(self):
        new_card = self.card_pool.pop(random.randrange(len(self.card_pool)))
        self.common_cards.append(new_card)
        print("Now common cards : ")
        for c_card in self.common_cards:
            print(c_card)
        print("\n")
    
    def score(self, hand):
        '''
            Calculate the score of cards of each player
            Keyword argument:
                - hand: a list of cards
            Returns:
                - 
        '''
        score = 0
        kicker = []
        
        #------------------------------------------------
        #-------------Checking for Pairs-----------------
        #------------------------------------------------
        pairs = {}
        prev = 0
        
        #Keeps track of all the pairs in a dictionary where the key is the pair's card value
        #and the value is the number occurrences. Eg. If there are 3 Kings -> {"13":3} 
        for card in hand:
            if prev == card.value:
                key = card.value
                if key in pairs:
                    pairs[key] += 1
                else:
                    pairs[key] = 2
            prev = card.value
        
        #Keeps track of the number of pairs and sets. The value of the previous dictionary
        #is the key. Therefore if there is a pair of 4s and 3 kings -> {"2":1,"3":1}
        nop = {}
        for k, v in iter(pairs.items()):
            if v in nop:
                nop[v] += 1
            else:
                nop[v] = 1
        
        #Here we determine the best possible combination the hand can be knowing if the
        #hand has a four of a kind, three of a kind, and multiple pairs.
        
        if 4 in nop:        #Has 4 of a kind, assigns the score and the value of the 
            score = 7
            kicker = list(pairs.keys())
            #ensures the first kicker is the value of the 4 of a kind
            kicker = [key for key in kicker if pairs[key] == 4] 
            key = kicker[0]

            #Gets a list of all the cards remaining once the the 4 of a kind is removed
            temp = [card.value for card in hand if card.value != key]
            #Gets the last card in the list which is the highest remaining card to be used in 
            #the event of a tie
            card_value = temp.pop()
            kicker.append(card_value)
            
            return [score, kicker] # Returns immediately because this is the best possible hand
            #doesn't check get the best 5 card hand if all users have a 4 of a kind
            
        elif 3 in nop:      #Has At least 3 of A Kind
            if nop[3] == 2 or 2 in nop:     #Has two 3 of a kind, or a pair and 3 of a kind (fullhouse)
                score = 6
                
                #gets a list of all the pairs and reverses it
                kicker = list(pairs.keys())
                kicker.reverse()
                temp = kicker
                
                #ensures the first kicker is the value of the highest 3 of a king
                kicker = [key for key in kicker if pairs[key] == 3]
                if( len(kicker) > 1):   # if there are two 3 of a kinds, take the higher as the first kicker
                    kicker.pop() #removes the lower one from the kicker
                
                #removes the value of the kicker already in the list
                temp.remove(kicker[0])
                #Gets the highest pair or 3 of kind and adds that to the kickers list
                card_value = temp[0]
                kicker.append(card_value)
                
            else:           #Has Only 3 of A Kind
                score = 3
                
                kicker = list(pairs.keys())      #Gets the value of the 3 of a king
                key = kicker[0]
                
                #Gets a list of all the cards remaining once the three of a kind is removed
                temp = [card.value for card in hand if card.value != key]
                #Get the 2 last cards in the list which are the 2 highest to be used in the 
                #event of a tie
                card_value = temp.pop()
                kicker.append(card_value)
                
                card_value = temp.pop()
                kicker.append(card_value)
    
        elif 2 in nop:      #Has at Least a Pair
            if nop[2] >= 2:     #Has at least 2  or 3 pairs
                score = 2
                
                kicker = list(pairs.keys())   #Gets the card value of all the pairs 
                kicker.reverse()        #reverses the key so highest pairs are used
                
                if ( len(kicker) == 3 ):    #if the user has 3 pairs takes only the highest 2
                    kicker.pop()
                    
                key1 = kicker[0]
                key2 = kicker[1]
                
                #Gets a list of all the cards remaining once the the 2 pairs are removed
                temp = [card.value for card in hand if card.value != key1 and card.value != key2]
                #Gets the last card in the list which is the highest remaining card to be used in 
                #the event of a tie
                card_value = temp.pop()
                kicker.append(card_value)
                
            else:           #Has only a pair
                score = 1 
                
                kicker = list(pairs.keys())
                #Gets the value of the pair
                key = kicker[0] 
     
                #Gets a list of all the cards remaining once pair are removed
                temp = [card.value for card in hand if card.value != key]
                #Gets the last 3 cards in the list which are the highest remaining cards
                #which will be used in the event of a tie
                card_value = temp.pop()
                kicker.append(card_value)
                
                card_value = temp.pop()
                kicker.append(card_value)
                
                card_value = temp.pop()
                kicker.append(card_value)
                
        
        #------------------------------------------------
        #------------Checking for Straight---------------
        #------------------------------------------------    
        #Doesn't check for the ace low straight
        counter = 0
        high = 0
        straight = False
        
        #Checks to see if the hand contains an ace, and if so starts checking for the straight
        #using an ace low
        if (hand[6].value == 14):
            prev = 1
        else: 
            prev = None
            
        #Loops through the hand checking for the straight by comparing the current card to the
        #the previous one and tabulates the number of cards found in a row
        #***It ignores pairs by skipping over cards that are similar to the previous one
        for card in hand:
            if prev and card.value == (prev + 1):
                counter += 1
                if counter == 4: #A straight has been recognized
                    straight = True
                    high = card.value
            elif prev and prev == card.value: #ignores pairs when checking for the straight
                pass
            else:
                counter = 0
            prev = card.value
        
        #If a straight has been realized and the hand has a lower score than a straight
        if (straight or counter >= 4) and score < 4:
            straight = True  
            score = 4
            kicker = [high] #Records the highest card value in the straight in the event of a tie
    
    
        #------------------------------------------------
        #-------------Checking for Flush-----------------
        #------------------------------------------------
        flush = False
        total = {}
        
        for card in hand:
            key = card.symbol
            if key in total:
                total[key] += 1
            else:
                total[key] = 1
        
        key = -1
        for k, v in iter(total.items()):
            if v >= 5:
                key = int(k)
        
        if key != -1 and score < 5:
            flush = True
            score = 5
            kicker = [card.value for card in hand if card.symbol == key]        
        
        
        #------------------------------------------------
        #-----Checking for Straight & Royal Flush--------
        #------------------------------------------------
        if flush and straight:
            
            #Doesn't check for the ace low straight
            counter = 0
            high = 0
            straight_flush = False
            
            if (kicker[len(kicker)-1] == 14): 
                prev = 1
            else: 
                prev = None
                
            for card in kicker:
                if prev and card == (prev + 1):
                    counter += 1
                    if counter >= 4: #A straight has been recognized
                        straight_flush = True
                        high = card
                elif prev and prev == card: #ignores pairs when checking for the straight
                    pass
                else:
                    counter = 0
                prev = card
            
            #If a straight has been realized and the hand has a lower score than a straight
            if straight_flush:
                if high == 14:
                    score = 9
                else:
                    score = 8
                kicker = [high]
                return [score, kicker]
        
        if flush:     #if there is only a flush then determines the kickers
            kicker.reverse()
            
            #This ensures only the top 5 kickers are selected and not more.
            length = len(kicker) - 5
            for i in range (0,length):
                kicker.pop() #Pops the last card of the list which is the lowest
        
        #------------------------------------------------
        #-------------------High Card--------------------
        #------------------------------------------------
        if score == 0:      #If the score is 0 then high card is the best possible hand
            
            #It will keep track of only the card's value
            kicker = [int(card.value) for card in hand]
            #Reverses the list for easy comparison in the event of a tie
            kicker.reverse()
            #Since the hand is sorted it will pop the two lowest cards position 0, 1 of the list
            kicker.pop()
            kicker.pop()      
        
        #Return the score, and the kicker to be used in the event of a tie
        return [score, kicker]
    
    def determine_score(self, players):
        players_hands = []
        for _player in players:
            players_hands.append(_player.player_cards)
        
        for hand in players_hands:
            hand.extend(self.common_cards)
#             hand.sort()
    
        results = []
        for hand in players_hands:
                     
            overall = self.score(hand)
            results.append([overall[0], overall[1]])    # Stores the results
        print(results)
        return results
    
    def determine_winner(self, results):
        #the highest score if found
        high = 0
        for r in results:
            if r[0] > high:
                high = r[0]
            
        kicker = {}    
        counter = 0
        #Only the kickers of the player's hands that are tied for the win are analysed
        for r in results:
            if r[0] == high:
                kicker[counter] = r[1]
                
            counter += 1
        
        #if the kickers of multiple players are in the list then we have a tie and need
        #to begin comparing kickers 
        if(len(kicker) > 1):
            
            #Iterate through all the kickers
            #It is important to the number of kickers differ based on the type of hand
            number_of_kickers = len(kicker[list(kicker.keys()).pop()])
            for i in range (0, number_of_kickers):
                high = 0
                for k, v in kicker.items():
                    if v[i] > high:
                        high = v[i]
                
                #only hands matching the highest kicker remain in the list to be compared
                kicker = {k:v for k, v in kicker.items() if v[i] == high}
                
                #if only one the kickers of one player remains that they are the winner
                if( len(kicker) <= 1):
                    return [list(kicker.keys()).pop()]
                
        else:   # A clear winner was found
            return [list(kicker.keys()).pop()]
        
        # A tie occurred, a list of the winners is returned
        return list(kicker.keys())