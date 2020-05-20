from copy import deepcopy
import math

board = []
vaild_move = []
game_finished = False
size = int(input("How big do you want the board to be? "))
bot_play = input("Do you want to play a bot? [Y/N] ")
search_depth = 3

if bot_play == 'Y':
    bot_play = True
else:
    bot_play = False


# assume it is 1
def diag_win():
    global game_finished
    same_diag = []
    opp_diag = []
    for i in range(0, size):
        same_diag.append(board[i][i])
        opp_diag.append(board[i][size - (1 + i)])
    same_start = same_diag[0]
    opp_start = opp_diag[0]
    for x in opp_diag:
        if x != opp_start or x == 0:
            return False
    for x in same_diag:
        if x != same_start or x == 0:
            return False
    game_finished = True


def vert_win():
    global game_finished
    verticals = []
    for i in range(0, size):
        current = []
        for j in range(0, size):
            current.append(board[i][j])
        verticals.append(current)

    for x in verticals:
        good_colm = True
        for i in range(0, size):
            if x[i] != x[0] or x[i] == 0:
                good_colm = False
        if good_colm:
            game_finished = True
            break


def horz_win():
    global game_finished
    horizontals = []
    for i in range(0, size):
        current = []
        for j in range(0, size):
            current.append(board[j][i])
        horizontals.append(current)

    for x in horizontals:
        good_row = True
        for i in range(0, size):
            if x[i] != x[0] or x[i] == 0:
                good_row = False
        if good_row:
            game_finished = True
            break


def check_game():
    diag_win()
    vert_win()
    horz_win()


def validate_moves():
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            if abs(board[x][y]) == 1:
                vaild_move[x][y] = False
            else:
                vaild_move[x][y] = True


def find_children():
    moves = []
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            if vaild_move[x][y]:
                moves.append((x, y))
    return moves


def bot_move():
    move = minimax(search_depth, True, board)
    column = move[1][0]
    row = move[1][1]
    board[column][row] = -1


def check_diagonal(current_board, column, row, current_state, x_o):
    currently_same = current_state[0]
    currently_opp = current_state[1]
    if column == row and current_state[0] == False:
        if x_o:
            currently_same = True
            for i in range(0, size):
                if current_board[i][i] == -1:
                    currently_same = False
        else:
            currently_same = True
            for i in range(0, size):
                if current_board[i][i] == 1:
                    currently_same = False
    if column == size - (row + 1) and current_state[1] == False:
        if x_o:
            currently_opp = True
            for i in range(0, size):
                if current_board[i][size - (i + 1)] == -1:
                    currently_opp = False
        else:
            currently_opp = True
            for i in range(0, size):
                if current_board[i][size - (i + 1)] == 1:
                    currently_opp = False
    return [currently_same, currently_opp]


def check_columns(current_board, column, current_state, x_o):
    if current_state[column]:
        return current_state
    if x_o:
        current_state[column] = True
        for i in range(0, size):
            if current_board[column][i] == -1:
                current_state[column] = False
    else:
        current_state[column] = True
        for i in range(0, size):
            if current_board[column][i] == 1:
                current_state[column] = False
    return current_state


def check_rows(current_board, column, row, current_state, x_o):
    if current_state[row]:
        return current_state
    if x_o:
        current_state[row] = True
        for i in range(0, size):
            if current_board[i][row] == -1:
                current_state[row] = False
    else:
        current_state[row] = True
        for i in range(0, size):
            if current_board[i][row] == 1:
                current_state[row] = False
    return current_state


# Diagonals Top Left > Bottom Right & Top Right > Bottom Left
def winning_lines(current_board):
    diagonals = [False, False]
    columns = [False, False, False, False, False]
    rows = [False, False, False, False, False]
    for row in range(0, size):
        for column in range(0, size):
            if current_board[column][row] == 1:
                if (column == row or column + row == 4) and diagonals != [True, True]:
                    diagonals = check_diagonal(current_board, column, row, diagonals, True)
                columns = check_columns(current_board, column, columns, True)
                rows = check_rows(current_board, column, row, rows, True)
    count = 0
    for x in diagonals:
        if x:
            count += 1
    for x in columns:
        if x:
            count += 1
    for x in rows:
        if x:
            count += 1
    return count


def losing_lines(current_board):
    diagonals = [False, False]
    columns = [False, False, False, False, False]
    rows = [False, False, False, False, False]
    for row in range(0, size):
        for column in range(0, size):
            if current_board[column][row] == -1:
                if (column == row or column + row == 4) and diagonals != [True, True]:
                    diagonals = check_diagonal(current_board, column, row, diagonals, False)
                columns = check_columns(current_board, column, columns, False)
                rows = check_rows(current_board, column, row, rows, False)
    count = 0
    for x in diagonals:
        if x:
            count += 1
    for x in columns:
        if x:
            count += 1
    for x in rows:
        if x:
            count += 1
    return count


def evaluate_board(player, current_board):
    if player:
        return winning_lines(current_board) - losing_lines(current_board)
    else:
        return losing_lines(current_board) - winning_lines(current_board)


def minimax(depth, player, current_board):
    validate_moves()
    if depth == 0:
        return evaluate_board(player, current_board), (None, None)
    child = find_children()
    if not player:
        value = -math.inf
        for move in child:
            newish_board = deepcopy(current_board)
            newish_board[move[0]][move[1]] = -1
            new_board = newish_board
            result = max(value, minimax(depth - 1, True, new_board)[0]), move
    else:
        value = +math.inf
        for move in child:
            newish_board = deepcopy(current_board)
            newish_board[move[0]][move[1]] = 1
            new_board = newish_board
            result = min(value, minimax(depth - 1, False, new_board)[0]), move
    return result


def annouce_start():
    print("Welcome to Tic-Tac-Toe, you will play first")
    print("To play a position, select a row number, and a column number")
    # anything else here


def make_move(bool):
    row = int(input("What row do you want to play at? "))
    column = int(input("What column do you want to play at? "))
    if bool:
        board[row][column] = 1
    else:
        board[row][column] = -1


def start_board(length):
    rc = []
    vm = []
    for i in range(0, length):
        rc.append(0)
        vm.append(True)
    for i in range(0, length):
        board.append(deepcopy(rc))
        vaild_move.append(deepcopy(vm))


def print_neat():
    current_col = 0
    for i in range(0, size):
        if current_col == size - 1:
            print(str(current_col) + ".")
            break
        print(str(current_col) + ", ", end='')
        current_col += 1

    counter = 0
    current_row = 0

    for row in board:
        for element in row:
            print(element, end='')
            print(", ", end='')
            counter += 1
            if counter == size:
                print("Row " + str(current_row) + ".", end='')
        print()
        counter = 0
        current_row += 1


def game_finish():
    print("Cool, someone won, was it you?")


annouce_start()
start_board(size)
print_neat()

while not game_finished:
    make_move(True)
    check_game()
    print_neat()
    if game_finished:
        break
    if bot_play:
        bot_move()
    else:
        validate_moves()
        print(vaild_move)
        print(find_children())
        print(minimax(2,False,board))
        make_move(False)
    print_neat()
    check_game()

game_finish()
