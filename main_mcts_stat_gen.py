import sys
from time import time

from ai.state_functions import pick_move
from controller.controllers import CPUSpinnerController, NaiveAIControllerV1
from events.event_manager import EventManager
from global_variables import *
from model.game import Board


# ------------------------------------------------------------------------------
# logging.basicConfig(filename='game.log', filemode='w', level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
# ------------------------------------------------------------------------------
def main(g_limit, m_limit, stats_file_path=None):
    """..."""

    if len(sys.argv) > 1:
        game_limit, move_limit, c = sys.argv[0], sys.argv[1], sys.argv[2]
    else:
        game_limit, move_limit, c = g_limit, m_limit, 1.4

    # append scores and hyper params to file
    line = f'\nRandom, {game_limit}, {move_limit}, {c}, '
    with open(stats_file_path, 'a') as file:
        file.write(line)

    # gui_vars = GUIVariables.from_global()
    event_manager = EventManager()

    # ai controller setup
    # board_simulator = BoardSimulator()
    # eval_function_object = EvaluationFunction(model_path='ai/data/value_network_outcome_labels.h5')
    # eval_function = eval_function_object.evaluation_simple_conv_NN
    # mc = MonteCarlo(board_simulator=board_simulator,
    #                 game_limit=game_limit,
    #                 move_limit=move_limit,
    #                 c=c,
    #                 policy=AllPolicy(),
    #                 eval_function=eval_function,
    #                 print_move_ratings=False)
    # mcts_cont = MonteCarloController(event_manager=event_manager,
    #                                  monte_carlo_move_finder=mc,
    #                                  quit_on_no_moves=True)

    # mouse controller setup
    # mouse_cont = MouseController(event_manager, gui_vars)

    # board setup
    game_board = Board(rows=PUZZLE_ROWS,
                       columns=PUZZLE_COLUMNS,
                       ice_rows=ICE_ROWS,
                       medals_remaining=LEVEL_1_TOTAL_MEDALS,
                       moves_remaining=MOVES_LEFT,
                       event_manager=event_manager,
                       stats_file_path=stats_file_path)

    ai_cont = NaiveAIControllerV1(event_manager, game_board, pick_move, quit_on_no_moves=True)

    # view setup
    # view = GUI(gui_vars, *game_board.state(), event_manager=event_manager)

    # spinner setup
    spinner = CPUSpinnerController(event_manager)
    spinner.run()


if __name__ == "__main__":
    file_name = 'heuristic_tuning.csv'
    heading = 'Type, GameLimit, MoveLimit, C, Win, MedalLeft, MovesMade, Score, Duration\n'
    write_heading = False
    with open(file_name, 'r') as file:
        first = file.readline()
        if first != heading:
            write_heading = True

    if write_heading:
        with open(file_name, 'a') as file:
            file.write(heading)

    for g_limit in ['-']:
        for m_limit in ['-']:
            for i in range(100):
                start_time = time()
                main(g_limit=g_limit, m_limit=m_limit, stats_file_path=file_name)
                duration = time() - start_time
                line = f', {duration:4.3f}'
                print(f'Finished g: {g_limit}, m: {m_limit}, round: {i}, in time: {duration:4.3f}')
                with open(file_name, 'a') as file:
                    file.write(line)
