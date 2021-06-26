from enum import Enum
import random

import logging

class Hand:
    def __init__(self):
        self.hand = self.gen_hand()
    def __repr__(self):
        return str(self.hand)

    def gen_hand(self):
        dice = [random.randint(1,6) for i in range(5)]
        while not self.validate_hand(dice):
            dice = [random.randint(1,6) for i in range(5)]
        
        # process into dice format
        # ie a 5 long array, with counts for each die value
        ret = [0] * 6
        for d in dice:
            ret[d-1] += 1
        return ret

    # validate the hand, ensure we don't need to reroll it
    def validate_hand(self, dice):
        # fail if shunzi 
        if len(set(dice)) == len(dice):
            return False

        return True
   
    # generate the game value for the hand
    def get_value(self, num, one_incl):
        ret = self.get_count(num)
        if one_incl and num != 1:
            ret += self.get_count(1)
        return ret

    def get_count(self, num):
        return self.hand[num - 1]

class Player:
    def __init__(self, name):
        self.hand = Hand()
        self.name = name
    def __repr__(self):
        return f'<{self.name}>: ' + str(self.hand)

    def get_value(self, num, one_incl):
        return self.hand.get_value(num, one_incl)

class Game:
    def __init__(self, a_name, b_name):
        self.a = Player(a_name)
        self.b = Player(b_name)
        # action_list contains list of claims and actions
        self.game_history = []
        self.next_player = 0

    def ask_action(self):
        if self.next_player == 0:
            action = self.a.get_action(self.game_history)
        elif self.next_player == 1:
            action = self.b.get_action(self.game_history)
        
        # alternate the next_player between 0 and 1
        self.next_player = self.next_player + pow(-1, self.next_player)

def main():
    p = Player('p1')

if __name__=="__main__":
    main()
