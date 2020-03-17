empty_board=['#']*24

all_men_placed=False

player_turn='X'

forced_spots=[]

men_placed = \
{
    'X': 0,
    'O': 0
}

men_remaining = \
{
    'X': 9,
    'O': 9
}

made_mills_indexes = \
{
    'X': [],
    'O': []
}

counter=0

changeGamePhase=False

ref_coord=9