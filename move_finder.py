import sys
import random
from time import time
from itertools import product
from collections import Counter


class Grid:
    """
    Wrapper class for a grid, provides method for checking for matches
    """

    def __init__(self, grid: list):
        """
        Constructor for class
        :param grid: Grid of gem types
        """
        # Set field variabls
        self.grid = grid

    def get_gem(self, i: int, j: int):
        """
        Method to get gem at a location
        :param i: y coordinate to check
        :param j: x coordinate to check
        :return: None if coordinate off grid, if not then gem at coordinate
        """
        if len(self.grid) <= i or len(self.grid[0]) <= j:
            return None
        else:
            return self.grid[i][j]

    def match_check(self):
        """
        Method to check if this grid contains matches
        :return: True if grid contains one or matches, False if not
        """
        for i in range(len(self.a)):
            for j in range(len(self.a[0])):
                    if self.get_gem(i, j) is self.get_gem(i + 1, j) is self.get_gem(i + 2, j) is not None:
                        return True
                    if self.get_gem(i, j) is self.get_gem(i, j + 1) is self.get_gem(i, j + 2) is not None:
                        return True
        return False


class Swapped(Grid):
    """
    Class that provides an swapped view of a grid if a move had been made
    """

    def __init__(self, grid: list, y: int, x: int, d: int):
        """
        Constructor for class
        :param grid: grid of gems
        :param y: Y coordinate of move
        :param x: X coordinate of move
        :param d: Direction of move, 0 for down or 1 for right
        """
        # Call to super constructor
        super().__init__(grid)
        # Set field variables
        self.y = y
        self.x = x
        self.d = d
        # Calculate coordinates of swap
        self.swapped = [[y, x], [j + 1 if i == d else j for i, j in enumerate([y, x])]]
    
    def good(self):
        """
        Method to check that the move this class was made with was not a swap off the grid
        :return: True is swap was on grid, False if not
        """
        return self.swapped[1][0] < len(self.grid) and self.swapped[1][1] < len(self.grid[0])
    
    def get_gem(self, i: int, j: int):
        """
        Method to find the gem at a position in the grid
        :return: None if coordinate off grid, if not them gem at coordinate
        """
        # Gem at other swapped location if swapped location was given...
        if [i, j] in self.swapped:
            k = self.swapped.index([i, j])
            return self.grid[self.swapped[1 - k][0]][self.swapped[1 - k][1]]
        # ... if not call method from superclass
        else:
            return super().get_gem(i, j)


def moves_one(grid: list):
    """
    Function that returns a list of moves that can be made
    :param grid: Grid to search for moves, should not contain matches
    :return: List of moves that can be made
    """
    # Create empty list for moves
    moves = []
    # Iterate through all possible moves
    for i, j, k in product(range(len(grid)), range(len(grid[0])), range(2)):
        # Create view of grid if this move was made
        swapped = Swapped(grid, i, j, k)
        # Check if this move was not off grid and if it results in a match
        if swapped.good() and swapped.match_check():
            # If this resulted in a match add to list
            moves.append((i, j, k))
    # Return list of moves
    return moves


def moves_two(grid: list):
    """
    Function adapted from GemGem's method for checking if there are possible moves. Returns the 
    coordinates of the top left corner of the rectangle the move would be in, not an actual move
    :param grid: Grid to search for moves, should not contain matches
    :return: List of rectangle corners
    """
    # Wrap grid in Grid object to reuse get_gem method
    wrapper = Grid(grid)
    # Create empty list for moves
    corners = []
    # These specify patterns where the same gem type must exist for a move to be possible
    oneOffPatterns = (((0, 1), (1, 0), (2, 0)),
                      ((0, 1), (1, 1), (2, 0)),
                      ((0, 0), (1, 1), (2, 0)),
                      ((0, 1), (1, 0), (2, 1)),
                      ((0, 0), (1, 0), (2, 1)),
                      ((0, 0), (1, 1), (2, 1)),
                      ((0, 0), (0, 2), (0, 3)),
                      ((0, 0), (0, 1), (0, 3)))
    # Iterate through all positions and patterns
    for i, j, pat in product(range(len(a)), range(len(a[0])), oneOffPatterns):
        # Check if pattern exists 
        if (wrapper.get_gem(i + pat[0][0], j + pat[0][1]) is \
            wrapper.get_gem(i + pat[1][0], j + pat[1][1]) is \
            wrapper.get_gem(i + pat[2][0], j + pat[2][1]) is not None) or \
           (wrapper.get_gem(i + pat[0][1], j + pat[0][0]) is \
            wrapper.get_gem(i + pat[1][1], j + pat[1][0]) is \
            wrapper.get_gem(i + pat[2][1], j + pat[2][0]) is not None):
                # If a move exists here add the corner to the list
                corners.append((i, j))
    # Return list of corners
    return corners


def moves_three(grid: list):
    """
    Function that returns a list of moves that can be made
    :param grid: Grid to search for moves, should not contain matches
    :return: List of moves that can be made, may contain duplicates
    """
    # Create empty list for moves
    moves = []
    # Get number of rows in grid
    rows = len(grid)
    # Get number of columns in grid
    columns = len(grid[0])
    # Iterate over all locations and down/right directions
    for i, j, k in product(range(rows), range(columns), range(2)):
        # Check if this location/direction pair extends three without leaving the grid
        if (i < rows - 2 and k == 0) or (j < columns - 2 and k == 1):
            # Get the coordinates in this section of three
            to_check = [(i + c, j) if k == 0 else (i, j + c) for c in range(3)]
            # Get the types in this section
            types = [grid[i][j] for i, j in to_check]
            # Count the occurrences of each type 
            c = Counter(types).most_common()
            # If there are 2 types then must be two of one type, one of another
            if len(c) == 2:
                # Get the type which occoured twice
                major_type = c[0][0]
                # Get the type which occoured once
                minor_type = c[1][0]
                # Get the coordinates of the minor_type
                y1, x1 = to_check[types.index(minor_type)]
                # Get the coordinates surrounding this
                surround = [(y1, x1 + offset) for offset in range(-1, 2, 2)] + [(y1 + offset, x1) for offset in range(-1, 2, 2)]
                # Filter this to make sure they are on the grid and not in the section of three
                surround = [(y2, x2) for y2, x2 in surround if 0 <= y2 < rows and 0 <= x2 < columns and (y2, x2) not in to_check]
                # Iterate through these locations
                for y2, x2 in surround:
                    # If a major_type gem is present this can be used to make a match
                    if grid[y2][x2] == major_type:
                        # Add move to moves list
                        moves.append(((y1, x1), (y2, x2)))
    # Return list of moves
    return moves


def p(grid: list):
    """
    Function to print a grid
    :param grid: Grid to print
    :return: None
    """
    print('\n'.join([''.join([str(el) for el in row]) for row in grid]))


def time_test(grid: list, N: int):
    """
    Function to compare runtimes of functions
    :param grid: Grid to test with
    :param N: Number of times to test each function
    :return: None
    """
    # Create list to store times in
    t = []
    # Append start time
    t.append(time())
    # Run moves_one N times
    for _ in range(N):
        m1 = moves_one(a)
    # Append intermediate time
    t.append(time())
    # Run moves_two N times
    for _ in range(N):
        m2 = moves_two(a)
    # Append intermediate time
    t.append(time())
    # Run moves_three N times
    for _ in range(N):
        m3 = moves_three(a)
    # Append end time
    t.append(time())
    # Print results
    print(m1, m2, m3, sep='\n\n', end='\n')
    # Print total times
    print('Total times:')
    print(*[t[i] - t[i - 1] for i in range(1, len(t))], sep='\t', end='\n')
    # Print times for one run
    print('Single time:')
    print(*[(t[i] - t[i - 1]) / N for i in range(1, len(t))], sep='\t', end='\n')

# Main
if __name__ == '__main__':
    # Get grid size from command line, default to 5
    n = int(sys.argv[1]) if 1 < len(sys.argv) else 5
    # Generate a grid with no matches (caution with large grid sizes, may run for a long time)
    while True:
        grid = [[random.randrange(6) for _ in range(n)] for _ in range(n)]
        if not Normal(grid).match_check():
            p(grid, end='\n\n')
            break

    # Get number of tests from command line, default to 1000
    N = int(sys.argv[2]) if 2 < len(sys.argv) else 1000
    # Run tests
    time_test(grid, N)
