from game import Board

rows = 2
columns = 3
ice_rows = 2
medals = 1
moves_left = 30

b = Board(rows, columns, ice_rows, medals, moves_left, test='horizontal')


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
