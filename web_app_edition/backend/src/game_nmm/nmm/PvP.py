from game_nmm.nmm import constraints as cs
from game_nmm.nmm.general import find_move 

from game_nmm import redis_management as rm

def Game(room_name,player_turn,new_board):

    board,all_men_placed,men_placed,men_remaining,made_mills_indexes,_,_,_=rm.get_board_info(room_name)
    participating_mills=cs.getParticipatingMills()
    empty_spots=[]

    type_m,coords = find_move(board,new_board)

    made_mills_indexes['X']=set(made_mills_indexes['X'])
    made_mills_indexes['O']=set(made_mills_indexes['O'])

    if type_m == "add":
        men_placed[player_turn] += 1
        if men_placed['X'] + men_placed['O'] == 18:
            all_men_placed = True

        mills_indexes = cs.getNewMadeMillsIndexes(new_board, coords[-1], participating_mills)
        if len(mills_indexes) != 0:#if new mill update and find removable coords
            made_mills_indexes[player_turn].update(mills_indexes)
            removable_men_coords = cs.getRemovableMenCoords(new_board, cs.getOpponentMillsIndexes(made_mills_indexes, player_turn), player_turn)
            if len(removable_men_coords) == 0:
                removable_men_coords = cs.getPlayerMenCoords(new_board,cs.getOpponent(player_turn))

            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,0,False,0)
            return "removingMan",player_turn , removable_men_coords, [],all_men_placed
        else: 
            player_turn=cs.getOpponent(player_turn)

            if not all_men_placed:
                empty_spots = cs.getEmptyPositions(new_board)
                rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,0,False,0)
                return "placingMan" ,player_turn , empty_spots,[],False
            else:
                movable_men_coords, movable_men_available_moves = cs.getPlayerMovableMenCoords(new_board, player_turn)
                rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,0,False,0)
                if len(movable_men_coords) == 0:
                    return "gameOver",cs.getOpponent(player_turn) , movable_men_coords ,movable_men_available_moves,False

                return "movingMan",player_turn , movable_men_coords ,movable_men_available_moves ,True

    elif type_m == "remove":
        men_remaining[cs.getOpponent(player_turn)] -= 1
        cs.updateMadeMills(made_mills_indexes[cs.getOpponent(player_turn)], coords[-1])

        if cs.getOpponentMenRemaining(men_remaining, player_turn) == 2:
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,0,False,0)
            return "gameOver",player_turn , [] ,[],False
            
        player_turn=cs.getOpponent(player_turn)
        if not all_men_placed:
            empty_spots = cs.getEmptyPositions(new_board)
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,0,False,0)
            return "placingMan" ,player_turn , empty_spots,[],False
        else:
            movable_men_coords, movable_men_available_moves = cs.getPlayerMovableMenCoords(new_board, player_turn)
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,0,False,0)
            if len(movable_men_coords) == 0:
                return "gameOver",cs.getOpponent(player_turn) , movable_men_coords ,movable_men_available_moves,False

            return "movingMan",player_turn , movable_men_coords ,movable_men_available_moves,False
    
    elif type_m == "move":
        cs.updateMadeMills(made_mills_indexes[player_turn], coords[0])
        mills_indexes = cs.getNewMadeMillsIndexes(new_board, coords[-1], participating_mills)
        if len(mills_indexes) != 0: #if new mill update and find removable coords
            made_mills_indexes[player_turn].update(mills_indexes)
            removable_men_coords = cs.getRemovableMenCoords(new_board, cs.getOpponentMillsIndexes(made_mills_indexes, player_turn), player_turn)
            if len(removable_men_coords) == 0:
                removable_men_coords = cs.getPlayerMenCoords(new_board,cs.getOpponent(player_turn))
            
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,0,False,0)            
            return "removingMan",player_turn , removable_men_coords, [],False
        else:
            player_turn=cs.getOpponent(player_turn)
            movable_men_coords, movable_men_available_moves = cs.getPlayerMovableMenCoords(new_board, player_turn)
            rm.update_board_info(room_name,new_board,all_men_placed,men_placed,men_remaining,made_mills_indexes,0,False,0)
            if len(movable_men_coords) == 0:
                return "gameOver",cs.getOpponent(player_turn) , movable_men_coords ,movable_men_available_moves,False
            return "movingMan",player_turn , movable_men_coords ,movable_men_available_moves,False
    
    else:
        return "wrong", "wrong", [] ,[] ,False
