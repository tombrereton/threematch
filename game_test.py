from events import *
from game import Board

rows = 2
columns = 3
ice_rows = 2
medals = 1
moves_left = 30

event_manager = EventManager()
b = Board(rows, columns, ice_rows, medals, moves_left, test='horizontal', event_manager=event_manager)

rows1 = 1
columns1 = 5
ice_rows1 = 0
medals1 = 0
moves_left1 = 30

event_manager = EventManager()
b1 = Board(rows1, columns1, ice_rows1, medals1, moves_left1, test='horizontal', event_manager=event_manager)


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
    ice_grid = [[-1] * columns for _ in range(rows)]
    current_ice = b.ice_grid.grid
    assert current_ice == ice_grid


def test_medals_removed():
    medal_grid = [[-1] * columns for _ in range(rows)]
    current_medals = b.medal_grid.grid
    assert current_medals == medal_grid
