#тут будет просто подготовка (в виде разбиения на дни) таблицы для разбиения на дни
#То есть просто просто словарь списков по дням неделям

from GoogleSheet import *
from WorkingTime import *


#Да я вручную проставлял, я псих.
LETTER_COORD_AND_WORKING_TIME_FOR_EACH_CLASS = {
    "5мл":   ['E',  WORKING_TIME1],
    "6мл":   ['J',  WORKING_TIME1],
    "7мл":   ['O',  WORKING_TIME1],
    "8м":    ['T',  WORKING_TIME1],

    "9м":    ['AB', WORKING_TIME2],
    "10м":   ['AG', WORKING_TIME2],
    "11м":   ['AL', WORKING_TIME2],
    "8хб":   ['AQ', WORKING_TIME2],
    "9хб":   ['AV', WORKING_TIME2],
    "10хб":  ['BA', WORKING_TIME2],
    "11хб":  ['BF', WORKING_TIME2],

    "8г":    ['BN', WORKING_TIME3],
    "9г":    ['BS', WORKING_TIME3],
    "10г":   ['BX', WORKING_TIME3],
    "11г":   ['CC', WORKING_TIME3],

}

def get_lesson_time(class_name: str, lesson_idx: int):
    return LETTER_COORD_AND_WORKING_TIME_FOR_EACH_CLASS[class_name][1].get_lesson_time(lesson_idx)


NUMBER_COORD_FOR_DAY_OF_THE_WEEK = {
    'ПН': 10,
    'ВТ': 20,
    'СР': 30,
    'ЧТ': 40,
    'ПТ': 50,
    'СБ': 60,
    'ВС': 70,

}



def get_day(student_class: str, day_of_the_week: str):
    l = [[NONE_CELL] * 4 for _ in range(MAX_LESSONS_PER_DAY)]

    cell_coord = CellCoord(LETTER_COORD_AND_WORKING_TIME_FOR_EACH_CLASS[student_class][0],
                           NUMBER_COORD_FOR_DAY_OF_THE_WEEK[day_of_the_week])


    for i in range(MAX_LESSONS_PER_DAY):
        cell_coord.add_val_to_number_coord(1)
        for j in range(4):
            l[i][j] = SCHOOL_TABLE.get_cell(cell_coord)
            cell_coord.add_val_to_letters_coord(1)
        cell_coord.add_val_to_letters_coord(-4)

    return l

