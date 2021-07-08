from enum import Enum
import random
import logging

import util

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
        # ie a 6 long array, with counts for each die value
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
    
    # Given the game history, produce the next action.
    # If not automated, then get it from stdin
    def get_action(self, game_history, manual=False):
        if manual:
            next_move = util.get_move_from_stdin(self.name)
        else:
            raise ValueError
        return next_move
        

class Action:
    class DOUBT:
        def __init__(self):
            pass
        def __repr__(self):
            return f'<{self.__class__.__name__}>'

    class BID:
        def __init__(self, count, rank, incl_one):
            self.count = count
            self.rank = rank 
            self.incl_one = incl_one
        def __repr__(self):
            return f'<{self.__class__.__name__}: c {self.count},'\
                    + f'r {self.val},'\
                    + f'incl {"Y" if self.incl_one else "N"}>'

class Game:
    def __init__(self, a_name, b_name, manual=False):
        self.a = Player(a_name)
        self.b = Player(b_name)
        self.manual = manual
        self.player_lim = 2
        # action_list contains list of claims and actions
        self.game_history = []
        self.next_player = 0

    def game_loop(self):
        game_over = False
        while not game_over:
            next_act = self.ask_action()
            self.game_history += [next_act]
            #self.process_move()
            self.rotate_player()

    def ask_action(self):
        if self.next_player == 0:
            action = self.a.get_action(self.game_history, self.manual)
        elif self.next_player == 1:
            action = self.b.get_action(self.game_history, self.manual)
        return (self.next_player, action)

    def process_action(self):
        last_player,last_action = self.game_history[-1]

    # alternate the next_player between 0 and 1
    def rotate_player(self):
        self.next_player = (self.next_player + 1) % self.player_lim

    def validate_action(self):
        pass

def main():
    g = Game('a', 'b', manual=True)
    g.game_loop()




if __name__=="__main__":
    main()
