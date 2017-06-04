"""
background image credit:
Designed by Freepik
http://www.freepik.com

asset credit:
1001.com
"""

import pygame
from pygame.locals import *

import board as b
from background import Background
from game_state import GameState
from global_variables import CELL_SIZE, MARGIN, PUZZLE_ROWS, PUZZLE_COLUMNS, WINDOW_WIDTH, WINDOW_HEIGHT, TEST, \
    ANIMATION_SCALE

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


# ============================================
# locator functions
# ============================================
def getLeftTopOfTile(tile_x, tile_y):
    left = (tile_x * CELL_SIZE) + (tile_x - 1)
    top = (tile_y * CELL_SIZE) + (tile_y - 1)
    return (left, top)


def get_gem_location_from_click(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for i in range(0, PUZZLE_ROWS):
        for j in range(0, PUZZLE_COLUMNS):
            gemRect = pygame.Rect(board.get_gem(i, j).rect)
            if gemRect.collidepoint(x, y):
                return i, j
                # c.MOVES_LEFT = c.MOVES_LEFT - 1
                # board.swap_gems(i, j, "up")
                # return board.get_gem(i, j).punched()
    return None, None


# ============================================
# event loop
# ============================================

def check_events(board: b.Board, bg: Background, game_state: GameState, screen: pygame.display,
                 gem_row: int,
                 gem_column: int):
    """
    This function loops of the events from the event queue.

    If there are 2 clicks of neighbouring gems, it tries to swap them.
    :param game_state:
    :param bg:
    :param gem_column:
    :param gem_row:
    :param board:
    :param game_over_text:
    :param going:
    :param screen:
    :param text_pos:
    :return:
    """

    # for event in pygame.event.get():
    #     if game_state.state in {"animate_swap", "animate_explode", "animate_pull_down"}:
    #
    #         # ignore events while animating
    #         # do we want to set this to return None?
    #         return bg, game_state, gem_row, gem_column
    #
    #     elif event.type == QUIT:
    #         # quit
    #         game_state.stop_going()
    #
    #     elif c.MOVE_LEFT == 0:
    #         # game over
    #         bg.set_game_over_text()
    #         screen.blit(bg.game_over_text, bg.game_over_text_pos)
    #
    #     elif event.type == KEYDOWN and event.key == K_ESCAPE:
    #         # quit
    #         game_state.stop_going()
    #
    #     elif event.type == MOUSEBUTTONDOWN:
    #
    #         if game_state.state == "user_clicked":
    #             # second click, if valid move, change state to animate_move
    #             # if it is not a valid move, change state to empty
    #             # this is done within the GameState class
    #             second_gem_row, second_gem_column = get_gem_location_from_click(board, event.pos[0], event.pos[1])
    #             game_state.animate_swap(second_gem_row, second_gem_row)
    #
    #         elif game_state.state == "empty":
    #             # first click, get coordinates and save them to game state object
    #             # change state to user_clicked
    #             gem_row, gem_column = get_gem_location_from_click(board, event.pos[0], event.pos[1])
    #             game_state.user_clicked(gem_row, gem_column)

    for event in pygame.event.get():
        if event.type == QUIT:
            game_state.stop_going()
        elif game_state.moves_left == 0:
            bg.set_game_over_text()
            screen.blit(bg.game_over_text, bg.game_over_text_pos)
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            game_state.stop_going()
        elif event.type == MOUSEBUTTONDOWN:
            # get gem coordinates if user clicks
            if gem_row is None and gem_column is None:
                # if use has not clicked yet, get the first gem coordinates
                gem_row, gem_column = get_gem_location_from_click(board, event.pos[0], event.pos[1])

            else:
                # if user has already clicked, get the second gem coordinates
                second_gem_row, second_gem_column = get_gem_location_from_click(board, event.pos[0], event.pos[1])

                # we check if the second gem is a neighbouring gem, swap it if so
                if second_gem_row == gem_row - 1 and second_gem_column == gem_column:
                    # swap up
                    board.swap_gems(gem_row, gem_column, "up")
                    number_of_matches = board.check_matches(False)
                    if number_of_matches == 0:
                        board.swap_gems(gem_row, gem_column, "up")
                    else:
                        game_state.moves_left = game_state.moves_left - 1

                    gem_row = None
                    gem_column = None

                elif second_gem_row == gem_row + 1 and second_gem_column == gem_column:
                    # swap down
                    board.swap_gems(gem_row, gem_column, "down")
                    number_of_matches = board.check_matches(False)
                    if number_of_matches == 0:
                        board.swap_gems(gem_row, gem_column, "down")
                    else:
                        game_state.moves_left = game_state.moves_left - 1
                    gem_row = None
                    gem_column = None

                elif second_gem_row == gem_row and second_gem_column == gem_column + 1:
                    # swap right
                    board.swap_gems(gem_row, gem_column, "right")
                    number_of_matches = board.check_matches(False)
                    if number_of_matches == 0:
                        board.swap_gems(gem_row, gem_column, "right")
                    else:
                        game_state.moves_left = game_state.moves_left - 1
                    gem_row = None
                    gem_column = None

                elif second_gem_row == gem_row and second_gem_column == gem_column - 1:
                    # swap down
                    board.swap_gems(gem_row, gem_column, "left")
                    number_of_matches = board.check_matches(False)
                    if number_of_matches == 0:
                        board.swap_gems(gem_row, gem_column, "left")
                    else:
                        game_state.moves_left = game_state.moves_left - 1
                    gem_row = None
                    gem_column = None

                else:
                    # if the second gem is not a neighbouring gem, set the gem coordinates to none
                    gem_row = None
                    gem_column = None

    return bg, game_state, gem_row, gem_column


def animate_loop(board: b.Board, screen, bg: Background, clock: pygame.time.Clock(), game_state: GameState):
    """
    This function animates the sprites then sets the game_state depending on its current states.
    :param board:
    :param screen:
    :param bg:
    :param clock:
    :return:
    """
    for i in range(ANIMATION_SCALE):
        # loop the number of times we need to animate given
        # by ANIMATION_SCALE

        # Call the update method on the sprites
        board.get_gem_group().update()
        board.get_ice_group().update()
        board.get_medal_group().update()

        # Draw background and text
        bg.set_moves_left()
        screen.blit(bg.background, (0, 0))
        screen.blit(bg.moves_left_text, (10, WINDOW_HEIGHT - MARGIN * 3 / 4))
        screen.blit(bg.score_text, (10, WINDOW_HEIGHT - MARGIN / 3))

        # Draw sprites
        board.get_medal_group().draw(screen)
        board.get_ice_group().draw(screen)
        board.get_gem_group().draw(screen)

        # Draw game over text
        screen.blit(bg.game_over_text, bg.game_over_text_pos)

        # update the entire screen
        pygame.display.flip()

        # never run quicker than 60 frames per second
        clock.tick(60)

    # change game state
    if game_state.state == "animate_swap":
        game_state.check_matches()
    elif game_state.state == "animate_reverse":
        game_state.empty()
    elif game_state.state == "animate_explode":
        game_state.remove_gems()
    elif game_state.state == "animate_pull_down":
        game_state.check_matches()

    return game_state


# ============================================
# main
# ============================================
def main():
    """
    Initialising game
    :return:
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Gem Island")

    # total moves allowed in game
    moves_left = 16
    # game state object to store current state
    game_state = GameState(moves_left)
    # background object to store background and text
    bg = Background(game_state)

    # create the background
    screen.blit(bg.background, (0, 0))

    # Put Text On The Background
    if pygame.font:
        screen.blit(bg.moves_left_text, (10, WINDOW_HEIGHT - MARGIN * 3 / 4))
        screen.blit(bg.score_text, (10, WINDOW_HEIGHT - MARGIN / 3))

    # create the board
    board = b.Board(screen, bg.background, PUZZLE_ROWS, PUZZLE_COLUMNS, CELL_SIZE, MARGIN)

    # change to test board if true
    if TEST:
        board.remove_all()
        board.get_gem_group().update()
        board.get_gem_group().draw(screen)
        board.test_board()
        board.get_gem_group().update()
        board.get_gem_group().draw(screen)

    # flip the screen after adding everything to it
    pygame.display.flip()

    clock = pygame.time.Clock()

    # declare clicked gems to none
    gem_row = None
    gem_column = None

    # check for matches
    if not TEST:
        board.check_matches(True)

    while game_state.going:
        # Frames per second
        clock.tick(60)

        # loop over events
        bg, game_state, gem_row, gem_column = check_events(board, bg, game_state, screen, gem_row, gem_column)

        if game_state.state in {"animate_swap", "animate_reverse", "animate_explode", "animate_pull_down"}:
            # start animation if in animation state
            animate_loop(board, screen, bg, clock, game_state)

        # Update groups
        board.get_gem_group().update()
        board.get_ice_group().update()
        board.get_medal_group().update()

        # Draw Everything

        # Draw background and text
        bg.set_moves_left()
        screen.blit(bg.background, (0, 0))
        screen.blit(bg.moves_left_text, (10, WINDOW_HEIGHT - MARGIN * 3 / 4))
        screen.blit(bg.score_text, (10, WINDOW_HEIGHT - MARGIN / 3))

        # Draw sprites
        board.get_medal_group().draw(screen)
        board.get_ice_group().draw(screen)
        board.get_gem_group().draw(screen)

        # Draw game over text
        screen.blit(bg.game_over_text, bg.game_over_text_pos)

        # Show drawn objects
        pygame.display.flip()


if __name__ == '__main__':
    main()
