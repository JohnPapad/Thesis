from game_nmm.nmm import constraints as cs
from game_nmm.nmm import AB_pruning as ABP
from game_nmm.nmm import heuristics as hs
from game_nmm.nmm import AI_utils 
from game_nmm.nmm import general 
from game_nmm.nmm.general import find_move 

from game_nmm import redis_management as rm
import math

ALPHA=-math.inf
BETA=math.inf


def make_first_move(room_name,MY_marker,difficulty):

    depth = 6
    board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,changeGamePhase,ref_coord=rm.get_board_info(room_name)
    new_board=board
    if difficulty=="easy":
        AI_heuristic = hs.easy_heuristic
    elif difficulty=="normal":
        AI_heuristic = hs.normal_heuristic
    else:
        AI_heuristic = hs.hard_heuristic

    participating_mills=cs.getParticipatingMills()
    made_mills_indexes['X']=set(made_mills_indexes['X'])
    made_mills_indexes['O']=set(made_mills_indexes['O'])
    AI_move = ABP.gameState()
    input_coord2=-2

    AI_marker='X'
  
    AI_move = ABP.alphaBetaPruning(new_board, depth, AI_marker, ALPHA, BETA, counter, AI_heuristic, AI_marker, participating_mills, made_mills_indexes, men_remaining,ref_coord)
    counter=1
    input_coord = AI_utils.AI_getCoordFromBoard1(new_board,AI_move.board)

    cs.placeMan(new_board, int(input_coord), AI_marker)

    men_placed[AI_marker] += 1
        
    move="triggerManMovement"
    empty_spots = cs.getEmptyPositions(new_board)
    rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,changeGamePhase,ref_coord)            
    return "placingMan" ,MY_marker ,empty_spots ,[] ,False ,move ,int(input_coord2) ,int(input_coord)

def Game(room_name,new_board,MY_marker,difficulty):

    depth = 0

    board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,changeGamePhase,ref_coord=rm.get_board_info(room_name)

    if difficulty=="easy":
        AI_heuristic = hs.easy_heuristic
        depth = 6
    elif difficulty=="normal":
        AI_heuristic = hs.normal_heuristic
        depth = 6
    else:
        AI_heuristic = hs.hard_heuristic
        depth = 6

    AI_marker = 'O'
    if MY_marker=='O':
        AI_marker = 'X'
    type_m,coords = find_move(board,new_board)
    if len(coords)>0:
        if type_m!="remove":
            ref_coord=int(coords[-1]) 
    new_ref_coord=ref_coord    
   
    participating_mills=cs.getParticipatingMills()
    empty_spots=[]

    made_mills_indexes['X']=set(made_mills_indexes['X'])
    made_mills_indexes['O']=set(made_mills_indexes['O'])

    input_coord2=-1
    input_coord=-1
    AI_move = ABP.gameState()
    player_move=False
    pr_all_men_placed=all_men_placed
    change=False

    if type_m == "add":
        men_placed[MY_marker] += 1
        counter += 1
        if men_placed['X'] + men_placed['O'] == 18:
            all_men_placed = True
            if pr_all_men_placed!=all_men_placed:
                change=True

        mills_indexes = cs.getNewMadeMillsIndexes(new_board, coords[-1], participating_mills)
        if len(mills_indexes) != 0:
            made_mills_indexes[MY_marker].update(mills_indexes)
            removable_men_coords = cs.getRemovableMenCoords(new_board, cs.getOpponentMillsIndexes(made_mills_indexes, MY_marker), MY_marker)
            if len(removable_men_coords) == 0:
                removable_men_coords = cs.getPlayerMenCoords(new_board,cs.getOpponent(MY_marker))

            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,change,new_ref_coord)
            return "removingMan" ,MY_marker ,removable_men_coords ,[] ,False ,'' ,-1 ,-1

    elif type_m == "remove":
        men_remaining[cs.getOpponent(MY_marker)] -= 1
        cs.updateMadeMills(made_mills_indexes[cs.getOpponent(MY_marker)], coords[-1])
        
        if cs.getOpponentMenRemaining(men_remaining, MY_marker) == 2:
            return "MYgameOver" ,MY_marker ,[] ,[] ,False ,'' ,-1 ,-1

    elif type_m == "move":
        cs.updateMadeMills(made_mills_indexes[MY_marker], coords[0])
        mills_indexes = cs.getNewMadeMillsIndexes(new_board, coords[-1], participating_mills)
        if len(mills_indexes) != 0:
            made_mills_indexes[MY_marker].update(mills_indexes)
            removable_men_coords = cs.getRemovableMenCoords(new_board, cs.getOpponentMillsIndexes(made_mills_indexes, MY_marker), MY_marker)
            if len(removable_men_coords) == 0:
                removable_men_coords = cs.getPlayerMenCoords(new_board,cs.getOpponent(MY_marker))
            
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,changeGamePhase,new_ref_coord) 
            return "removingMan" ,MY_marker ,removable_men_coords ,[] ,False ,'' ,-1 ,-1

    elif type_m == "no_move":
        pass
    else:
        return "wrong" ,"wrong" ,[] ,[] ,False ,'' ,-1 ,-1

    input_coord2=-1
    move=""
    if not type_m == "no_move":
        if not all_men_placed:
            AI_move = ABP.alphaBetaPruning(new_board, depth, AI_marker, ALPHA, BETA, counter, AI_heuristic, AI_marker, participating_mills, made_mills_indexes, men_remaining,ref_coord)
            counter += 1
            input_coord = AI_utils.AI_getCoordFromBoard1(new_board,AI_move.board)
            cs.placeMan(new_board, int(input_coord), AI_marker)
            men_placed[AI_marker] += 1
            if men_placed['X'] + men_placed['O'] == 18:
                all_men_placed = True
                if pr_all_men_placed!=all_men_placed:
                    change=True
            move="triggerManMovement"

        else:
            AI_movable_men_coords, _ = cs.getPlayerMovableMenCoords(new_board, AI_marker)
            if len(AI_movable_men_coords) == 0:
                return "MYgameOver" ,MY_marker ,[] ,[],False ,'' ,-1 ,-1
            
            AI_move = ABP.alphaBetaPruning(new_board, depth, AI_marker, ALPHA, BETA, 19, AI_heuristic, AI_marker, participating_mills, made_mills_indexes, men_remaining)
            input_coord2,input_coord = AI_utils.AI_getCoordFromBoard2(new_board,AI_move.board)#returns from,to coords
            cs.updateMadeMills(made_mills_indexes[AI_marker], int(input_coord2))
            cs.moveMan(new_board, int(input_coord2), int(input_coord))
            move="storeSourceDestCoord"

        mills_indexes = cs.getNewMadeMillsIndexes(new_board, int(input_coord), participating_mills)
        if len(mills_indexes) != 0:
            made_mills_indexes[AI_marker].update(mills_indexes)
            if changeGamePhase:
                change=True
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,change,new_ref_coord)
            return "nothing" ,AI_marker ,[] ,[] ,False ,move ,int(input_coord2) ,int(input_coord)
        else:
            player_move=True

    if type_m == "no_move":
        removable_men_coords = cs.getRemovableMenCoords(new_board, cs.getOpponentMillsIndexes(made_mills_indexes, AI_marker), AI_marker)
        if len(removable_men_coords) == 0:
            removable_men_coords = cs.getPlayerMenCoords(new_board,cs.getOpponent(AI_marker))

        input_coord = AI_utils.AI_remove_rival(new_board, AI_marker, not(all_men_placed), removable_men_coords,made_mills_indexes,men_remaining,participating_mills)
        cs.removeMan(new_board, int(input_coord), men_remaining)
        cs.updateMadeMills(made_mills_indexes[cs.getOpponent(AI_marker)], int(input_coord))

        rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,changeGamePhase,new_ref_coord)
        move="triggerRemovingManMovement"

        if cs.getOpponentMenRemaining(men_remaining, AI_marker) == 2:
            return "AIgameOver" ,AI_marker ,[] ,[] ,False ,move ,int(input_coord2) ,int(input_coord)
        else:
            player_move=True  

    if player_move:
        if not all_men_placed:
            empty_spots = cs.getEmptyPositions(new_board)
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,changeGamePhase,new_ref_coord)            
            return "placingMan" ,MY_marker ,empty_spots ,[] ,False ,move ,int(input_coord2) ,int(input_coord)

        else: 
            movable_men_coords, movable_men_available_moves = cs.getPlayerMovableMenCoords(new_board, MY_marker)
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,False,new_ref_coord)
            if len(movable_men_coords) == 0:
                return "AIgameOver" ,AI_marker ,[] ,[] ,False ,move ,int(input_coord2) ,int(input_coord)

            if change:
                changeGamePhase=True

            return "movingMan" ,MY_marker ,movable_men_coords ,movable_men_available_moves ,changeGamePhase ,move ,int(input_coord2) ,int(input_coord)
