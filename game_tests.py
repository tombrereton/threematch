from game import Board

# class GameTest(unittest.TestCase):


if __name__ == '__main__':
    # unittest.main
    rows = 2
    columns = 3
    ice_rows = 2
    medals = 1
    moves_left = 30
    b = Board(rows, columns, ice_rows, medals, moves_left, test='horizontal')

    print("Board 1:\n")
    print(b)

    swap_locations = [(0, 0), (0, 1)]
    b.set_swap_locations(swap_locations)

    print("bag 1:\n")
    bag = b.get_update()
    print(bag)

    print("bag 2:\n")
    bag = b.get_update()
    print(bag)

    print("bag 3:\n")
    bag = b.get_update()
    print(bag)

    print("bag 4:\n")
    bag = b.get_update()
    print(bag)

    print("Board 2:\n")
    print(b)
