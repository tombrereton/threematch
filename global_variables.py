# ============================================
# Global Constants
# ============================================

# Game variables
LEVEL_1_TOTAL_MEDALS = 3
LEVEL_2_TOTAL_MEDALS = 4
LEVEL_3_TOTAL_MEDALS = 5
SCORE = 0
MOVES_LEFT = 36

# GUI variables
HD_SCALE = 1  # Scale for changing the number of pixels
CELL_SIZE = int(30 * HD_SCALE)  # Width of each shape (pixels).
MARGIN = int(70 * HD_SCALE)  # Margin around the board (pixels).
TEXT_AREA = int(75 * HD_SCALE)
PUZZLE_ROWS = 9  # Number of rows on the board.
PUZZLE_COLUMNS = 15  # Number of columns on the board.
WINDOW_WIDTH = PUZZLE_COLUMNS * CELL_SIZE + 2 * MARGIN
WINDOW_HEIGHT = PUZZLE_ROWS * CELL_SIZE + 2 * MARGIN + TEXT_AREA
ANIMATION_SCALE = 20


# Testing
TEST = False
