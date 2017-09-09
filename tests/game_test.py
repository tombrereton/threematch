import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from events.event_manager import EventManager
from model.game import Board
from itertools import product

rows0 = 2
columns0 = 3
ice_rows0 = 2
medals0 = 1
moves_left0 = 30

rows1 = 1
columns1 = 5
ice_rows1 = 0
medals1 = 0
moves_left1 = 30

rows2 = 1
columns2 = 5
ice_rows2 = 0
medals2 = 0
moves_left2 = 30

event_manager = EventManager()
b = Board(rows0, columns0, ice_rows0, medals0, moves_left0, test='horizontal', event_manager=event_manager)
b0 = Board(rows0, columns0, ice_rows0, medals0, moves_left0, test='horizontal', event_manager=event_manager)
b2 = Board(rows2, columns2, ice_rows2, medals2, moves_left2, test='horizontal', event_manager=event_manager)


def test_create_diamond_bonus():
    """
    Test creation of diamond bonus.

    Vertical is a three in a column.
    Horizontal is a three in a row.

    The swap makes the horizontal and vertical
    intersect. The intersection is a
    diamond bonus (type 3).

    All matches should be removed including the gems
    from the bonus action (points (1,1) and (1,3))
    :return:
    """
    print('\n\nTest 1.5 match intersect:\n')

    b2 = Board(3, 4, ice_rows1, medals1, moves_left1, gem_types=3, test='horizontal', event_manager=event_manager)

    # Set up grid for testing
    b2.gem_grid.grid[0][2] = (2, 0, 0)
    b2.gem_grid.grid[1][2] = (2, 0, 0)
    b2.gem_grid.grid[2][2] = (0, 0, 0)
    b2.gem_grid.grid[2][3] = (2, 3, 0)
    print(b2)

    # swap to allow matches to be found
    swap_locations = [(2, 2), (2, 3)]
    b2.set_swap_locations(swap_locations)
    b2.swap_gems()

    expected_removals = [(0, 2, 2, 0, 0), (1, 1, 1, 0, 0), (1, 2, 2, 0, 0), (1, 3, 1, 0, 0), (2, 0, 2, 0, 0),
                         (2, 1, 2, 0, 0), (2, 3, 0, 0, 0)]
    expected_bonuses = [(2, 2, 2, 3, 0)]

    actual_removals, actual_bonuses = b2.find_matches()

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_create_star_bonus():
    """
    Test creation of star bonus.

    5 gems in a row. Swap first 2 gems.
    :return:
    """
    print('\n\nTest 1.5 match intersect:\n')

    b2 = Board(1, 5, ice_rows1, medals1, moves_left1, gem_types=3, test='horizontal', event_manager=event_manager)

    # swap to allow matches to be found
    swap_locations = [(0, 0), (0, 1)]
    b2.set_swap_locations(swap_locations)
    b2.swap_gems()

    expected_removals = [(0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 0, 0), (0, 4, 0, 0, 0)]
    expected_bonuses = [(0, 0, 0, 2, 0)]

    actual_removals, actual_bonuses = b2.find_matches()

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_create_and_use_cross_bonus():
    """
    Tests the use and creation of a cross bonus.

    5 gems in a row. 3 gems of type 0.
    Then 1 gem of type 0 and cross bonus (removes entire row).
    Then gem of type 1.

    Should remove all gems in row and create a bonus at 1st swap location.

    Swap location is the zeroth element, and the bonus created should be
    type 1.
    :return:
    """
    print('\n\nTest use bonus type 1:\n')
    b1 = Board(rows1, columns1, ice_rows1, medals1, moves_left1, test='horizontal', event_manager=event_manager)

    # Set up grid for testing
    b1.gem_grid.grid[0][3] = (0, 1, 0)
    b1.gem_grid.grid[0][4] = (1, 0, 0)
    print(b1)

    # swap to allow matches to be found
    swap_locations = [(0, 0), (0, 1)]
    b1.set_swap_locations(swap_locations)

    expected_removals = [(0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 1, 0), (0, 4, 1, 0, 0)]
    expected_bonuses = [(0, 0, 0, 1, 0)]

    actual_removals, actual_bonuses = b1.find_matches()

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_create_cross_over_diamond_bonus():
    """
    Tests creation of cross bonus over diamond bonus.

    Vertical and horizontal matches intersect but one is 4 long.
    This means a cross should be created rather than a diamond.
    """
    print('\n\nTest 4 match intersect:\n')

    b2 = Board(4, 4, ice_rows1, medals1, moves_left1, gem_types=4, test='horizontal', event_manager=event_manager)

    # Set up grid for testing
    b2.gem_grid.grid[0][2] = (2, 0, 0)
    b2.gem_grid.grid[1][2] = (2, 0, 0)
    b2.gem_grid.grid[2][2] = (0, 0, 0)
    b2.gem_grid.grid[3][2] = (2, 0, 0)
    print(b2)

    # swap to allow matches to be found
    swap_locations = [(2, 2), (2, 3)]
    b2.set_swap_locations(swap_locations)
    b2.swap_gems()

    # find matches by calling get update twice
    actual_removals, actual_bonuses = b2.find_matches()

    expected_removals = [(0, 2, 2, 0, 0), (1, 2, 2, 0, 0), (2, 0, 2, 0, 0), (2, 1, 2, 0, 0), (3, 2, 2, 0, 0)]
    expected_bonuses = [(2, 2, 2, 1, 0)]

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_create_cross_from_star_bonus():
    """
    Testing that a cross bonus is still
    created when using a bonus type 2.

    8 gems in a row.

    4 of type 0. Then 1 of type 1.
    Then a star bonus (type 2) of type 0.
    Then 2 more of type 0.

    All gems of type 0 should be removed and a
    bonus of type 1 should be created at location
    (0,0).

    Bonus type 1 occurs from 4 in a row.
    Bonus type 2 destroys all gems of that type.
    :return:
    """
    print('\n\nTest 1.6 using a star bonus and getting a match 4:\n')

    b2 = Board(1, 8, ice_rows1, medals1, moves_left1, gem_types=3, test='horizontal', event_manager=event_manager)

    # Set up grid for testing
    b2.gem_grid.grid[0][4] = (1, 0, 0)
    b2.gem_grid.grid[0][5] = (0, 2, 0)
    print(b2)

    expected_removals = [(0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 0, 0), (0, 5, 0, 2, 0),
                         (0, 6, 0, 0, 0), (0, 7, 0, 0, 0)]
    expected_bonuses = [(0, 0, 0, 1, 0)]

    actual_removals, actual_bonuses = b2.find_matches()

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_use_star_bonus():
    """
    Testing that a star bonus (type 2)
    removes all gems of the same type.

    5 gems in a row.
    2 gems of type 0. Then gem of type 0 and bonus type 2 (star).
    Then gem of type 1. Then gem of type 0.

    4 Gems should be removed (all of type 0).
    :return:
    """
    print('\n\nTest use bonus type 2:\n')

    # Set up grid for testing
    row = b2.gem_grid.grid[0]
    # Add type 2 bonus
    row[2] = (0, 2, 0)
    # Add type 1
    row[3] = (1, 0, 0)
    print(row)

    # find matches by calling find_matches
    actual_removals, actual_bonuses = b2.find_matches()

    expected_removals = [(0, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 2, 0, 2, 0), (0, 4, 0, 0, 0)]
    expected_bonuses = []

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_cascade_bonus_activations():
    """
    Testing cascade of bonus activation.

    Star bonus should remove all type 0 gems,
    one of which is a cross bonus, which should
    remove the remaining type 1 gem.

    5 gems in a row.

    1st gem is a diamond of type 0. 2nd is a gem of
    type 1. 3rd is a star of type 0. The last 2
    are normal gems of type 0.

    The star should remove all gems of type 0, which
    should the activate the 1st gem bonus, removing the
    type 1 gem.

    In short, this should remove all gems.
    :return:
    """
    print('\n\nTest 1.7 using a bonus when it is removed by a bonus:\n')

    b2 = Board(1, 5, ice_rows1, medals1, moves_left1, gem_types=3, test='horizontal', event_manager=event_manager)

    # Set up grid for testing
    b2.gem_grid.grid[0][0] = (0, 3, 0)
    b2.gem_grid.grid[0][1] = (1, 0, 0)
    b2.gem_grid.grid[0][2] = (0, 2, 0)
    print(b2)

    expected_removals = [(0, 0, 0, 3, 0), (0, 1, 1, 0, 0), (0, 2, 0, 2, 0), (0, 3, 0, 0, 0), (0, 4, 0, 0, 0)]
    expected_bonuses = []

    actual_removals, actual_bonuses = b2.find_matches()

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_using_cross_bonus_vertically():
    """
    Testing cross bonus removes column when
    in vertical match.

    5 gems in a column. 2 gems of type 0,
    then a gem of type 1, then a cross gem of
    type 0, then a gem of type 1.

    All 5 gems should be removed.
    :return:
    """
    print('\n\nTest 1.8 swap in a cross bonus and removing all gems vertically:\n')

    b2 = Board(rows=5, columns=1, ice_rows=0, medals_remaining=0, moves_remaining=10, gem_types=3, test='vertical',
               event_manager=event_manager)

    # Set up grid for testing
    b2.gem_grid.grid[2][0] = (1, 0, 0)
    b2.gem_grid.grid[3][0] = (0, 1, 0)
    b2.gem_grid.grid[4][0] = (1, 0, 0)
    print(b2)

    swap_locations = [(2, 0), (3, 0)]
    b2.set_swap_locations(swap_locations)
    b2.swap_gems()

    print(b2)

    expected_removals = [(0, 0, 0, 0, 0), (1, 0, 0, 0, 0), (2, 0, 0, 1, 0), (3, 0, 1, 0, 0), (4, 0, 1, 0, 0)]
    expected_bonuses = []

    actual_removals, actual_bonuses = b2.find_matches()

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_using_cross_bonus_horizontally():
    """
    Testing cross bonus removes row when
    in horizontal match.

    5 gems in a row. 2 gems of type 0,
    then a gem of type 1, then a cross gem of
    type 0, then a gem of type 1.

    All 5 gems should be removed.
    :return:
    """
    print('\n\nTest 1.9 swap in a cross bonus and removing all gems horizontally:\n')

    b2 = Board(rows=1, columns=5, ice_rows=0, medals_remaining=0, moves_remaining=10, gem_types=3, test='horizontal',
               event_manager=event_manager)

    # Set up grid for testing
    b2.gem_grid.grid[0][2] = (1, 0, 0)
    b2.gem_grid.grid[0][3] = (0, 1, 0)
    b2.gem_grid.grid[0][4] = (1, 0, 0)
    print(b2)

    swap_locations = [(0, 2), (0, 3)]
    b2.set_swap_locations(swap_locations)
    b2.swap_gems()

    print(b2)

    expected_removals = [(0, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 2, 0, 1, 0), (0, 3, 1, 0, 0), (0, 4, 1, 0, 0)]
    expected_bonuses = []

    actual_removals, actual_bonuses = b2.find_matches()

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_ice_removed():
    """
    Testing that all ice is removed
    when gems are matched on top.

    All gems should match and remove
    the ice underneath.

    Grid is 2 by 3.
    :return:
    """
    print("\nBoard 1:\n")
    print(b)

    # ice should be like this
    ice_grid = [[-1] * columns0 for _ in range(rows0)]
    expected_ice = b.ice_grid.grid

    swap_locations = [(0, 0), (0, 1)]
    b.set_swap_locations(swap_locations)

    actual_removals, actual_bonuses = b.find_matches()
    b.match_list = actual_removals
    b.bonus_list = actual_bonuses
    b.remove_gems_add_bonuses()

    actual_ice_grid = b.ice_grid.grid

    assert expected_ice == actual_ice_grid


def test_remove_ice_when_creating_bonus():
    """
    Testing that ice is removed when a bonus is
    also created.

    Row of 4 gems of type 0.

    Should remove all gems except for the first,
    where a bonus of type 1 is created.

    The ice should all be removed underneath
    :return:
    """
    print('\n\nTest 2.3 removing ice when creating a bonus:\n')

    b2 = Board(rows=1, columns=4, ice_rows=1, medals_remaining=0, moves_remaining=10, gem_types=3, test='horizontal',
               event_manager=event_manager)

    print(b2)

    expected_removals = [(0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 0, 0)]
    expected_bonuses = [(0, 0, 0, 1, 0)]
    expected_ice_grid = [[-1, -1, -1, -1]]

    actual_removals, actual_bonuses = b2.find_matches()
    b2.match_list = actual_removals
    b2.bonus_list = actual_bonuses
    b2.remove_gems_add_bonuses()

    actual_ice_grid = b2.ice_grid.grid

    assert expected_ice_grid == actual_ice_grid
    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_get_game_state():
    """
    The get game state function should
    return all three states as a string in vector form.

    Medals are obscured so they should be all -1 values.
    :return:
    """
    print('\n\nTest 3.1 get state in vector form:\n')

    b = Board(rows=2, columns=3, ice_rows=2, medals_remaining=1, moves_remaining=10, gem_types=3, test='horizontal',
              event_manager=event_manager)

    b.medal_grid.grid = [[0, 1, -1], [2, 3, -1]]

    b.gem_grid_copy = b.gem_grid.grid
    print(b)

    state = b.get_game_state()
    print(state)

    medal_score = '0\t0\t'
    expected_state = medal_score + '0\t0\t0\t-1\t0\t0\t0\t-1\t0\t0\t0\t-1\t1\t0\t0\t-1\t1\t0\t0\t-1\t1\t0\t0\t-1\t'

    assert state == expected_state


def test_get_game_state_2():
    """
    The get game state function should
    return all three states as a string in vector form.
    :return:
    """
    print('\n\nTest 3.1 get state in vector form:\n')

    b = Board(rows=2, columns=3, ice_rows=2, medals_remaining=1, moves_remaining=10, gem_types=3, test='horizontal',
              event_manager=event_manager)

    print(b)

    b.gem_grid_copy = b.gem_grid.grid
    game_state = b.get_game_state()
    print(game_state)

    expected_game_state = '0\t0\t' + '0\t0\t0\t-1\t' + '0\t0\t0\t-1\t' + '0\t0\t0\t-1\t' + '1\t0\t0\t-1\t' + \
                          '1\t0\t0\t-1\t' + '1\t0\t0\t-1\t'

    assert game_state == expected_game_state


def test_get_game_state_3():
    """
    The get game state function should
    return all three states as a string in vector form.
    :return:
    """
    print('\n\nTest 3.1 get state in vector form:\n')

    b = Board(rows=2, columns=3, ice_rows=2, medals_remaining=1, moves_remaining=10, gem_types=3, test='horizontal',
              event_manager=event_manager)

    for i, j in product(range(2), range(3)):
        b.ice_grid.grid[i][j] = -1
        b.medal_grid.grid[i][j] = -1

    b.medal_grid.grid[0][0] = 0
    b.medal_grid.grid[0][1] = 1
    b.medal_grid.grid[1][0] = 2
    b.medal_grid.grid[1][1] = 3

    b.ice_grid.grid[0][1] = 0
    b.ice_grid.grid[1][1] = 0

    print(b)

    b.gem_grid_copy = b.gem_grid.grid
    game_state = b.get_game_state()
    print(game_state)

    expected_game_state = '0\t0\t' + '0\t0\t-1\t0\t' + '0\t0\t0\t-1\t' + '0\t0\t-1\t-1\t' + '1\t0\t-1\t2\t' + \
                          '1\t0\t0\t-1\t' + '1\t0\t-1\t-1\t'

    assert game_state == expected_game_state
