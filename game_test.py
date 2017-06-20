from events import *
from game import Board

rows0 = 2
columns0 = 3
ice_rows0 = 2
medals0 = 1
moves_left0 = 30

event_manager = EventManager()
b0 = Board(rows0, columns0, ice_rows0, medals0, moves_left0, test='horizontal', event_manager=event_manager)

rows1 = 1
columns1 = 5
ice_rows1 = 0
medals1 = 0
moves_left1 = 30

event_manager = EventManager()
b1 = Board(rows1, columns1, ice_rows1, medals1, moves_left1, test='horizontal', event_manager=event_manager)

rows2 = 1
columns2 = 5
ice_rows2 = 0
medals2 = 0
moves_left2 = 30

event_manager = EventManager()
b2 = Board(rows2, columns2, ice_rows2, medals2, moves_left2, test='horizontal', event_manager=event_manager)


def test_use_bonus_type_1():
    """
    Should remove all gems in row and create no bonuses
    :return:
    """
    print('\n\nTest use bonus type 1:\n')

    # Set up grid for testing
    b1.gem_grid.grid[0][3] = (0, 1, 0)
    b1.gem_grid.grid[0][4] = (1, 0, 0)

    # swap to allow matches to be found
    swap_locations = [(0, 0), (0, 1)]
    b1.set_swap_locations(swap_locations)

    # find matches by calling get update twice
    bag1 = b1.get_update()
    bag = b1.get_update()

    expected_removals = [(0, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 1, 0), (0, 4, 1, 0, 0)]
    expected_bonuses = []

    actual_removals = bag.removals
    actual_bonuses = bag.bonuses

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_use_bonus_type_2():
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


def test_use_bonus_type_3():
    """
    TODO
    :return:
    """
    print('\n\nTest use bonus type 3:\n')

    # Set up grid for testing

    # swap to allow matches to be found
    swap_locations = [(0, 0), (0, 1)]

    # find matches by calling get update twice
    bag = b1.get_update()

    expected_removals = [(0, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 1, 0), (0, 4, 1, 0, 0)]
    expected_bonuses = []

    actual_removals = bag.removals
    actual_bonuses = bag.bonuses

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_use_4_match_intersect():
    """
    TODO
    :return:
    """
    print('\n\nTest 4 match intersect:\n')

    # Set up grid for testing

    # swap to allow matches to be found
    swap_locations = [(0, 0), (0, 1)]

    # find matches by calling get update twice
    bag = b1.get_update()

    expected_removals = [(0, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 1, 0), (0, 4, 1, 0, 0)]
    expected_bonuses = []

    actual_removals = bag.removals
    actual_bonuses = bag.bonuses

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_ice_removed():
    print("\nBoard 1:\n")
    print(b0)

    swap_locations = [(0, 0), (0, 1)]
    b0.set_swap_locations(swap_locations)

    print("\nbag 1:\n")
    bag = b0.get_update()
    print(bag)

    print("\nbag 2:\n")
    bag = b0.get_update()
    print(bag)

    print("\nbag 3:\n")
    bag = b0.get_update()
    print(bag)

    print("\nbag 4:\n")
    bag = b0.get_update()
    print(bag)

    print("\nbag 5:\n")
    bag = b0.get_update()
    print(bag)

    print("\nBoard 2:\n")
    print(b0)  #
    # ice should be like this
    ice_grid = [[-1] * columns0 for _ in range(rows0)]
    current_ice = b0.ice_grid.grid
    assert current_ice == ice_grid


def test_medals_removed():
    medal_grid = [[-1] * columns0 for _ in range(rows0)]
    current_medals = b0.medal_grid.grid
    assert current_medals == medal_grid
