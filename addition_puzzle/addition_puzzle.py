import random as rm
import copy

def choose_pattern():
    # the tuples in the patterns indicate which possitions are added to get that position
    patterns = [[0, (0,2), 0, (0,6), (1, 3, 5, 7), (2, 8), 0, (6, 8), 0],
                [0, (2, 5), (5, 8), 0, (1, 7), 0, (0, 3), (3, 6), 0],
                [0, (0, 4), (1, 5), (0, 4), 0, (4, 8), (3, 7), (4, 8), 0],
                [(1, 3), 0, (1, 5), 0, (0, 2, 6, 8), 0, (3, 7), 0, (5, 7)],
                [(3, 6), (4, 7), (5, 8), 0, 0, (3, 4), 0, 0, (6, 7)],
                [(1, 4), 0, (1, 4), (0, 6), 0, (2, 8), (4, 7), 0, (4, 7)],
                [(3, 6), (0, 4), (1, 5), 0, (3, 7), (4, 8), 0, 0, (6, 7)]]
    pattern = rm.choice(patterns) # choose a random pattern
    return pattern

def fill_grid(pattern):
    """
    the pattern is organized such that a zero entry is an inicial value to be randomly filled,
    a tuple is one that has not been filled yet, and a non-zero integer has already been filled
    """
    still_going = True
    while still_going:
        still_going = False
        for i, item in enumerate(pattern):
            if item == 0: # if item is one of the initial values, fill with a random integer 1-9
                still_going = True
                pattern[i] = rm.sample(range(1, 10), 1)[0]
                continue
            elif isinstance(item, tuple): # if it is a tuple, check if all spaces are filled that need to be added up
                still_going = True
                missing_number = False
                sum = 0
                for val in item:
                    if isinstance(pattern[val], int) and pattern[val] > 0:
                        sum += pattern[val]
                    else:
                        missing_number = True
                        break
                if not missing_number:
                    pattern[i] = sum
    return pattern

def print_grid(grid):
    print()
    print(grid[0], grid[1], grid[2])
    print(grid[3], grid[4], grid[5])
    print(grid[6], grid[7], grid[8])
    print()
    

def create_grids():
    pattern = choose_pattern()
    g1 = fill_grid(copy.deepcopy(pattern))
    g2 = fill_grid(copy.deepcopy(pattern))
    g3 = fill_grid(copy.deepcopy(pattern))
    g4 = fill_grid(copy.deepcopy(pattern))
    # remove and save number from g3
    to_remove_g3 = rm.sample(range(0, 9), 1)[0]
    g3_missing = g3[to_remove_g3]
    g3[to_remove_g3] = '?'
    # remove and save three numbers from g4
    to_remove_g4 = rm.sample(range(0, 9), 3)
    g4_missing = []
    for index in to_remove_g4:
        g4_missing.append(g4[index])
        g4[index] = '?'
    return g1, g2, g3, g3_missing, g4, g4_missing

def do_puzzle(): # get the grids, then have the user guess the missing numbers
    print("Welcome to the my number puzzle! I will give you four 3 by 3 grids \n" \
    "of numbers. Each one has the same pattern, but different numbers. \n" \
    "The first two will be completely filled in, the third one will be \n" \
    "missing one number, then the last one will be missing three numbers. \n" \
    "Your job is to find the missing numbers. Hint, the pattern uses addition.")
    while True:
        print()
        print("Here are the grids:")
        g1, g2, g3, g3_missing, g4, g4_missing = create_grids()
        print_grid(g1)
        print_grid(g2)
        print_grid(g3)
        print_grid(g4)
        g3_guess = input("What number is missing from the third grid? ")
        if int(g3_guess) == g3_missing:
            print("You got it right!")
        else:
            print(f"Sorry to tell you, that's not the answer. The number was {g3_missing}.")
        print()
        g4_guess = input("Now, what three numbers are missing from the fourth grid? Enter them \n"
        "with spaces inbetween. The order doesn't matter. For example: '1 2 3'. ")
        if set(g4_missing) == set(int(num) for num in g4_guess.split(" ")):
            print("You got it right! Nice job, that one was hard.")
        else:
            print(f"It appears you did something wrong. Better luck next time! The numbers were {g4_missing}.")
        print()
        print("Thanks for playing!")
        again = input("Would you like to play again? (y/n) ")
        if again == 'n':
            break

if __name__ == '__main__':
    do_puzzle()
    