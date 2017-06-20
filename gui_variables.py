import global_variables as gv


class GUIVariables:

    def __init__(self, rows: int, columns: int, hd_scale: float, base_cell_size: int, gem_ratio: float, base_margin: int,
                base_text_area: int, animation_scale: int, explosion_frames: int):
        self.rows = rows
        self.columns = columns
        self.hd_scale = hd_scale
        self.cell_size = int(self.hd_scale * base_cell_size)
        self.gem_size = int(gem_ratio * self.cell_size)
        self.gem_offset = (self.cell_size - self.gem_size) // 2
        self.medal_size = 2 * self.cell_size
        self.margin = int(self.hd_scale * base_margin)
        self.text_area = int(self.hd_scale * base_text_area)
        self.width = 2 * self.margin + self.columns * self.cell_size
        self.height = 2 * self.margin + self.rows * self.cell_size + self.text_area
        self.animation_scale = animation_scale
        self.explosion_frames = explosion_frames

    def default():
        return GUIVariables(gv.PUZZLE_ROWS, gv.PUZZLE_COLUMNS, gv.HD_SCALE, gv.BASE_CELL_SIZE, gv.GEM_RATIO,
                            gv.BASE_MARGIN, gv.BASE_TEXT_AREA, gv.ANIMATION_SCALE, gv.EXPLOSION_FRAMES)

    def pixel_to_grid(self, y_coord: int, x_coord: int):
        """
        Method to calculate the row and column from pixel coordinates.
        :param y_coord: Pixel y coordinate
        :param x_coord: Pixel x coordinate
        :return: A tuple of the grid coordinates (y, x)
        """
        row = (y_coord - self.margin) // self.cell_size
        column = (x_coord - self.margin) // self.cell_size
        row = row if row in range(self.rows) else -1
        column = column if column in range(self.columns) else -1
        return row, column
