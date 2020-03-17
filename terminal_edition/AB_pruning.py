import constraints as cs
import AI_utils
import math

class gameState():

    def __init__(self):
        self.evaluation = 0
        self.board = []


def alphaBetaPruning(board, depth, player_turn, alpha, beta, moves_counter, heuristic, AI_marker, participating_mills, made_mills_indexes, men_remaining, ref_coord = None):
    final_evaluation = gameState()

    # opponent has just played
    if moves_counter < 18: # placement phase
        all_poss_new_boards, all_poss_new_boards_coords = cs.getAllPossibleNewBoards1(board, player_turn, participating_mills, ref_coord)
    else: # movement phase  
        if men_remaining[player_turn] < 3: # game over condition
            if player_turn == AI_marker: # if player has just played (now it is AI' turn) and AI has only 2 men left then it lost
                final_evaluation.evaluation = -1100 - depth * 10
            else: # if AI has just played (now it is player's turn) and player has only 2 men left then he lost
                final_evaluation.evaluation = 1100 + depth * 10
            return final_evaluation

        all_poss_new_boards, all_poss_new_boards_coords = cs.getAllPossibleNewBoards2(board, player_turn)
        if len(all_poss_new_boards) == 0: # game over condition - no valid moves available
            if player_turn == AI_marker: # if player has just played (now it is AI' turn) and AI does not have any valid moves to make then it lost
                final_evaluation.evaluation = -1100 - depth * 10
            else: # if AI has just played (now it is player' turn) and player does not have any valid moves to make then he lost
                final_evaluation.evaluation = 1100 + depth * 10
            return final_evaluation
        else:
            final_evaluation.board = all_poss_new_boards[0]

    if depth == 0:
        final_evaluation.evaluation = heuristic(board, moves_counter < 16, player_turn, AI_marker, made_mills_indexes, men_remaining, participating_mills)
    else: 
        for poss_board_i, poss_board in enumerate(all_poss_new_boards): # every poss_board is a copy of the previous board

            made_mills_indexes_copy = cs.myDeepcopyMadeMillsIndexesDict(made_mills_indexes)
            men_remaining_copy = men_remaining.copy()
            poss_board_copy = poss_board.copy()

            orig_dest_coords = all_poss_new_boards_coords[poss_board_i]
            dest_coord = None
            if len(orig_dest_coords) == 1: # placement phase 
                dest_coord = orig_dest_coords[0] # there is only the destination board coord
            elif len(orig_dest_coords) == 2: # movement phase
                orig_coord = orig_dest_coords[0] # there are both origin and destination board coords
                dest_coord = orig_dest_coords[1]
                cs.updateMadeMills(made_mills_indexes_copy[player_turn], orig_coord)

            new_mills = cs.getNewMadeMillsIndexes(poss_board, dest_coord, participating_mills) # poss_board will be used as read only in the function
            if len(new_mills) != 0:
                made_mills_indexes_copy[player_turn].update(new_mills)
                removable_men_coords = cs.getRemovableMenCoords(poss_board, cs.getOpponentMillsIndexes(made_mills_indexes_copy, player_turn), player_turn)
                all_rival_men_in_mills = False
                if removable_men_coords == []: # all rival men in mills
                    all_rival_men_in_mills = True
                    removable_men_coords = cs.getPlayerMenCoords(poss_board, cs.getOpponent(player_turn))
                
                men_remaining_copy[cs.getOpponent(player_turn)] -= 1
                coord_to_remove = AI_utils.AI_remove_rival(poss_board, player_turn, moves_counter < 16, removable_men_coords, made_mills_indexes_copy, men_remaining_copy, participating_mills, all_rival_men_in_mills)
                cs.removeMan(poss_board_copy, coord_to_remove)
                if all_rival_men_in_mills:
                    cs.updateMadeMills(made_mills_indexes_copy[cs.getOpponent(player_turn)], coord_to_remove)
                
            current_evaluation = alphaBetaPruning(poss_board_copy, depth - 1, cs.getOpponent(player_turn), alpha, beta, moves_counter + 1, heuristic, AI_marker, participating_mills, made_mills_indexes_copy, men_remaining_copy, ref_coord)

            if player_turn == AI_marker: # maximizer
                if current_evaluation.evaluation > alpha:
                    alpha = current_evaluation.evaluation
                    final_evaluation.board = poss_board
            else: # minimizer
                if current_evaluation.evaluation < beta:
                    beta = current_evaluation.evaluation
                    final_evaluation.board = poss_board

            if alpha >= beta:
                break

        if player_turn == AI_marker:
            final_evaluation.evaluation = alpha
        else:
            final_evaluation.evaluation = beta

    return final_evaluation

