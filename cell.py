from cell_coord import *

EPSILON = 0.00001


class ColorRGB:
    def __init__(self, red=1.0, green=1.0, blue=1.0):  # числа от 0 до 1
        self.__red = red
        self.__green = green
        self.__blue = blue

    def get_red(self):
        return self.__red

    def set_red(self, new_red):
        self.__red = new_red

    def get_green(self):
        return self.__green

    def set_green(self, new_green):
        self.__green = new_green

    def get_blue(self):
        return self.__blue

    def set_blue(self, new_blue):
        self.__blue = new_blue

    def __eq__(self, other):  # ==
        colors = [self.__red, self.__green, self.__blue]
        other_colors = [other.get_red(), other.get_green(), other.get_blue()]
        for i in range(len(colors)):
            if abs(colors[i] - other_colors[i]) > EPSILON:
                return False
        return True

    def __ne__(self, other):  # !=
        colors = ColorRGB(self.__red, self.__green, self.__blue)
        return not (colors == other)

    def __str__(self):
        return f"[{self.__red}, {self.__green}, {self.__blue}]"


WHITE_COLOR = ColorRGB()


class Cell:
    def __init__(self, cell_coord, text, color, merge_start_cell_coord=None, merge_end_cell_coord=None):
        self.__cell_coord = cell_coord
        self.__text = text
        self.__color = color

        if merge_start_cell_coord is None:
            self.__merge_start_cell_coord = cell_coord
        else:
            self.__merge_start_cell_coord = merge_start_cell_coord

        if merge_end_cell_coord is None:
            self.__merge_end_cell_coord = cell_coord
        else:
            self.__merge_end_cell_coord = merge_end_cell_coord

    def get_text(self):
        return self.__text

    def get_color(self):
        return self.__color

    def get_cell_coord(self):
        return self.__cell_coord

    def get_merge_start_cell_coord(self):
        return self.__merge_start_cell_coord

    def get_merge_end_cell_coord(self):
        return self.__merge_end_cell_coord

    def set_merge_range(self, merge_start_cell_coord, merge_end_cell_coord):
        self.__merge_start_cell_coord = merge_start_cell_coord
        self.__merge_end_cell_coord = merge_end_cell_coord


    def is_merge_main_cell(self):
        return self.__cell_coord.get_cell_address() == self.__merge_start_cell_coord.get_cell_address()

    def get_merged_cells_list(self):

        ans = []

        start_col = self.__merge_start_cell_coord.get_letters_coord()
        end_col = self.__merge_end_cell_coord.get_letters_coord()
        start_row = self.__merge_start_cell_coord.get_numbers_coord()
        end_row = self.__merge_end_cell_coord.get_numbers_coord()

        for col in range(start_col, end_col + 1):
            for row in range(start_row, end_row + 1):
                ans.append(CellCoord(col, row))

        return ans

    def __str__(self):
        l = []
        try:
            merged_cells = self.get_merged_cells_list()
            for cell_coord in merged_cells:
                l.append(cell_coord.get_cell_address())
        except Exception as e:
            l = [f"Ошибка при получении списка объединенных ячеек: {e}"]
            print_crash(f"Ошибка при получении списка объединенных ячеек: {e}")

        ans = (
            f"ADDRESS = '{self.__cell_coord.get_cell_address()}', \n"
            f"TEXT = '''{self.__text}''', \n"
            f"COLOR = ColorRGB({self.__color.get_red():.2f}, {self.__color.get_green():.2f}, {self.__color.get_blue():.2f}), \n"
            f"MERGE_RANGE = {l}, \n"
            f"IS_MERGED_MAIN_CELL = {self.is_merge_main_cell()} \n"
        )

        return ans


NONE_CELL = Cell(CellCoord(-1, -1), "", ColorRGB())