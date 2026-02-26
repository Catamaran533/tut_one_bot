from GoogleSheet import *
from cell_coord import *

MAX_LESSONS_PER_DAY = 8

class WorkingTime:
    def __init__(self, cell_coord: CellCoord):
        l = [""] * MAX_LESSONS_PER_DAY
        for i in range(MAX_LESSONS_PER_DAY):
            cell_coord = cell_coord.add_val_to_number_coord(1)
            for j in range(3):
                l[i] += SCHOOL_TABLE.get_cell(cell_coord).get_text()
                cell_coord = cell_coord.add_val_to_letters_coord(1)
            cell_coord = cell_coord.add_val_to_letters_coord(-3)
        self.__lessons_time = l

    def get_lesson_time(self, idx: int):
        return self.__lessons_time[idx]


WORKING_TIME1 = WorkingTime(CellCoord("A", 10))
WORKING_TIME2 = WorkingTime(CellCoord("X", 10))
WORKING_TIME3 = WorkingTime(CellCoord("BJ", 10))