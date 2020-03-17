import constraints as cs
import visualization as vs
from random import randint


def startGame(board, participating_mills, men_placed, men_remaining, made_mills_indexes):
    all_men_placed = False
    player_turn = 'X'

    print("--> You entered Player vs Player mode <--")
    print("-> Player 'X' always plays first. There will be a coin toss. Please choose heads or tails.")
    coin_res = randint(0, 1)
    if coin_res == 0:
        print("-> Coin toss result: HEADS")
    else:
        print("-> Coin toss result: TAILS")

    print("--> GAME STARTS <--", end='\n\n')

    while True:

        print("////////////////////////////////////////")
        vs.printBoard(board)
        print("========================================")
        print("-> Player turn: ", player_turn, end='\n\n')

        if not all_men_placed:  #placement phase
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
                break

            cs.placeMan(board, int(input_coord), player_turn)

            men_placed[player_turn] += 1
            if men_placed['X'] + men_placed['O'] == 18:
                all_men_placed = True

        else: #movement phase
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

            vs.printBoard(board)
            print("========================================")

            all_rival_men_in_mills = False
            removable_men_coords = cs.getRemovableMenCoords(board, cs.getOpponentMillsIndexes(made_mills_indexes, player_turn), player_turn)
            if removable_men_coords == []: #all rival men in mills
                all_rival_men_in_mills = True
                removable_men_coords = cs.getPlayerMenCoords(board, cs.getOpponent(player_turn))

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

