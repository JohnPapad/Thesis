from constraints import empty_marker
from constraints import getOpponent
from heuristics import after_remove_heuristic
import math

# decides which rival man will be removed by the AI
def AI_remove_rival(board, player_turn, placement_phase, removable_men_coords, made_mills_indexes, men_remaining, participating_mills, all_rival_men_in_mills):
    rival_marker = getOpponent(player_turn)
    rival_to_remove = None
    max_eval = -math.inf

    for rm_coord in removable_men_coords: # max 9 reps
        board[rm_coord] = empty_marker # remove rival man
        rem_eval = after_remove_heuristic(board, player_turn, rm_coord, placement_phase, made_mills_indexes, men_remaining, participating_mills) #evaluate new board
        
        if rem_eval > max_eval: # keep best evaluation and board coord to remove
            max_eval = rem_eval
            rival_to_remove = rm_coord

        board[rm_coord] = rival_marker # put back the previously removed rival man 

    return rival_to_remove

# extract the board coord in which a man was placed, by comparing previous and new board in placement phase
def AI_getCoordFromBoard1(board, board2):
    for i in range(24):
        if board[i] != board2[i]:
            return i

# extract the board coord in which a man was moved from, as well as the board coord in which the man was moved to, by comparing previous and new board in movement phase
def AI_getCoordFromBoard2(board, board2):
    for i in range(24):
        if board[i] != board2[i]:
            if board[i] == empty_marker:
                to_coord = i
            else:
                from_coord = i
    return from_coord,to_coord
