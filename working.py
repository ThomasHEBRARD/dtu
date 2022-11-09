import numpy as np
import itertools
from collections import defaultdict
import time

import fileinput

map_ = {"#": 1, "_": 0}


def terminate():
    print("NO")
    exit()


def parse_input():
    lines = []
    for line in fileinput.input():
        lines.append(line)

    # Empty input
    if not lines:
        terminate()

    try:
        alphabet_size, no_of_strings, puzzle_size = map(int, lines[0].split(';'))
    # Missing info
    except ValueError:
        terminate()

    try:
        letters = lines[1].strip().split(";")
    # Missing line
    except IndexError:
        terminate()

    grid = lines[2: 2 + puzzle_size]
    try:
        grid = [[map_[item] for item in line.strip() if item != ';'] for line in grid]
    # Characters that aren't # or _ in the grid lines
    except KeyError:
        terminate()

    # Input grid isn't a perfect square
    for row in grid:
        if len(row) != puzzle_size:
            terminate()

    strings = set([s.strip() for s in lines[2 + puzzle_size:]])

    letters = set(letters)
    letters_in_strings = set()
    for string in strings:
        letters_in_string = set(string)
        # string contains letter not in alphabet
        if len(letters_in_string - letters) != 0:
            terminate()
        letters_in_strings = letters_in_strings.union(letters_in_string)

    # Not all leters used in strings
    if letters_in_strings != letters:
        terminate()

    return alphabet_size, no_of_strings, puzzle_size, letters, grid, strings


def transpose(grid):
    return np.array(grid).T.tolist()


def printer_util(s):
    return "#" if s == 1 else s


def pprint(grid):
    for row in grid:
        print(row)


def verify_columns(grid, strings):
    """Verifies that the "words" in the rows are strings"""
    for row in transpose(grid):
        strings_in_row = "".join([str(i) for i in row]).split("1")
        for string in strings_in_row:
            if string != "" and string not in strings:
                return False
    return True


def zero_runs(a):
    """Gets indices in row where there is a sequence of zeros
       I.e the indices where we need to input words
       https://stackoverflow.com/questions/24885092/finding-the-consecutive-zeros-in-a-numpy-array"""
    is_zero = np.concatenate(([0], np.equal(a, 0), [0]))
    abs_diff = np.abs(np.diff(is_zero))
    ranges = np.where(abs_diff == 1)[0].reshape(-1, 2)
    return ranges


def get_details_of_rows(grid):
    """
        grid_information -> List of tuples of location and length of each word. eg.
                            [(0, 1, 2), ...) means, that at 0th row, 1st position, there
                            is a word of length 2.

        count_lengths    -> Dict {word_length: count, ...} of how many
                            words of each length are needed to fill rows.
    """
    grid_information = []
    count_lengths = defaultdict(int)
    for i, row in enumerate(grid):
        row_information = zero_runs(np.array(row))
        for word_start, word_end in row_information:
            word_length = word_end - word_start
            grid_information.append((i, word_start, word_length))
            count_lengths[word_length] += 1
    return grid_information, count_lengths


def split_strings_by_length(strings):
    """
    strings_by_length is something like:
        {3: ['bab', 'cab'], 2: ['aa', 'ac', 'bb'], 1: ['a']}
    """
    strings_by_length = defaultdict(list)
    for string in strings:
        strings_by_length[len(string)].append(string)
    return strings_by_length


def get_all_potential_solutions(count_lengths, strings_by_length):
    """Generator that generates all possible combinations of strings that may
        yield a solution. For example, if the grid needs 2 words of length 2 and
        3 words of length 3, it will generate all combinations of 5 elements from strings
        whereof two strings will have length 2, and 3 strings will have length 3
    """
    permutations = []
    for word_length in sorted(count_lengths.keys()):
        permutations.append(itertools.product(strings_by_length[word_length],
                                              repeat=count_lengths[word_length]))

    for i in itertools.product(*permutations):
        yield list(sum(i, ()))  # Slightly hacky, but concats a tuple of tuples into a list.


def input_solution_to_grid(grid, possible_solution, grid_information):
    """Fill grid with the possible solution"""
    for s, (row, col, length) in zip(possible_solution, grid_information):
        grid[row][col: col + length] = list(s)

    return grid


def solver(grid, strings):

    grid_information, count_lengths = get_details_of_rows(grid)

    strings_by_length = split_strings_by_length(strings)

    # Sort by string length, as that is the output order of itertools.product combinations
    grid_information = sorted(grid_information, key=lambda x: x[2])

    for possible_solution in get_all_potential_solutions(count_lengths, strings_by_length):
        grid = input_solution_to_grid(grid, possible_solution, grid_information)

        if verify_columns(grid, strings):
            for row in grid:
                print(";".join([printer_util(s) for s in row]))
            return
    print("NO")


if __name__ == "__main__":
    # import time
    # s = time.time()
    alphabet_size, no_of_strings, puzzle_size, letters, grid, strings = parse_input()
    filled_grid = solver(grid, strings)
    # print(time.time() - s, "seconds")
