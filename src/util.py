from engine import Action

import re

# Ask for an input from stdin in format either <BID c r incl> or <DOUBT>
def get_move_from_stdin(player_name):
    ipt = input('Specify (' + player_name + ') move: ')
    
    # accept BID or b or B, then c r incl
    bid_pattern = re.compile('[\s]*(BID|b|B)[\s]+([0-9])[\s]+([0-9])[\s]+(y|Y|n|N)[\s]*')
    # accept DUOBT or d or D
    doubt_pattern = re.compile('[\s]*(DOUBT|d|D)[\s]*')
    
    bid_match = bid_pattern.match(ipt)
    doubt_match = doubt_pattern.match(ipt)
    
    if bid_match:
        count = bid_match[2]
        rank = bid_match[3]
        incl = True if ((bid_match[4] == 'y') or (bid_match[4] == 'Y')) else False
        return Action.BID(count, rank, incl)
    elif doubt_match:
        return Action.DOUBT()
    else:
        return get_move_from_stdin(player_name)
