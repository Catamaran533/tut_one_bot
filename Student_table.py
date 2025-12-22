from cell import *

#TODO переделать ВСЁ


HORIZONTAL_TABLE_SIZE = 4
MAX_LESSONS_PER_DAY = 8



def get_table(cell_coord):
    if (type(cell_coord) != CellCoord):
        print_crash("Косяк в StudentTable, вы передали не CellCoord в get_table")
        raise TypeError

    cell_coord.add_val_to_number_coord(1)
    l = [[None] * 4 for _ in range(8)]
    for i in range(MAX_LESSONS_PER_DAY):
        for j in range(HORIZONTAL_TABLE_SIZE):

            print(i, j)

            l[i][j] = Cell(cell_coord)
            cell_coord.add_val_to_letters_coord(1)
        cell_coord.add_val_to_number_coord(1)
        cell_coord.add_val_to_letters_coord(-HORIZONTAL_TABLE_SIZE)

    return l



class StudentTable:
    def __init__(self, cell_coord):            #Вы передаёте сюда координаты с названием класса, где ниже есть его расписание
        self.__class_name = Cell(cell_coord).get_text()



    def get_class(self):
        return self.__class_name

    def set_class(self, new_class):
        self.__class_name = new_class



a = get_table(CellCoord("E", 10))
for i in a:
    for j in i:
        print(j.get_text(), end=" ")
    print()