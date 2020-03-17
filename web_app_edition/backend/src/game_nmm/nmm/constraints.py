from orderedset import OrderedSet

empty_marker = "#"

# every spot's possible neighbors coordinates // left, up, right, down // -1: no neighbor
neighbors = \
    [
		[-1, -1, 1, 3],  # 0
		[0, -1, 2, 9],  # 1
		[1, -1, -1, 4],  # 2
		[-1, 0, 11, 5],  # 3
		[12, 2, -1, 7],  # 4
		[-1, 3, 6, -1],  # 5
		[5, 14, 7, -1],  # 6
		[6, 4, -1, -1],  # 7
		[-1, -1, 9, 11],  # 8
		[8, 1, 10, 17],  # 9
		[9, -1, -1, 12],  # 10
		[3, 8, 19, 13],  # 11
		[20, 10, 4, 15],  # 12
		[-1, 11, 14, -1],  # 13
		[13, 22, 15, 6],  # 14
		[14, 12, -1, -1],  # 15
		[-1, -1, 17, 19],  # 16
		[16, 9, 18, -1],  # 17
		[17, -1, -1, 20],  # 18
		[11, 16, -1, 21],  # 19
		[-1, 18, 12, 23],  # 20
		[-1, 19, 22, -1],  # 21
		[21, -1, 23, 14],  # 22
		[22, 20, -1, -1]  # 23
    ]


# every spot's possible neighbors coordinates without the '-1'
possible_neighbors = \
    [
		[1, 3],  # 0
		[0, 2, 9],  # 1
		[1, 4],  # 2
		[0, 11, 5],  # 3
		[12, 2, 7],  # 4
		[3, 6],  # 5
		[5, 14, 7],  # 6
		[6, 4],  # 7
		[9, 11],  # 8
		[8, 1, 10, 17],  # 9
		[9, 12],  # 10
		[3, 8, 19, 13],  # 11
		[20, 10, 4, 15],  # 12
		[11, 14],  # 13
		[13, 22, 15, 6],  # 14
		[14, 12],  # 15
		[17, 19],  # 16
		[16, 9, 18],  # 17
		[17, 20],  # 18
		[11, 16, 21],  # 19
		[18, 12, 23],  # 20
		[19, 22],  # 21
		[21, 23, 14],  # 22
		[22, 20]  # 23
    ]


# left, up, right, down
moves =	\
    {
        "L": 0,
        "U": 1,
        "R": 2,
        "D": 3
    }


# all mills' formations that can be formed in a nine men's morris game
possible_mills = \
    [  # total: 16
        [0, 1, 2],  # 0
        [8, 9, 10],  # 1
        [16, 17, 18],  # 2
        [3, 11, 19],  # 3
        [20, 12, 4],  # 4
        [21, 22, 23],  # 5
        [13, 14, 15],  # 6
        [5, 6, 7],  # 7
        [0, 3, 5],  # 8
        [8, 11, 13],  # 9
        [16, 19, 21],  # 10
        [1, 9, 17],  # 11
        [22, 14, 6],  # 12
        [18, 20, 23],  # 13
        [10, 12, 15],  # 14
        [2, 4, 7]  # 15
    ]


# all board spots which are part of the same board "square" for each board spot
same_square_spots = \
    [
        # outer square
        [4, 6, 7, 2, 5, 1, 3],  # 0
		[3, 4, 6, 5, 7, 0, 2],  # 1
		[3, 6, 5, 0, 7, 1, 4],  # 2
		[1, 6, 4, 2, 7, 0, 5],  # 3
		[1, 6, 3, 0, 5, 2, 7],  # 4
		[1, 4, 2, 0, 7, 3, 6],  # 5
		[3, 4, 1, 0, 2, 5, 7],  # 6
		[1, 3, 0, 2, 5, 4, 6],  # 7

        # middle square
		[12, 14, 15, 10, 13, 9, 11],  # 8
		[11, 12, 14, 13, 15, 8, 10],  # 9
		[11, 14, 13, 8, 15, 9, 12],   # 10
		[9, 14, 12, 10, 15, 8, 13],   # 11
		[9, 14, 11, 8, 13, 10, 15],   # 12
		[9, 12, 10, 8, 15, 11, 14],   # 13
		[11, 12, 9, 8, 10, 13, 15],   # 14
		[9, 11, 8, 10, 13, 12, 14],   # 15

        # inner square
		[20, 22, 23, 18, 21, 17, 19], # 16
		[19, 20, 22, 21, 23, 16, 18], # 17
		[19, 22, 21, 16, 23, 17, 20], # 18
		[17, 22, 20, 18, 23, 16, 21], # 19
		[17, 22, 19, 16, 21, 18, 23], # 20
		[17, 20, 18, 16, 23, 19, 22], # 21
		[19, 20, 17, 16, 18, 21, 23], # 22
		[17, 19, 16, 18, 21, 20, 22]  # 23
    ]


look_up_spots = \
    [
         # outer square
        [7, 4, 6, 2, 5, 1, 3],  # 0
		[5, 7, 3, 4, 6, 0, 2, 9, 17],  # 1
		[5, 3, 6, 0, 7, 1, 4],  # 2
		[2, 7, 1, 6, 4, 0, 5, 11, 19],  # 3
		[0, 5, 1, 6, 3, 2, 7, 12, 20],  # 4
		[2, 1, 4, 0, 7, 3, 6],  # 5
		[0, 2, 3, 4, 1, 5, 7, 14, 22],  # 6
		[0, 1, 3, 2, 5, 4, 6],  # 7

        # middle square
		[15, 12, 14, 10, 13, 9, 11],  # 8
		[13, 15, 11, 12, 14, 8, 10, 1, 17],  # 9
		[13, 11, 14, 8, 15, 9, 12],   # 10
		[10, 15, 9, 14, 12, 8, 13, 3, 19],   # 11
		[8, 13, 9, 14, 11, 10, 15, 4, 20],   # 12
		[10, 9, 12, 8, 15, 11, 14],   # 13
		[8, 10, 11, 12, 9, 13, 15, 6, 22],   # 14
		[8, 9, 11, 10, 13, 12, 14],   # 15

        # inner square
		[23, 20, 22, 18, 21, 17, 19], # 16
		[21, 23, 19, 20, 22, 16, 18, 1, 9], # 17
		[21, 19, 22, 16, 23, 17, 20], # 18
		[18, 23, 17, 22, 20, 16, 21, 3, 11], # 19
		[16, 21, 17, 22, 19, 18, 23, 4, 12], # 20
		[18, 17, 20, 16, 23, 19, 22], # 21
		[16, 18, 19, 20, 17, 21, 23, 6, 14], # 22
		[16, 17, 19, 18, 21, 20, 22]  # 23
    ]


outer_square_coords = [1, 3, 4, 6, 0, 2, 5, 7]
middle_square_coords = [9, 11, 12, 14, 8, 10, 13, 15]
inner_square_coords = [17, 19, 20, 22, 16, 18, 21, 23]


def getOpponent(player_turn):
    if player_turn == 'X':
        return 'O'
    return 'X'

def getOpponentMenRemaining(men_remaining, player_turn):
    if player_turn == "X":
        return men_remaining['O']
    else:
        return men_remaining['X']


# returns a list of mills' indexes in which each spot can be part of.
# mills' indexes range form 0 to 15
def getParticipatingMills():
    participating_mills = [[-1 for x in range(2)] for y in range(24)]
    for coord in range(24):
        mills_counter = 0
        for i_mill, mill in enumerate(possible_mills):
            if coord in mill:
                participating_mills[coord][mills_counter] = i_mill
                mills_counter += 1
                if mills_counter == 2:
                    break
    return participating_mills


# Parameter 'forced_spots' is a dict with key a spot's coordinate in which a mill can be formed in the next move (based on a placed man)
# and value a set of the corresponding possible mills' indexes. 
# New forced spots are added in the dict.
# If two forced spots are detected (e.g. a double threat) then True is returned; False otherwise
def getForcedSpot(board, coord, participating_mills, forced_spots):
    forced_spots_count = 0 
    for mill_index in participating_mills[coord]:
        possible_mill_coords = possible_mills[mill_index]
        poss_forced_spot = -1
        empty_spots_counter = 0

        for poss_mill_coord in possible_mill_coords:
            if poss_mill_coord == coord:
                continue
            if isEmptyPosition(board, poss_mill_coord):
                empty_spots_counter += 1
                poss_forced_spot = poss_mill_coord
                if empty_spots_counter > 1:
                    poss_forced_spot = -1
                    break
            elif board[coord] != board[poss_mill_coord]:
                poss_forced_spot = -1
                break

        if poss_forced_spot != -1:
            forced_spots_count += 1
            if poss_forced_spot in forced_spots:
                forced_spots[poss_forced_spot].add(mill_index)
            else:
                forced_spots[poss_forced_spot] = set([mill_index])

    return forced_spots_count == 2


# Stores forced spots to a dict passed as parameter
# Returns the number of double threats detected.
def getAllForcedSpots(board, n_coord, player_marker, participating_mills, forced_spots):
    double_threat_count = 0
    for coord in range(24):
        if coord == n_coord:
            continue
        if board[coord] == player_marker:
            if getForcedSpot(board, coord, participating_mills, forced_spots):
                double_threat_count += 1
    return double_threat_count


def getCrossedMillsThreats(forced_spots):
    count = 0
    for _, mills_set in forced_spots.items():
        if len(mills_set) == 2:
            count += 1
    return count


# returns 0 if a double mill is detected or the number of blocked possible double mills (if a proper one is not detected);
# -1 otherwise
def getDoubleMills(board, player_marker, participating_mills, made_mills_indexes, forced_spots):
    canBeBlockedCount = 0
    for spot_coord, mills_set in forced_spots.items():
        for mill_i in mills_set:
            crossing_mill_i = participating_mills[spot_coord][0] if participating_mills[spot_coord][1] == mill_i else participating_mills[spot_coord][1]
            crossing_mill = possible_mills[crossing_mill_i]

            doubleMillFormed = False
            for crossing_mill_coord in crossing_mill:
                if board[crossing_mill_coord] == player_marker and crossing_mill_coord in possible_neighbors[spot_coord]:
                    for made_mill_i in made_mills_indexes:
                        if crossing_mill_coord in possible_mills[made_mill_i]:
                            doubleMillFormed = True
                            break

            if not doubleMillFormed:
                continue
            
            opponentCanBlock = False
            for crossing_mill_coord in crossing_mill:
                if board[crossing_mill_coord] == getOpponent(player_marker) and crossing_mill_coord in possible_neighbors[spot_coord]:
                    opponentCanBlock = True

            if doubleMillFormed and not opponentCanBlock:
                return 0
            elif doubleMillFormed and opponentCanBlock: 
                canBeBlockedCount += 1
    
    if canBeBlockedCount == 0:
        return -1
    else:
        return canBeBlockedCount


def getDoubleMillsReport(number):
    if number == 0:
        return "FOUND"
    elif number == -1:
        return "NONE found"
    else: 
        return "None found but there are " + str(number) + " which can be blocked"


# returns the number of open mills and the number of possible open mills (e.g. which can be blocked by a rival man in one move)
def getOpenMills(board, player_marker, forced_spots):
    open_mills = 0
    open_mills_can_be_blocked = 0

    for spot_coord, mills_set in forced_spots.items():
        for mill_i in mills_set:
            mill_coords = possible_mills[mill_i]
            forced_spot_neighs = possible_neighbors[spot_coord]

            open_mill = False
            blocked_mill = False
            for neigh in forced_spot_neighs:
                if neigh not in mill_coords:
                    if board[neigh] == player_marker:
                        open_mill = True
                    elif board[neigh] == getOpponent(player_marker):
                        blocked_mill = True
            if open_mill:
                if blocked_mill:
                    open_mills_can_be_blocked += 1
                else:
                    open_mills += 1

    return open_mills, open_mills_can_be_blocked


# checks if a new mill has been formed
def isMillMade(board, coord, participating_mills):
    for mill_index in participating_mills[coord]:
        possible_mill = possible_mills[mill_index]
        if board[possible_mill[0]] == board[coord] \
            and board[possible_mill[1]] == board[coord] \
            and board[possible_mill[2]] == board[coord]:
                return True
    return False


# returns a list of mills' indexes that have just been formed
def getNewMadeMillsIndexes(board, coord, participating_mills):
    mills_indexes = set()
    for mill_index in participating_mills[coord]:
        possible_mill = possible_mills[mill_index]
        if board[possible_mill[0]] == board[coord] \
            and board[possible_mill[1]] == board[coord] \
            and board[possible_mill[2]] == board[coord]:
                mills_indexes.add(mill_index)
                if len(mills_indexes) == 2:
                    break
    return mills_indexes
    

# returns a list containing mills' indexes that are blocked (e.g. all three men that form the mill can not be moved)
def getBlockedMillsIndexes(board, made_mills_indexes):
    blockedMillsIndexes = []
    for mill_i in made_mills_indexes:
        blockedMill = True
        for mill_spot_coord in possible_mills[mill_i]:
            if len(getPossiblePositions(mill_spot_coord, board)) != 0:
                blockedMill = False
                break
        if blockedMill:
            blockedMillsIndexes.append(mill_i)
        
    return blockedMillsIndexes


# returns a list of spots' coordinates that contain rival men which can be removed (that are not part of a mill)
def getRemovableMenCoords(board, made_mills_indexes, player_marker):
    removable_men_coords = []

    for coord in range(24):
        if not isEmptyPosition(board, coord) and board[coord] != player_marker:
            if len(made_mills_indexes) != 0:
                abort_flag = False
                for mill_i in made_mills_indexes:
                    if coord in possible_mills[mill_i]:
                        abort_flag = True
                        break

                if abort_flag is False:
                    removable_men_coords.append(coord)
            else:
                removable_men_coords.append(coord)

    return removable_men_coords


# removes a broken mill's index from 'made mills' set
def updateMadeMills(made_mills_indexes, coord):
    tmp_mills_indexes = made_mills_indexes.copy()
    for mill_i in tmp_mills_indexes:
        if coord in possible_mills[mill_i]:
            made_mills_indexes.remove(mill_i)
    return


def getOpponentMillsIndexes(made_mills_indexes, player_marker):
    if player_marker == 'X':
        return made_mills_indexes['O']
    else:
        return made_mills_indexes['X']


def getEmptyPositions(board):
    empty_spots = []
    for coord in range(24):
        if isEmptyPosition(board, coord):
            empty_spots.append(coord)

    return empty_spots


def getPlayerMenCoords(board, player_marker):
    player_men_coords = []
    for coord in range(24):
        if board[coord] == player_marker:
            player_men_coords.append(coord)

    return player_men_coords


# return left, upper, right or lower neighbor's coord
def getNeighborCoord(coord, direction):
    return neighbors[coord][moves[direction]]


# returns a list with all coord's neighs
def getAllNeighborsCoord(coord):
    return possible_neighbors[coord]


def isEmptyPosition(board, coord):
    if board[coord] != empty_marker:
        return False
    return True

 
def placeMan(board, coord, player_marker):
    board[coord] = player_marker


def removeMan(board, coord, remaining_men = None):
    if remaining_men != None:
        remaining_men[board[coord]] -= 1
    board[coord] = empty_marker


def moveMan(board, coord_from, coord_to):
    board[coord_to] = board[coord_from]
    board[coord_from] = empty_marker


# checks if a man can be moved in a specific direction
def isValidMove(board, coord, move):
    neighbor_coord = getNeighborCoord(coord, move)
    if neighbor_coord == -1:
        return False
    if not isEmptyPosition(board, neighbor_coord):
        return False
    return True


# returns a list of spots' coordinates in which a man can be moved
def getPossiblePositions(coord, board):
    possible_poss = []
    for move in moves:
        if isValidMove(board, coord, move):
            possible_poss.append(getNeighborCoord(coord, move))
    return possible_poss


# returns a list of player's men coordinates that can be moved to at least one direction
# and also the available spots' coordinates in which each movable man can be moved to
def getPlayerMovableMenCoords(board, player_turn):
    player_men_coords = getPlayerMenCoords(board, player_turn)
    movable_men_coords = []
    movable_men_available_moves = []
    for coord in player_men_coords:
        poss_spots = getPossiblePositions(coord, board)
        if len(poss_spots) != 0:
            movable_men_coords.append(coord)
            movable_men_available_moves.append(poss_spots)

    return [movable_men_coords, movable_men_available_moves]


# returns the number of game states that can be generated from the current state by a move
def getPossGenStates(movable_men_available_moves):
    count = 0
    for available_moves in movable_men_available_moves:
        count += len(available_moves)

    return count
    

# returns a list of player's men coordinates that are blocked (that they can not be moved to any direction)
def getPlayerBlockedMenCoords(board, player_turn):
    player_men_coords = getPlayerMenCoords(board, player_turn)
    movable_men_coords, _ = getPlayerMovableMenCoords(board, player_turn)

    blocked_men_coords = []
    for coord in player_men_coords:
        if coord not in movable_men_coords:
            blocked_men_coords.append(coord)

    return blocked_men_coords


# returns a list of all possible new boards that can be formed in a specific game state in the placement phase
def getAllPossibleNewBoards1(board, player_turn, participating_mills = None, ref_coord = None):
    empty_spots = getEmptyPositions(board)
    new_boards = []
    new_boards_coords = []

    if ref_coord != None:
        empty_spots = getOrderedEmptySpots(board, ref_coord, empty_spots, participating_mills)

    for coord in empty_spots:
        new_board = board.copy()
        placeMan(new_board, coord, player_turn)
        new_boards.append(new_board)
        new_boards_coords.append([coord]) 

    return [new_boards, new_boards_coords]


# get empty spots in an "appropriate" order (which will help in more efficiet pruning)
def getOrderedEmptySpots(board, ref_coord, empty_spots, participating_mills):
    ordered_empty_spots = OrderedSet()

    for coord in look_up_spots[ref_coord]:
        if board[coord] == empty_marker:
            ordered_empty_spots.add(coord)

    if ref_coord in outer_square_coords:
        ordered_empty_spots.update(empty_spots)
    elif ref_coord in inner_square_coords:
        empty_spots.sort(reverse=True)
        ordered_empty_spots.update(empty_spots)
    else:
        ordered_empty_spots.update(empty_spots)
     
    return ordered_empty_spots


# returns a list of all possible new boards that can be formed in a specific game state in the movement phase
def getAllPossibleNewBoards2(board, player_turn):
    movable_men_coords, movable_men_available_moves = getPlayerMovableMenCoords(board, player_turn)
    new_boards = []
    new_boards_coords = []

    for i, coord_list in enumerate(movable_men_available_moves):
        for coord in coord_list:
            new_board = board.copy()
            moveMan(new_board, movable_men_coords[i], coord)
            new_boards.append(new_board)
            new_boards_coords.append([movable_men_coords[i], coord])

    return [new_boards, new_boards_coords]


def getForcedMill(coord1, coord2, participating_mills):
    mills1 = participating_mills[coord1]
    mills2 = participating_mills[coord2]

    for m in mills1:
        if m in mills2:
            return possible_mills[m]


def myDeepcopyMadeMillsIndexesDict(dict1):
    dict2 = \
        {
            'X' : dict1['X'].copy() ,
            'O' : dict1['O'].copy()
        }
    return dict2

