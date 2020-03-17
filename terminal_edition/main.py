import constraints as cs
import PvAI as PvAI_mode
import PvP as PvP_mode

if __name__ == "__main__":

    while True:

        print("--> Welcome to Nine Men's Morris Game <--")

        board = [cs.empty_marker for x in range(24)]
        participating_mills = cs.getParticipatingMills()

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
                'X': set(),
                'O': set()
            }

        while True:
            print("-> Press '1' to enter Player vs Player mode, or '2' to enter player vs AI mode..")
            option = input()
            if option == '1' or option == '2':
                break

        if option == '1':
            PvP_mode.startGame(board, participating_mills, men_placed, men_remaining, made_mills_indexes)
        else:
            PvAI_mode.startGame(board, participating_mills, men_placed, men_remaining, made_mills_indexes)

        print("-> Press any key to exit, or '1' to play again..")
        option = input()
        if option != '1':
            break


