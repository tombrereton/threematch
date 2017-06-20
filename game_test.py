from events import *
from game import Board

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

def test_1_1_use_bonus_type_1():
    """
    Should remove all gems in row and create no bonuses
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

    # find matches by calling get update twice
    bag1 = b1.get_update()
    bag = b1.get_update()
    print(bag)

    expected_removals = [(0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 1, 0), (0, 4, 1, 0, 0)]
    expected_bonuses = [(0, 0, 0, 1, 0)]

    actual_removals = bag.removals
    actual_bonuses = bag.bonuses

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_1_2_use_bonus_type_2():
    """
    TODO
    :return:
    """
    print('\n\nTest use bonus type 2:\n')

    # Set up grid for testing
    row = b2.gem_grid.grid[0]
    # Add type 2 bonus
    row[2] = (0, 2, 0)
    # Add type 1
    row[3] = (1, 0, 0)

    # find matches by calling find_matches
    actual_removals, actual_bonuses = b2.find_matches()

    expected_removals = [(0, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 2, 0, 2, 0), (0, 4, 0, 0, 0)]
    expected_bonuses = []

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_1_3_use_bonus_type_3():
    """
    TODO
    :return:
    """
    print('\n\nTest use bonus type 3:\n')


def test_1_4_use_4_match_intersect():
    """
    TODO
    :return:
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

    # find matches by calling get update twice
    bag = b2.get_update()
    bag = b2.get_update()
    print(bag)

    expected_removals = [(0, 2, 2, 0, 0), (1, 2, 2, 0, 0), (2, 0, 2, 0, 0), (2, 1, 2, 0, 0), (3, 2, 2, 0, 0)]
    expected_bonuses = [(2, 2, 2, 1, 0)]

    actual_removals = bag.removals
    actual_bonuses = bag.bonuses

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_1_5_use_bonus_3_intersect():
    """
    TODO
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

    # find matches by calling get update twice
    bag = b2.get_update()
    bag = b2.get_update()
    print(bag)

    expected_removals = [(0, 2, 2, 0, 0), (1, 1, 1, 0, 0), (1, 2, 2, 0, 0), (1, 3, 1, 0, 0), (2, 0, 2, 0, 0),
                         (2, 1, 2, 0, 0), (2, 3, 0, 0, 0)]
    expected_bonuses = [(2, 2, 2, 3, 0)]

    actual_removals = bag.removals
    actual_bonuses = bag.bonuses

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_1_6_use_bonus_2_get_bonus_1():
    """
    Testing that a bonus type 1 is still
    created when using a bonus type 2.

    Bonus type 1 occurs from 4 in a row.
    Bonus type 2 destroys all gems of that type.
    :return:
    """
    print('\n\nTest 1.6 using a start bonus and getting a match 4:\n')

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


def test_1_7_use_bonuses_when_removed_by_bonus():
    """
    TODO
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


def test_2_1_ice_removed():
    print("\nBoard 1:\n")
    print(b)

    swap_locations = [(0, 0), (0, 1)]
    b.set_swap_locations(swap_locations)

    print("\nbag 1:\n")
    bag = b.get_update()
    print(bag)

    print("\nbag 2:\n")
    bag = b.get_update()
    print(bag)

    print("\nbag 3:\n")
    bag = b.get_update()
    print(bag)

    print("\nbag 4:\n")
    bag = b.get_update()
    print(bag)

    print("\nbag 5:\n")
    bag = b.get_update()
    print(bag)

    print("\nBoard 2:\n")
    print(b)  #
    # ice should be like this
    ice_grid = [[-1] * columns0 for _ in range(rows0)]
    current_ice = b0.ice_grid.grid
    assert current_ice == ice_grid


def test_2_2_medals_removed():
    medal_grid = [[-1] * columns0 for _ in range(rows0)]
    current_medals = b0.medal_grid.grid
    assert current_medals == medal_grid

