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
    ANIMATION_SCALE, MOVES_LEFT, LEVEL_1_TOTAL_MEDALS

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

def check_events(screen: pygame.display, board: b.Board, bg: Background, game_state: GameState):
    """
    This function loops of the events from the event queue and changes the game state.

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
    event = pygame.event.poll()

    if event.type == QUIT:
        # quit
        game_state.stop_going()

    elif game_state.medals_left == 0:
        # win
        bg.set_game_over_text(True)
        screen.blit(bg.game_over_text, bg.game_over_text_pos)

    elif event.type == KEYDOWN and event.key == K_ESCAPE:
        # quit
        game_state.stop_going()

    elif game_state.state == "pull_down":
        # Pull the gems downs
        repeat_pull_down = board.pull_gems_down()

        # Then set state to animate pull down
        if repeat_pull_down:
            game_state.animate_pull_down_repeat()
        else:
            game_state.animate_pull_down()

        pygame.event.clear()

    elif game_state.state == "remove_gems":
        # Gems have been exploded, remove the exploded gems
        medals_freed = board.remove_gems(game_state.match_list)

        # add bonuses if needed
        bonus_list = game_state.bonus_list
        medals_freed += board.update_bonus(bonus_list)

        # if medals freed, update counter on screen
        if medals_freed > 0:
            game_state.medal_freed(medals_freed)

        # update score
        points = board.get_points(game_state.match_list)
        bg.update_score(points)

        # Pull the gems downs
        repeat_pull_down = board.pull_gems_down()

        # Then set state to animate pull down
        if repeat_pull_down:
            game_state.animate_pull_down_repeat()
        else:
            game_state.animate_pull_down()

        pygame.event.clear()

    elif game_state.state == "check_matches":
        # A valid swap, check for matches
        # if we have more than 3 matches, explode gems
        # else set state to empty

        # get list of gem tuples
        match_list, bonus_list = board.find_matches(game_state.get_swaps())
        number_of_matches = len(match_list)

        if number_of_matches > 0:
            # if list length is greater than 0 pass into game_state
            game_state.animate_explode(number_of_matches, match_list, bonus_list)

            # set gems to explode
            board.explode_gems(match_list)
        else:
            game_state.empty()

        pygame.event.clear()

    elif game_state.state == "check_swap":
        # Check matches from the animate_swap state
        # if we have more than 3 matches, explode gems
        # else set state to empty

        match_list, bonus_list = board.find_matches(game_state.get_swaps())
        number_of_matches = len(match_list)

        if number_of_matches > 0:
            # move made if valid swap
            game_state.move_made()
            game_state.animate_explode(number_of_matches, match_list, bonus_list)

            # set gems to explode
            board.explode_gems(match_list)
        else:
            # Swap back if no match
            game_state.animate_reverse()
            row = game_state.row
            column = game_state.column
            direction = game_state.direction
            board.swap_gems(row, column, direction)

        pygame.event.clear()

    elif event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP]:

        # TODO: change so both drag and click work

        if game_state.state == "user_clicked":
            # second click, if valid move, change state to animate_move
            # if it is not a valid move, change state to empty
            # the GameState class works out if it is a valid move
            second_gem_row, second_gem_column = get_gem_location_from_click(board, event.pos[0], event.pos[1])
            game_state.animate_swap(second_gem_row, second_gem_column)

            if game_state.state == "animate_swap":
                # move gems if clicked on valid positions
                row = game_state.row
                column = game_state.column
                direction = game_state.direction
                board.swap_gems(row, column, direction)

        elif game_state.state == "empty" and event.type == MOUSEBUTTONDOWN:
            # first click, get coordinates and save them to game state object
            # change state to user_clicked
            gem_row, gem_column = get_gem_location_from_click(board, event.pos[0], event.pos[1])
            if gem_row is None or gem_column is None:
                game_state.empty()
            else:
                game_state.user_clicked(gem_row, gem_column)

    elif game_state.moves_left == 0:
        # game over
        bg.set_game_over_text()
        screen.blit(bg.game_over_text, bg.game_over_text_pos)

    return screen, board, bg, game_state


# ============================================
# animate loop
# ============================================

def animate_loop(screen, board: b.Board, bg: Background, game_state: GameState, clock: pygame.time.Clock()):
    """
    This function animates the sprites then sets the game_state depending on its current states.

    Future implementation: change the number of loops depending on the animation. This
    would require changing the respective update method to suit.
    :param game_state:
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
        bg.set_medals_left()
        screen.blit(bg.background, (0, 0))
        screen.blit(bg.moves_left_text, (10, WINDOW_HEIGHT - MARGIN * 3 / 4))
        screen.blit(bg.medals_left_text, (10, WINDOW_HEIGHT - MARGIN * 7 / 6))
        screen.blit(bg.score_text, (10, WINDOW_HEIGHT - MARGIN / 3))

        # Draw sprites
        board.get_medal_group().draw(screen)
        board.get_ice_group().draw(screen)
        board.get_gem_group().draw(screen)

        # Draw game over text
        screen.blit(bg.game_over_text, bg.game_over_text_pos)

        # update the entire screen
        pygame.display.flip()

        # pump events
        pygame.event.pump()

        # never run quicker than 60 frames per second
        clock.tick(60)

    # change game state
    if game_state.state == "animate_swap":
        game_state.check_swap()
    elif game_state.state == "animate_not_valid_swap":
        game_state.not_valid_swap()
    elif game_state.state == "animate_reverse":
        game_state.empty()
    elif game_state.state == "animate_explode":
        game_state.remove_gems()
    elif game_state.state == "animate_pull_down":
        game_state.check_matches()
    elif game_state.state == "animate_pull_down_repeat":
        game_state.pull_down()

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

    # game state object to store current state
    game_state = GameState(MOVES_LEFT, LEVEL_1_TOTAL_MEDALS)
    # background object to store background and text
    bg = Background(game_state)

    # allowed events in event queue
    pygame.event.set_allowed(MOUSEBUTTONDOWN)
    pygame.event.set_blocked(MOUSEMOTION)

    # create the background
    screen.blit(bg.background, (0, 0))

    # Put Text On The Background
    if pygame.font:
        screen.blit(bg.moves_left_text, (10, WINDOW_HEIGHT - MARGIN * 3 / 4))
        screen.blit(bg.medals_left_text, (10, WINDOW_HEIGHT - MARGIN * 7 / 6))
        screen.blit(bg.score_text, (10, WINDOW_HEIGHT - MARGIN / 3))

    # create the board
    board = b.Board(screen, bg, PUZZLE_ROWS, PUZZLE_COLUMNS, CELL_SIZE, MARGIN)

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

    # Create FPS clock
    clock = pygame.time.Clock()

    # check for matches if not test game
    if not TEST:
        board.check_matches(True)

    animate_loop(screen, board, bg, game_state, clock)

    while game_state.going:
        # Frames per second
        pygame.time.wait(1)

        if game_state.state in ["animate_swap", "animate_reverse", "animate_explode", "animate_pull_down",
                                "animate_not_valid_swap", "animate_pull_down_repeat"]:
            # start animation if in animation state
            game_state = animate_loop(screen, board, bg, game_state, clock)

        else:
            # loop over events
            screen, board, bg, game_state = check_events(screen, board, bg, game_state)

        pygame.display.flip()
        pygame.event.pump()


if __name__ == '__main__':
    main()
