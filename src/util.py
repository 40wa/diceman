import re

from engine import Action

# Ask for an input from stdin in format either <BID c f incl> or <DOUBT>
def get_move_from_stdin(player_name):
    ipt = input('Specify (' + player_name + ') move: ')

    bid_pattern = re.compile('[\s]*(BID|b|B)[\s]+([0-9])[\s]+([0-9])[\s]+(y|n)[\s]*')
    doubt_pattern = re.compile('[\s]*(DOUBT|d|D)[\s]*')
    
    bid_match = bid_pattern.match(ipt)
    doubt_match = doubt_pattern.match(ipt)
    
    if bid_match:
        count = bid_match[2]
        rank = bid_match[3]
        incl = True if (bid_match[4] == 'y') else False
        return Action.BID(count, rank, incl)
    elif doubt_match:
        return Action.DOUBT()
    else:
        get_move_from_stdin(player_name)
