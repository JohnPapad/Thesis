from game_nmm.nmm import constraints as cs
import math


# counting men
def easy_heuristic(board, placement_phase, player_turn, AI_marker, made_mills_indexes, men_remaining, participating_mills):
    my_markers = 0
    rival_markers = 0
    for spot in board:
        if spot == player_turn:
            my_markers += 1
        elif spot != cs.empty_marker:
            rival_markers += 1
    
    evaluation = 100 * (my_markers - rival_markers) + 10 * my_markers

    if player_turn == AI_marker: # human (min player) has just played
        return evaluation
    else: # AI (max player) has just played
        return -evaluation


# counting men and level of mens' freedom
def normal_heuristic(board, placement_phase, player_turn, AI_marker, made_mills_indexes, men_remaining, participating_mills):
    # count rival's available moves 
    _, movable_men_available_moves = cs.getPlayerMovableMenCoords(board, cs.getOpponent(player_turn))
    AM_counter = 0 
    for man_moves in movable_men_available_moves:
        AM_counter += len(man_moves)

    # then count human's and AI's men
    my_markers = 0
    rival_markers = 0
    for spot in board:
        if spot == player_turn:
            my_markers += 1
        elif spot != cs.empty_marker:
            rival_markers += 1

    evaluation = 0
    if AM_counter == 0: # game over condition: opponent does not have any valid move to make and therefore he lost
        evaluation = math.inf
    else:
        evaluation = 150 * my_markers - 100 * rival_markers + 500/AM_counter

    if player_turn == AI_marker: # human (min player) has just played
        return evaluation
    else: # AI (max player) has just played
        return -evaluation


def hard_heuristic(board, placement_phase, player_turn, AI_marker, made_mills_indexes, men_remaining, participating_mills):

    if placement_phase:
        evaluation = placement_phase_hard_heuristic(board, player_turn, made_mills_indexes, men_remaining,participating_mills)
    else:
        evaluation = movement_phase_hard_heuristic(board, player_turn, made_mills_indexes, men_remaining,participating_mills)
    
    if player_turn == AI_marker: # human (min player) has just played
        return evaluation
    else: # AI (max player) has just played
        return -evaluation


def placement_phase_hard_heuristic(board, player_turn, made_mills_indexes, men_remaining, participating_mills):
    # weights 
    p_w = 1  

    normal_threats_diff_weight = 7 * p_w   
    double_threats_diff_weight = 15 * p_w  
    mills_diff_weight = 26 * p_w           
    blocked_men_diff_weight = 4 * p_w      
    men_diff_weight = 10 * p_w             
    
    # getting game state's props
    normal_threats = {}
    double_threats_count = cs.getAllForcedSpots(board, -1, player_turn, participating_mills, normal_threats)
    normal_threats_count = len(normal_threats)

    opp_normal_threats = {}
    opp_double_threats_count = cs.getAllForcedSpots(board, -1, cs.getOpponent(player_turn), participating_mills, opp_normal_threats)
    opp_normal_threats_count = len(opp_normal_threats)

    made_mills_count = len(made_mills_indexes[player_turn])
    opp_made_mills_count = len(made_mills_indexes[cs.getOpponent(player_turn)])

    blocked_men = len(cs.getPlayerBlockedMenCoords(board, player_turn))
    opp_blocked_men = len(cs.getPlayerBlockedMenCoords(board, cs.getOpponent(player_turn)))

    # evaluating game state
    evaluation = 0
    
    normal_threats_diff = normal_threats_count - opp_normal_threats_count
    evaluation += normal_threats_diff * normal_threats_diff_weight
      
    double_threats_diff = double_threats_count - opp_double_threats_count
    evaluation += double_threats_diff * double_threats_diff_weight
    
    mills_diff = made_mills_count - opp_made_mills_count
    evaluation += mills_diff * mills_diff_weight
    
    blocked_men_diff = opp_blocked_men - blocked_men
    evaluation += blocked_men_diff * blocked_men_diff_weight

    men_diff = men_remaining[player_turn] - men_remaining[cs.getOpponent(player_turn)]
    evaluation += men_diff * men_diff_weight

    return evaluation
    

def movement_phase_hard_heuristic(board, player_turn, made_mills_indexes, men_remaining, participating_mills):
    # weights 
    p_w = 1

    mills_diff_weight = 20 * p_w              
    blocked_men_diff_weight = 10 * p_w        
    men_diff_weight = 50 * p_w                
    double_mills_weight = 40 * p_w           
    open_mills_diff_weight = 30 * p_w         

    # getting game state's props
    blocked_men = len(cs.getPlayerBlockedMenCoords(board, player_turn))
    
    opp_blocked_men = len(cs.getPlayerBlockedMenCoords(board, cs.getOpponent(player_turn)))
    if opp_blocked_men >= men_remaining[cs.getOpponent(player_turn)]: # game over condition
        return 1100  # opponent does not have any valid move to make and therefore he lost

    normal_threats = {}
    cs.getAllForcedSpots(board, -1, player_turn, participating_mills, normal_threats)

    opp_normal_threats = {}
    cs.getAllForcedSpots(board, -1, cs.getOpponent(player_turn), participating_mills, opp_normal_threats)

    made_mills_count = len(made_mills_indexes[player_turn])
    opp_made_mills_count = len(made_mills_indexes[cs.getOpponent(player_turn)])

    double_mills = cs.getDoubleMills(board, player_turn, participating_mills, made_mills_indexes[player_turn], normal_threats)
    opp_double_mills = cs.getDoubleMills(board, cs.getOpponent(player_turn), participating_mills, made_mills_indexes[cs.getOpponent(player_turn)], opp_normal_threats)

    open_mills, open_mills_blocked = cs.getOpenMills(board, player_turn, normal_threats)
    opp_open_mills, opp_open_mills_blocked = cs.getOpenMills(board, cs.getOpponent(player_turn), opp_normal_threats)
  
    # evaluating game state
    evaluation = 0
    
    mills_diff = made_mills_count - opp_made_mills_count
    evaluation += mills_diff * mills_diff_weight
    
    blocked_men_diff = opp_blocked_men - blocked_men
    evaluation += blocked_men_diff * blocked_men_diff_weight

    men_diff = men_remaining[player_turn] - men_remaining[cs.getOpponent(player_turn)]
    evaluation += men_diff * men_diff_weight

    if opp_open_mills > 0 or opp_open_mills_blocked > 0:
        evaluation -= open_mills_diff_weight
    elif open_mills > 0 or open_mills_blocked > 1:
        evaluation += open_mills_diff_weight
    elif open_mills_blocked == 1:
        evaluation -= open_mills_diff_weight 

    if opp_double_mills >= 0:
        evaluation -= double_mills_weight
    elif double_mills == 0 or double_mills > 1:
       evaluation += double_mills_weight

    return evaluation


# used by AI to find the best rival man to remove
def after_remove_heuristic(board, player_turn, coord, placement_phase, made_mills_indexes, men_remaining, participating_mills):

    if placement_phase: 
        return placement_phase_hard_heuristic(board, player_turn, made_mills_indexes, men_remaining,participating_mills)
    
    # weights 
    p_w = 1

    mills_diff_weight = 20 * p_w             
    blocked_men_diff_weight = 10 * p_w        
    men_diff_weight = 45 * p_w               
    double_mills_weight = 40 * p_w            
    double_mills_blocked_weight = 35 * p_w
    open_mills_diff_weight = 30 * p_w         
    open_mills_blocked_diff_weight = 16 * p_w

    # getting game state's props
    blocked_men = len(cs.getPlayerBlockedMenCoords(board, player_turn))
    opp_blocked_men = len(cs.getPlayerBlockedMenCoords(board, cs.getOpponent(player_turn)))
    
    normal_threats = {}
    cs.getAllForcedSpots(board, -1, player_turn, participating_mills, normal_threats)

    opp_normal_threats = {}
    cs.getAllForcedSpots(board, -1, cs.getOpponent(player_turn), participating_mills, opp_normal_threats)

    made_mills_count = len(made_mills_indexes[player_turn])
    opp_made_mills_count = len(made_mills_indexes[cs.getOpponent(player_turn)])

    double_mills = cs.getDoubleMills(board, player_turn, participating_mills, made_mills_indexes[player_turn], normal_threats)
    opp_double_mills = cs.getDoubleMills(board, cs.getOpponent(player_turn), participating_mills, made_mills_indexes[cs.getOpponent(player_turn)], opp_normal_threats)

    open_mills, open_mills_blocked = cs.getOpenMills(board, player_turn, normal_threats)
    opp_open_mills, opp_open_mills_blocked = cs.getOpenMills(board, cs.getOpponent(player_turn), opp_normal_threats)
  
    # evaluating game state
    evaluation = 0
    
    mills_diff = made_mills_count - opp_made_mills_count
    evaluation += mills_diff * mills_diff_weight
    
    blocked_men_diff = opp_blocked_men - blocked_men
    evaluation += blocked_men_diff * blocked_men_diff_weight

    men_diff = men_remaining[player_turn] - men_remaining[cs.getOpponent(player_turn)]
    evaluation += men_diff * men_diff_weight

    if open_mills > 1 and opp_open_mills > 1:
        open_mills_diff = open_mills - opp_open_mills
        evaluation += open_mills_diff * open_mills_diff_weight
    elif opp_open_mills == 1:
        evaluation -= open_mills_diff_weight
    elif open_mills == 1:
        evaluation += open_mills_diff_weight

    if open_mills_blocked > 1 and opp_open_mills_blocked > 1:
        open_mills_blocked_diff = open_mills_blocked - opp_open_mills_blocked
        evaluation += open_mills_blocked_diff * open_mills_blocked_diff_weight
    elif opp_open_mills_blocked == 1:
        evaluation -= open_mills_diff_weight
    elif open_mills_blocked == 1:
        evaluation -= open_mills_blocked_diff_weight  

    if opp_double_mills == 0 or opp_double_mills > 1:
        evaluation -= double_mills_weight
    elif opp_double_mills == 1:
        evaluation -= double_mills_blocked_weight
    elif double_mills == 0 or double_mills > 1:
       evaluation += double_mills_weight
    elif double_mills == 1:
        evaluation -= double_mills_blocked_weight

    return evaluation
