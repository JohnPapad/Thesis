import constraints as cs
import visualization as vs
import AB_pruning as ABP
import heuristics as hs
import AI_utils
from random import randint
import time
import math

depth = 6
alpha = -math.inf #lower bound
beta = math.inf   #upper bound

def startGame(board, participating_mills, men_placed, men_remaining, made_mills_indexes):

    all_men_placed = False
    player_turn = 'X'

    while True:
        print("-> Press '1' for easy mode,'2' for normal mode,  '3' for hard mode..")
        option = input()
        if option == '1' or option == '2' or option == '3':
            break

    if option == '1':
        AI_heuristic = hs.easy_heuristic
    elif option == '2':
        AI_heuristic = hs.normal_heuristic
    else:
        AI_heuristic = hs.hard_heuristic

    print("--> You entered Player vs AI mode <--")
    print("-> Player 'X' always plays first. There will be a coin toss to be decided who will be player 'X'.")
    coin_res = randint(0, 1)
    if coin_res == 0:
        print("-> You will be player 'X' and play first")
        AI_marker = 'O'
    else:
        print("-> You will be player 'O' and play second")
        AI_marker = 'X'

    print("--> GAME STARTS <--", end='\n\n')
    counter = 0
    ref_coord = cs.middle_square_coords[randint(0, len(cs.middle_square_coords)-1)]
    while True:
        print("////////////////////////////////////////")
        vs.printBoard(board)
        print("========================================")

        if not all_men_placed:  # placement phase
            if player_turn != AI_marker:
                print("-> Placement phase:")
                print("-> 'X' player's remaining men to place: ", 9 - men_placed['X'])
                print("-> 'O' player's remaining men to place: ", 9 - men_placed['O'])
                print("========================================")

                empty_spots = cs.getEmptyPositions(board)

                while True:
                    print("-> Player '" + player_turn + "': Empty spots: ", end="")
                    print(empty_spots)
                    print("========================================")

                    print("-> Player '" + player_turn + "': Please enter a valid coordinate to place a man")
                    print("========================================")

                    input_coord = input()
                    if not input_coord.isnumeric() or int(input_coord) not in empty_spots:
                        print("-> Player '" + player_turn + "': WRONG MOVEMENT - Chosen spot is not empty, please try again..")
                        print("========================================")
                        continue
                    counter += 1 #player move done
                    ref_coord = int(input_coord)
                    break
            else:
                #AB PRUNING CALL
                print("-> AI is thinking...")
                start_time = time.time()
                AI_move = ABP.alphaBetaPruning(board, depth, AI_marker, alpha, beta, counter, AI_heuristic, AI_marker, participating_mills, made_mills_indexes, men_remaining, ref_coord)
                counter += 1 #ai move done
                input_coord = AI_utils.AI_getCoordFromBoard1(board, AI_move.board)
                end_time = time.time()

                elasped_time = end_time - start_time
                print("-> Player '" + player_turn + "': Placed a man at spot with coordinate: [" + str(input_coord) + "] in " + str(elasped_time) + " secs")
                print("========================================")

            cs.placeMan(board, int(input_coord), player_turn)
            men_placed[player_turn] += 1
            if men_placed['X'] + men_placed['O'] == 18:
                all_men_placed = True

        else:  # moving men phase
            if player_turn != AI_marker:
                print("-> Moving men phase:")
                print("-> 'X' player's remaining men: ", men_remaining['X'])
                print("-> 'O' player's remaining men: ", men_remaining['O'])
                print("========================================")

                movable_men_coords, movable_men_available_moves = cs.getPlayerMovableMenCoords(board, player_turn)
                if len(movable_men_coords) == 0:
                    print("--> GAME OVER <-- Player '" + player_turn + "' LOST !!")
                    print("========================================")
                    break

                print("-> Player '" + player_turn + "': Please enter a man's coordinate and the desired spot's coordinate in which it will be moved")
                while True:
                    print("-> Player's '" + player_turn + "' movable men coordinates: ", movable_men_coords)
                    print("========================================")
                    print("-> Player '" + player_turn + "': First enter your chosen man's coordinate")
                    print("========================================")

                    input_coord2 = input()
                    if not input_coord2.isnumeric() or int(input_coord2) not in movable_men_coords:
                        print("-> Player '" + player_turn + "': WRONG MOVEMENT - You chose invalid spot, please try again ..")
                        print("========================================")
                        continue
                    break

                poss_spots = movable_men_available_moves[movable_men_coords.index(int(input_coord2))]
                while True:
                    print("-> Player '" + player_turn + "': Available spots' coordinates for the chosen man: ", poss_spots)
                    print("========================================")
                    print("-> Player '" + player_turn + "': Now enter the spot's coordinate in which your chosen man will be moved")
                    print("========================================")

                    input_coord = input()
                    if not input_coord.isnumeric() or int(input_coord) not in poss_spots:
                        print("-> Player '" + player_turn + "': WRONG MOVEMENT - Your chosen man can not perform this move, please try again.. ")
                        print("========================================")
                        continue
                    break
            else: #AI turn here
                AI_movable_men_coords, _ = cs.getPlayerMovableMenCoords(board, player_turn)
                if len(AI_movable_men_coords) == 0:
                    print("--> GAME OVER <-- Player '" + player_turn + "' LOST !!")
                    print("========================================")
                    break

                #AB PRUNING CALL # as moves_counter here we could send 19 (it just has to be > 18 in order to indicate we are in movement phase)
                AI_move = ABP.alphaBetaPruning(board, depth, AI_marker, alpha, beta, 19, AI_heuristic, AI_marker, participating_mills, made_mills_indexes, men_remaining)
                input_coord2,input_coord = AI_utils.AI_getCoordFromBoard2(board, AI_move.board) # returns origin, destination board coord

                print("-> Player '" + player_turn + "': Moved man from spot with coordinate: [", input_coord2, "] to spot with coordinate: [", input_coord, "]")
                print("========================================")

            cs.updateMadeMills(made_mills_indexes[player_turn], int(input_coord2))
            cs.moveMan(board, int(input_coord2), int(input_coord))

        mills_indexes = cs.getNewMadeMillsIndexes(board, int(input_coord), participating_mills)
        if len(mills_indexes) != 0:
            made_mills_indexes[player_turn].update(mills_indexes)

            print("-> Player '" + player_turn + "' HAS MADE MILL(s):")
            for mill_i in mills_indexes:
                print(cs.possible_mills[mill_i])
            print("========================================")

            print("-> Player '" + player_turn + "' ALL MADE MILLS:")
            for mill_i in made_mills_indexes[player_turn]:
                print(cs.possible_mills[mill_i])
            print("========================================")

            if player_turn != AI_marker:
                vs.printBoard(board)
                print("========================================")

            all_rival_men_in_mills = False
            removable_men_coords = cs.getRemovableMenCoords(board, cs.getOpponentMillsIndexes(made_mills_indexes, player_turn), player_turn)
            if removable_men_coords == []: #all rival men in mills
                all_rival_men_in_mills = True
                removable_men_coords = cs.getPlayerMenCoords(board, cs.getOpponent(player_turn))

            if player_turn != AI_marker:
                while True:
                    print("-> Player '" + player_turn + "': Please remove a rival man that is not part of a mill")
                    print("========================================")
                    print("-> Player '" + player_turn + "': Removable rival men coordinates: ", removable_men_coords)
                    print("========================================")

                    input_coord2 = input()
                    if not input_coord2.isnumeric() or int(input_coord2) not in removable_men_coords:
                        print("-> Player '" + player_turn + "': WRONG MOVEMENT - You chose invalid spot, please try again ..")
                        print("========================================")
                        continue
                    break
            else: #ai call to remove a rival (assigns the rival man to be removed in input_coord2 var)
                input_coord2 = AI_utils.AI_remove_rival(board, AI_marker, not all_men_placed, removable_men_coords, made_mills_indexes, men_remaining, participating_mills, all_rival_men_in_mills)

            print("-> Player '" + player_turn + "' removed board coard: " + str(input_coord2))
            cs.removeMan(board, int(input_coord2), men_remaining)
            if cs.getOpponentMenRemaining(men_remaining, player_turn) == 2:
                print("--> GAME OVER <-- Player '" + player_turn + "' WON !!")
                break
            if all_rival_men_in_mills:
                cs.updateMadeMills(made_mills_indexes[cs.getOpponent(player_turn)], int(input_coord2))

        if player_turn == 'X': # change player's turn
            player_turn = 'O'
        else:
            player_turn = 'X'

