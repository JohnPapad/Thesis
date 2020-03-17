

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLUE = '\u001b[34m'
    CYAN = '\u001b[36m'
    YELLOW = '\u001b[33m'


def get_colored_spot(marker):
    if marker == 'X':
        return bcolors.BLUE + marker + bcolors.ENDC
    elif marker == 'O':
        return bcolors.CYAN + marker + bcolors.ENDC
    else:
        return marker


def printBoard(board):
    print(get_colored_spot(board[0]) + "(00)---------------------- " + get_colored_spot(
        board[1]) + "(01)---------------------- " + get_colored_spot(board[2]) + "(02)")
    print("|                           |                           |")
    print("|                           |                           |")
    print("|       " + get_colored_spot(board[8]) + "(08)-------------- " + get_colored_spot(
        board[9]) + "(09)-------------- " + get_colored_spot(board[10]) + "(10)   |")
    print("|       |                   |                   |       |")
    print("|       |                   |                   |       |")
    print("|       |         " + get_colored_spot(board[16]) + "(16)---- " + get_colored_spot(
        board[17]) + "(17)---- " + get_colored_spot(board[18]) + "(18)     |       |")
    print("|       |         |                   |         |       |")
    print("|       |         |                   |         |       |")
    print(get_colored_spot(board[3]) + "(03)-- " + get_colored_spot(board[11]) + "(11)---- " + get_colored_spot(
        board[19]) + "(19)               " + get_colored_spot(board[20]) + "(20)---- "
          + get_colored_spot(board[12]) + "(12)-- " + get_colored_spot(board[4]) + " (04)")
    print("|       |         |                   |         |       |")
    print("|       |         |                   |         |       |")
    print("|       |         " + get_colored_spot(board[21]) + "(21)---- " + get_colored_spot(
        board[22]) + "(22)---- " + get_colored_spot(board[23]) + "(23)     |       |")
    print("|       |                   |                   |       |")
    print("|       |                   |                   |       |")
    print("|       " + get_colored_spot(board[13]) + "(13)-------------- " + get_colored_spot(
        board[14]) + "(14)-------------- " + get_colored_spot(board[15]) + "(15)   |")
    print("|                           |                           |")
    print("|                           |                           |")
    print(get_colored_spot(board[5]) + "(05)---------------------- " + get_colored_spot(
        board[6]) + "(06)---------------------- " + get_colored_spot(board[7]) + "(07)")

