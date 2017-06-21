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
    5 gems in a row. 3 gems of type 0.
    Then 1 gem of type 0 and bonus type 1 (removes entire row).
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


def test_1_3_use_bonus_type_3():
    """
    TODO
    :return:
    """
    print('\n\nTest use bonus type 3:\n')


def test_1_4_use_4_match_intersect():
    """
    Vertical is a 4 in a row, therefore getting a type 1 bonus
    Horizontal is a normal 3 match.

    The vertical and horizontal matches intersect.

    This should result in all matches being removed except for the
    swap position (the intersection point in this case), where a
    type 1 bonus is created.

    FYI, type 1 bonus removes entire row/column.
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
    Vertical is a three in a row.

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


def test_1_7_use_bonuses_when_removed_by_bonus():
    """
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


def test_1_8_swap_in_bonus_and_activate_vertical():
    """
    Testing activating a cross bonus (type 1)
    when being swapped in.

    5 gems in a column. 2 gems of type 0,
    then a gem of type 1, then a cross gem of
    type 0, then a gem of type 1.

    All 5 gems should be removed.
    :return:
    """
    print('\n\nTest 1.8 swap in a cross bonus and removing all gems vertically:\n')

    b2 = Board(rows=5, columns=1, ice_rows=0, medals=0, moves=10, gem_types=3, test='vertical',
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


def test_1_9_swap_in_bonus_and_activate_horizontal():
    """
    Testing activating a cross bonus (type 1)
    when being swapped in.

    5 gems in a row. 2 gems of type 0,
    then a gem of type 1, then a cross gem of
    type 0, then a gem of type 1.

    All 5 gems should be removed.
    :return:
    """
    print('\n\nTest 1.9 swap in a cross bonus and removing all gems horizontally:\n')

    b2 = Board(rows=1, columns=5, ice_rows=0, medals=0, moves=10, gem_types=3, test='horizontal',
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


def test_1_10_swap_in_bonus_from_above_and_activate_horizontal():
    """
    Testing activating a cross bonus (type 1)
    when being swapped in.

    Grid is 2 by 5.

    Second row should all be removed except for swap location
    which should create a bonus.
    :return:
    """
    print('\n\nTest 1.10 swap in a cross bonus from above and remove all gems horizontally:\n')

    b2 = Board(rows=2, columns=5, ice_rows=0, medals=0, moves=10, gem_types=3, test='horizontal',
               event_manager=event_manager)

    # Set up grid for testing
    b2.gem_grid.grid[0][1] = (1, 1, 0)
    b2.gem_grid.grid[0][2] = (1, 0, 0)
    b2.gem_grid.grid[1][1] = (0, 0, 0)
    b2.gem_grid.grid[1][4] = (0, 0, 0)
    print(b2)

    swap_locations = [(0, 1), (1, 1)]
    b2.set_swap_locations(swap_locations)
    b2.swap_gems()

    print(b2)

    expected_removals = [(1, 0, 1, 0, 0), (1, 2, 1, 0, 0), (1, 3, 1, 0, 0), (1, 4, 0, 0, 0)]
    expected_bonuses = [(1, 1, 1, 1, 0)]

    actual_removals, actual_bonuses = b2.find_matches()

    assert expected_removals == actual_removals
    assert expected_bonuses == actual_bonuses


def test_1_11_diamond_grid():
    """
    Should remove all gems
    :return:
    """

    print('\n\nTest 1.11 grid full of diamonds, remove all:\n')

    b2 = Board(rows=3, columns=3, ice_rows=0, medals=0, moves=10, gem_types=1, test='horizontal',
               event_manager=event_manager)
    print(b2)

    actual_removed, actual_bonus = b2.find_matches()
    b2.match_list = actual_removed
    b2.bonus_list = actual_bonus
    b2.remove_gems_add_bonuses()


    print('\n\n second:\n')
    print(actual_removed)
    print(actual_bonus)

def test_2_1_ice_removed():
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
    current_ice = b.ice_grid.grid
    assert current_ice == ice_grid


def test_2_2_medals_removed():
    """
    Testing that all medals are removed
    when gems matched on top of ice.

    All gems should match, remove the ice,
    and free the medal underneath.

    Grid is 2 by 3.
    :return:
    """
    medal_grid = [[-1] * columns0 for _ in range(rows0)]
    current_medals = b.medal_grid.grid
    assert current_medals == medal_grid


def test_2_3_remove_ice_when_creating_bonus():
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

    b2 = Board(rows=1, columns=4, ice_rows=1, medals=0, moves=10, gem_types=3, test='horizontal',
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
