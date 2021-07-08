from engine import Action

import re

# Ask for an input from stdin in format either <BID c r incl> or <DOUBT>
def get_move_from_stdin(player_name):
    ipt = input('Specify (' + player_name + ') move: ')
    
    # accept BID or b or B, then c r incl
    bid_pattern = re.compile('[\s]*(BID|b|B)[\s]+([0-9])[\s]+([0-9])[\s]+(y|Y|n|N)[\s]*')
    # accept DOUBT or d or D
    # or press X to doubt
    doubt_pattern = re.compile('[\s]*(DOUBT|d|D|X)[\s]*')
    
    bid_match = bid_pattern.match(ipt)
    doubt_match = doubt_pattern.match(ipt)
    
    if bid_match:
        #I think these were strings, they're now ints
        count = int(bid_match[2])
        rank = int(bid_match[3])
        incl = True if ((bid_match[4] == 'y') or (bid_match[4] == 'Y')) else False
        return Action.BID(count, rank, incl)
    elif doubt_match:
        return Action.DOUBT()
    else:
        return get_move_from_stdin(player_name)

def request_doubts(player_name, players):
    #input should be either empty string, player index, or player name
    ipt = input('Specify player to doubt {}: '.format(player_name))
    if ipt == "":
        #no one doubts
        return None
    if ipt.isnumeric():
        doubt_player = int(ipt)
        #check if valid player index
        if doubt_player >= len(players):
            #no, try again
            request_doubts(player_name,players)
        else:
            #else this is a real player
            if players[doubt_player].name == player_name:
                print("you can't doubt yourself")
                request_doubts(player_name,players)
            else:
                return doubt_player
    #otherwise input is a player's name
    for i in range(len(players)):
        #check if this is the real name of a player other than yourself
        if ipt == players[i].name:
            if ipt != player_name:
                return i
    request_doubts(player_name,players)
    