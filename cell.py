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


WHITE_COLOR = ColorRGB()


class Cell:
    def __init__(self, cell_coord, text, color):
        self.__cell_coord = cell_coord
        self.__text = text
        self.__color = color

    def get_text(self):
        return self.__text

    def get_color(self):
        return self.__color

    def get_cell_coord(self):
        return self.__cell_coord

    def __str__(self):          #Для дебага
        return (
                f"ADDRESS = '{self.__cell_coord.get_cell_address()}', \n"
                f"TEXT = '''{self.__text}''', \n"
                f"COLOR = ColorRGB({self.__color.get_red():.2f}, {self.__color.get_green():.2f}, {self.__color.get_blue():.2f}))"
        )

NONE_CELL = Cell(CellCoord(-1, -1), "", ColorRGB())