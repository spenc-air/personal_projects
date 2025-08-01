import numpy as np
from termcolor import colored
import random

# define matrices representing rows in the hexdoku as global variables
# note, rows are numbered to allign with the hexigon they contain the most of
Columns = np.array([[4,0,4,0,3,0,3],[7,1,7,1,4,1,4],[6,2,6,2,5,2,5],[0,3,0,3,6,3,6],[1,4,1,4,0,4,0],[2,5,2,5,8,5,8],[3,6,3,6,2,6,2]])
R_diag = np.array([[8,8,0,0,0,1,1],[0,0,1,1,1,2,2],[1,1,2,2,2,3,3],[2,2,3,3,3,4,4],[3,3,4,4,4,5,5],[4,4,5,5,5,6,6],[5,5,6,6,6,7,7]])
L_diag = np.array([[0,2,5,0,2,5,0],[1,3,6,1,3,6,1],[2,7,0,2,7,0,2],[3,5,1,3,5,1,3],[4,6,8,4,6,8,4],[5,0,3,5,0,3,5],[6,1,4,6,1,4,6]])

# dictionary for converting row and spot to entry position
rs_dict = {(1,1):(0,1), (2,1):(0,0), (2,2):(0,4), (2,3):(2,1), (3,1):(0,3), (3,2):(2,0), (3,3):(2,4),
           (4,1):(0,2), (4,2):(0,6), (4,3):(2,3), (5,1):(1,1), (5,2):(0,5), (5,3):(2,2), (5,4):(2,6),
           (6,1):(1,0), (6,2):(1,4), (6,3):(3,1), (6,4):(2,5), (7,1):(1,3), (7,2):(3,0), (7,3):(3,4), (7,4):(5,1),
           (8,1):(1,2), (8,2):(1,6), (8,3):(3,3), (8,4):(5,0), (8,5):(5,4), (9,1):(1,5), (9,2):(3,2), (9,3):(3,6), (9,4):(5,3),
           (10,1):(4,1), (10,2):(3,5), (10,3):(5,2), (10,4):(5,6), (11,1):(4,0), (11,2):(4,4), (11,3):(6,1), (11,4):(5,5),
           (12,1):(4,3), (12,2):(6,0), (12,3):(6,4), (13,1):(4,2), (13,2):(4,6), (13,3):(6,3), (14,1):(4,5), (14,2):(6,2), (14,3):(6,6), (15,1):(6,5)}

def unique_vals(row):
    # returns false if values are not unique, not counting Nonetypes 
    # create set without Nonetype
    s = set(row)
    s.discard(None)
    # compare to total elements that are not Nonetype
    return len(s) == np.count_nonzero(row != None)

def check_axis(M, A, val): # matrix, axis matrix, value
    mask = (A == val)
    row = M[mask] # vector with values of M at the same indexes as the ones in row_matrix
    if not unique_vals(row):
        return False

def valid_hexudoku(A):
    # check if A is the right shape
    m,n = np.shape(A)
    if not m == n == 7:
        return False
    # check unique values of each group of 7 hexigons
    for row in A:
        if not unique_vals(row):
            return False
    # check for uniqueness along axes
    for i in range(7):
        if check_axis(A, Columns, i) == False:
            return False
        if check_axis(A, R_diag, i) == False:
            return False
        if check_axis(A, L_diag, i) == False:
            return False
    return True

def taken_vals(M, A, x, y):
    row_index = A[x, y]
    mask = (A == row_index)
    row = M[mask] # vector with values of M at the same indexes as the ones in row_matrix
    return set(row)

def possible_vals(M, x, y): 
    vals = {0,1,2,3,4,5,6}
    # check in hexigon
    for hex_val in M[x]:
        vals.discard(hex_val)
    # check columns
    h_vals = taken_vals(M, Columns, x, y)
    # check right diagonals
    r_vals = taken_vals(M, R_diag, x, y)
    # check left diagonals
    l_vals = taken_vals(M, L_diag, x, y)
    # subtract all taken values
    return vals - h_vals - r_vals - l_vals

def just_middle():
    M = np.full((7, 7), None) # fill with None
    M[3,] = np.arange(7) # replace middle row (hexigon) with 0 to 6
    return M

def find_valid_solution(M):
    # search the spaces in a dinamic order
    search_seq = [(5, 2), (5, 5), (5, 0), (5, 3), (5, 6), (5, 1), (5, 4),
                   (2, 5), (2, 2), (2, 6), (2, 4), (2, 3), (2, 0), (2, 1), 
                   (0, 5), (0, 2), (0, 6), (0, 3), (0, 0), (0, 1), (0, 4),
                   (1, 4), (1, 1), (1, 6), (1, 5), (1, 3), (1, 2), (1, 0),
                   (4, 1), (4, 0), (4, 4), (4, 6), (4, 3), (4, 5), (4, 2),
                   (6, 0), (6, 2), (6, 1), (6, 4), (6, 6), (6, 3), (6, 5)]
    pos_entries = [possible_vals(M, 5, 2)] # list of sets
    i = 0
    while True:
        if i == -1: # all combinations have been checked
            break
        x, y = search_seq[i]
        if pos_entries[i]:
            # takes a possible entry and inputs it into M
            M[x, y] = pos_entries[i].pop() 
            # then find possibilities for next space
            if i == 41: # all spaces have been filled
                return M
            x, y = search_seq[i + 1]
            vals = possible_vals(M, x, y)
            if vals:
                pos_entries.append(vals)
                i += 1
        else:
            # no more possible entries for space, need to back track
            pos_entries.pop()
            M[x, y] = None # reset space to none
            i -= 1

def entry(n):
    if n is None:
        return " "
    else:
        return n

def print_grid(M):
    print()
    print(colored('1......../', 'blue') + f'{entry(M[0,1])}' + colored('\\', 'blue')) 
    print(colored('2....../', 'blue') + f'{entry(M[0,0])}' + '\\ /' + f'{entry(M[0,4])}' + colored('\\ /', 'blue') + f'{entry(M[2,1])}' + colored('\\', 'blue'))
    print(colored('3......\\', 'blue') + f' /{entry(M[0,3])}\\ ' + colored('/', 'blue') + f'{entry(M[2,0])}\\ /{entry(M[2,4])}' + colored('\\', 'blue'))
    print(colored('4....../', 'blue') + f'{entry(M[0,2])}' + '\\ /' + f'{entry(M[0,6])}' + colored('\\', 'blue') + f' /{entry(M[2,3])}\\ ' + colored('/', 'blue'))
    print(colored('5..../', 'blue') + f'{entry(M[1,1])}' + colored('\\', 'blue') + f' /{entry(M[0,5])}\\ ' + colored('/', 'blue') + f'{entry(M[2,2])}\\ /{entry(M[2,6])}' + colored('\\', 'blue'))
    print(colored('6../', 'blue') + f'{entry(M[1,0])}' + '\\ /' + f'{entry(M[1,4])}' + colored('\\ /', 'blue') + f'{entry(M[3,1])}' + colored('\\', 'blue') + f' /{entry(M[2,5])}\\ ' + colored('/', 'blue'))
    print(colored('7..\\', 'blue') + f' /{entry(M[1,3])}\\ ' + colored('/', 'blue') + f'{entry(M[3,0])}\\ /{entry(M[3,4])}' + colored('\\ /', 'blue') + f'{entry(M[5,1])}' + colored('\\', 'blue'))
    print(colored('8../', 'blue') + f'{entry(M[1,2])}' + '\\ /' + f'{entry(M[1,6])}' + colored('\\', 'blue') + f' /{entry(M[3,3])}\\ ' + colored('/', 'blue') + f'{entry(M[5,0])}\\ /{entry(M[5,4])}' + colored('\\', 'blue'))
    print(colored('9..\\', 'blue') + f' /{entry(M[1,5])}\\ ' + colored('/', 'blue') + f'{entry(M[3,2])}\\ /{entry(M[3,6])}' + colored('\\', 'blue') + f' /{entry(M[5,3])}\\ ' + colored('/', 'blue'))
    print(colored('10...\\ /', 'blue') + f'{entry(M[4,1])}' + colored('\\', 'blue') + f' /{entry(M[3,5])}\\ ' + colored('/', 'blue') + f'{entry(M[5,2])}\\ /{entry(M[5,6])}' + colored('\\', 'blue'))
    print(colored('11.../', 'blue') + f'{entry(M[4,0])}' + '\\ /' + f'{entry(M[4,4])}' + colored('\\ /', 'blue') + f'{entry(M[6,1])}' + colored('\\', 'blue') + f' /{entry(M[5,5])}\\ ' + colored('/', 'blue'))
    print(colored('12...\\', 'blue') + f' /{entry(M[4,3])}\\ ' + colored('/', 'blue') + f'{entry(M[6,0])}\\ /{entry(M[6,4])}' + colored('\\ /', 'blue'))
    print(colored('13.../', 'blue') + f'{entry(M[4,2])}' + '\\ /' + f'{entry(M[4,6])}' + colored('\\', 'blue') + f' /{entry(M[6,3])}\\ ' + colored('/', 'blue'))
    print(colored('14...\\', 'blue') + f' /{entry(M[4,5])}\\ ' + colored('/', 'blue') + f'{entry(M[6,2])}\\ /{entry(M[6,6])}' + colored('\\', 'blue'))
    print(colored('15.....\\ / \\', 'blue') + f' /{entry(M[6,5])}\\ ' + colored('/', 'blue'))
    print(colored('             \\ /', 'blue'))
    print()

def get_random_solution():
    # get 0-6 in a random order
    nums = list(range(7))
    random.shuffle(nums)
    # fill grid with None
    M = np.full((7, 7), None) 
    # replace middle row (hexigon) with nums
    M[3,] = nums
    return find_valid_solution(M) # return with the rest of the grid filled in

def remove_nums(M, num):
    hexigons = [(i,j) for i in range(7) for j in range(7)] # list of all spaces in grid
    points_to_delete = random.sample(hexigons, 49-num) # choose which spaces to delete
    for point in points_to_delete:
        x, y = point
        M[x,y] = None
    return M

def take_turn(M):
    r, n, entry = input("What number would you like to add? (format 'row spot entry') ").split(" ")
    position = rs_dict[(int(r), int(n))]
    x, y = position
    if M[x, y] != None:
        print("Space is already filled, try an empty one")
    elif int(entry) in possible_vals(M, x, y):
        M[x, y] = entry
        print_grid(M)
    else:
        print("Entry is not valid, try again")
    return M

def is_complete(M):
    if None in M:
        return False
    else:
        return True

def play_game():
    print()
    print("Hello friends! This puzzle is called a hexudoku, which is a fun variant of the well known sudoku puzzle. \n" \
          "The puzzle is made up of seven groups of seven hexigons. The goal is to fill in the puzzle so no columns, \n" \
          "right-diagonals or left-diagonals repeat any numbers. Notice how you don't have to worry about the rows. \n" \
          "The numbers go from 0 to 6, which I think is way cooler than 1 to 7. When you have identified where you \n" \
          "want to enter a number, type the row, a space, then the spot in that row, another space, then the number \n" \
          "you want to enter there. For example, entering '3 1 2' would enter 2 in the third row, first spot. If the \n" \
          "program prints out the puzzle again that means you got the number right and can enter another, otherwise,\n" \
          "it will let you know you got it wrong. There are 49 total spaces. Starting with 40 hexigons filled in would \n" \
          "make a farely easy puzzle, but something like 20 would be a lot harder.")
    num = int(input("How many hexigons do you want to start filled? "))
    solution = get_random_solution()
    hexudoku = remove_nums(solution, num)
    print_grid(hexudoku)
    while True:
        hexudoku = take_turn(hexudoku) # take turns until the puzzle is solved
        if is_complete(hexudoku):
            print("Congradulations! You solved it!")
            break

if __name__ == '__main__':
    play_game()
    