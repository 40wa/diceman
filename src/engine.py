from enum import Enum
import random
import logging
import sys

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

    def get_count(self, rank):
        try:
            return self.hand[rank - 1]
        except IndexError:
            # The rank specified is out of rank, it seems
            return 0

    def get_hand(self):
        return self.hand

class Player:
    def __init__(self, name):
        self.hand = Hand()
        self.name = name
    def __repr__(self):
        return f'<{self.name}>: ' + str(self.hand)
    def get_hand_value(self, num, one_incl):
        return self.hand.get_value(num, one_incl)
    
    # Given the game history, produce the next action.
    # If not automated, then get it from stdin
    def get_action(self, game_history, manual=False):
        if manual:
            next_move = util.get_move_from_stdin(self.name)
        else:
            raise ValueError
        return next_move

    def get_hand(self):
        return self.hand.get_hand()
        

class Action:
    class DOUBT:
        def __init__(self):
            self.action_type = 'DOUBT'
            pass
        def __repr__(self):
            return f'<{self.__class__.__name__}>'

    class BID:
        def __init__(self, count, rank, incl_one):
            self.action_type = 'BID'
            self.count = count
            self.rank = rank 
            self.incl_one = incl_one
        def __repr__(self):
            return f'<{self.__class__.__name__}: c {self.count},'\
                    + f'r {self.rank},'\
                    + f'incl {"Y" if self.incl_one else "N"}>'

class Game:
    def __init__(self, total_players, manual=False):
        #players stored in an array, referred to by their index
        self.players = [Player(chr(ord('@')+1+i)) for i in range(total_players)]
        self.manual = manual
    
        # total number of players
        self.total_players = total_players
        # action_list contains list of claims and actions
        self.game_history = []
        # integer denoting who is next to move
        self.next_player = 0
        # flag indicating whether rank "one" die have been used yet
        self.ones_used = False
        # flag indicating whether or not game is over
        self.game_over = False

    def game_loop(self):
        while not self.game_over:
            next_act = self.ask_action()
            self.game_history += [next_act]
            self.process_last_action()
            self.rotate_player()

    def ask_action(self):
        action = self.players[self.next_player].get_action(self.game_history,self.manual)
        return (self.players[self.next_player].name, action)

    # contains the move progression logic
    # errors? if the move is inappropriate, and triggers the relevant checks
    # if there was a DOUBT
    def process_last_action(self):
        ult_player,ult_action = self.game_history[-1]
        print(ult_player, ult_action)
        
        # verify legality of move
        # we don't need to check out of bounds stuff because those can
        # be call DOUBT on, the system is self-regulating

        if ult_action.action_type == 'DOUBT':
            if len(self.game_history) == 0:
                raise ValueError
            else:
                penult_player, penult_action = self.game_history[-2]
                showdown_res = self.showdown(penult_action,
                               doubter=ult_player,
                               defendant=penult_player)
                util.display_showdown_result(showdown_res)
                sys.exit(0)
        
        # Rule checks below!
        # =========================================
        # we have certain checks for the very first move
        if len(self.game_history) == 1:
            # TODO: need to refactor whole system, and include a flag
            #       as to whether ones had been used before in the game
            if ult_action.incl_one:
                if not ult_action.count >= self.total_players * 2:
                    raise ValueError("Can't open with incl bid of count below {} in a {} person game!"\
                            .format(self.total_players * 2, self.total_players))
            else:
                if not ult_action.count >= (self.total_players * 2) - 1:
                    raise ValueError("Can't open with excl bid of count below {} in a {} person game!"\
                            .format(self.total_players * 2 - 1, self.total_players))

                    

        # and other relevant checks thereafter
        elif len(self.game_history) > 1:
            # TODO
            pass
    
    # return a dictionary declaring the result
    def showdown(self, penult_bid, doubter=None, defendant=None):
        hands_value_total = self.get_game_value(penult_bid.rank, penult_bid.incl_one)

        if penult_bid.count  >= hands_value_total:
            # if the count equals or exceeds the total, then the
            # defendant is correct, and the doubter is wrong
            winner = defendant
            loser = doubter
            challenge_succeeded = False
        else:
            # if the count is less than the total, then the challenge succeeded
            # and the doubter is correct, and the defendant is wrong
            winner = doubter
            loser = defendant
            challenge_succeeded = True

        return {'winner':winner,
                'loser':loser,
                'doubter':doubter,
                'defendant':defendant,
                'challenge_succeeded':challenge_succeeded,
                # offset is the true count minus last bid count
                'hands_value_total':hands_value_total,
                'penult_bid':penult_bid,
                'offset':hands_value_total - penult_bid.count}


    # get information of all hands
    def get_all_hands(self):
        return [(p.name, p.get_hand()) for p in self.players]
    
    def display_all_hands(self):
        print('======> Player Hands <======')
        hands = self.get_all_hands()
        for h in hands:
            print('> {}: {}'.format(h[0], h[1]))

    def get_game_value(self, rank, incl_one):
        return sum([p.get_hand_value(rank, incl_one) for p in self.players])
        
    # alternate the next_player between 0 and 1
    def rotate_player(self):
        self.next_player = (self.next_player + 1) % self.total_players


def main():
    g = Game(2, manual=True)
    g.display_all_hands()

    g.game_loop()



if __name__=="__main__":
    main()
