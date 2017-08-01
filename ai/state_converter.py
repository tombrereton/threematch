from model.game import Grid
from itertools import product
from ai.medal_placer import medal_grid_filler
from copy import deepcopy


def gems_from_state(state, rows=None, cols=None):
    if not rows or not cols:
        rows = range(len(state) - 1)
        cols = range(len(state[0]))

    return [[state[i][j][0] for j in rows] for i in cols]


def gems_plus_from_state(state, rows=None, cols=None):
    if not rows or not cols:
        rows = range(len(state) - 1)
        cols = range(len(state[0]))

    return [[(state[i][j][0], state[i][j][1], 0) for j in rows] for i in cols]


def ice_from_state(state, rows=None, cols=None):
    if not rows or not cols:
        rows = range(len(state) - 1)
        cols = range(len(state[0]))

    return [[state[i][j][2] for j in rows] for i in cols]


def medals_from_state(state, rows=None, cols=None):
    if not rows or not cols:
        rows = range(len(state) - 1)
        cols = range(len(state[0]))

    return [[state[i][j][3] for j in rows] for i in cols]


def state_to_grids(state):
    rows = range(len(state) - 1)
    cols = range(len(state[0]))

    gem_grid_wrapper = Grid(0, 0)
    ice_grid_wrapper = Grid(0, 0)
    medal_grid_wrapper = Grid(0, 0)

    moves_medals = state[-1]

    gem_grid = gems_plus_from_state(state, rows, cols)
    ice_grid = ice_from_state(state, rows, cols)
    medal_grid = medals_from_state(state, rows, cols)
    medal_grid = medal_grid_filler(ice_grid, medal_grid, moves_medals[1]).__next__()

    gem_grid_wrapper.grid = gem_grid
    ice_grid_wrapper.grid = ice_grid
    medal_grid_wrapper.grid = medal_grid

    return gem_grid_wrapper.grid, ice_grid_wrapper.grid, medal_grid_wrapper.grid, moves_medals


def start_state(state):
    gem_grid, ice_grid, medal_grid, moves_medals = state
    medal_grid = medal_grid_filler(ice_grid, medal_grid, moves_medals[1]).__next__()

    return deepcopy(gem_grid), deepcopy(ice_grid), medal_grid, moves_medals
