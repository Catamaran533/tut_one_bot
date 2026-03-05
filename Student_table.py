from cell import *
from SplittingDays import *
from StudentLesson import *
from consts import *
from Teachers_by_colors import get_teacher_by_color, have_color
from getting_teachers_and_lessons import *

HORIZONTAL_TABLE_SIZE = 4
MAX_LESSONS_PER_DAY = 8




class StudentDay:
    def __init__(self, class_name: str, day_of_the_week: str):
        l = get_day(class_name, day_of_the_week)
        class_table = [[StudentLesson("", [], [], ""), StudentLesson("", [], [], "")] for _ in range(MAX_LESSONS_PER_DAY)]
        for lesson_idx in range(MAX_LESSONS_PER_DAY):
            class_table[lesson_idx][0].set_lesson_name(get_lesson(l[lesson_idx][0].get_text()))
            class_table[lesson_idx][1].set_lesson_name(get_lesson(l[lesson_idx][2].get_text()))

            class_table[lesson_idx][0].set_teachers(get_teachers(l[lesson_idx][0].get_text()))
            class_table[lesson_idx][1].set_teachers(get_teachers(l[lesson_idx][2].get_text()))

            if len(class_table[lesson_idx][0].get_teachers()) == 0 and len(class_table[lesson_idx][0].get_lesson_name()) != 0 and have_color(l[lesson_idx][0].get_color()):
                class_table[lesson_idx][0].set_teachers([get_teacher_by_color(l[lesson_idx][0].get_color())])

            if len(class_table[lesson_idx][1].get_teachers()) == 0 and len(class_table[lesson_idx][1].get_lesson_name()) != 0 and have_color(l[lesson_idx][2].get_color()):
                class_table[lesson_idx][1].set_teachers([get_teacher_by_color(l[lesson_idx][2].get_color())])

            class_table[lesson_idx][0].set_time(WORKING_TIME_FOR_EACH_CLASS[class_name].get_lesson_time(lesson_idx))
            class_table[lesson_idx][1].set_time(WORKING_TIME_FOR_EACH_CLASS[class_name].get_lesson_time(lesson_idx))

        for lesson_idx in range(MAX_LESSONS_PER_DAY):
            if class_table[lesson_idx][0].get_lesson_name() != "":
                if get_cabs(l[lesson_idx][1].get_text()) != [] and l[lesson_idx][1].get_text() != l[lesson_idx][0].get_text():
                    class_table[lesson_idx][0].set_cabs(get_cabs(l[lesson_idx][1].get_text()))
                else:
                    class_table[lesson_idx][0].set_cabs(get_cabs(l[lesson_idx][3].get_text()))
            if class_table[lesson_idx][1].get_lesson_name() != "":
                class_table[lesson_idx][1].set_cabs(get_cabs(l[lesson_idx][3].get_text()))

        self.__class_table = class_table

    def get_lesson(self, lesson_idx: int, group_idx: int):
        return self.__class_table[lesson_idx][group_idx].get_lesson_name()

    def get_teachers(self, lesson_idx: int, group_idx: int):
        return self.__class_table[lesson_idx][group_idx].get_teachers()

    def get_time(self, lesson_idx: int, group_idx: int):
        return self.__class_table[lesson_idx][group_idx].get_time()

    def get_cabs(self, lesson_idx: int, group_idx: int):
        return self.__class_table[lesson_idx][group_idx].get_cabs()

    def get_class_table(self):
        return self.__class_table

    def __eq__(self, other):
        for i in range(MAX_LESSONS_PER_DAY):
            for j in [0, 1]:
                if (self.__class_table[i][j] != other.get_class_table()[i][j]):
                    return False
        return True

    def __ne__(self, other):
        return not (self == other)


'''#Чутка тестов
class_name = "11м"
day_of_the_week = "ВТ"
l = get_day(class_name, day_of_the_week)
a = StudentDay(class_name, day_of_the_week)         # - пример создания
for i in range(MAX_LESSONS_PER_DAY):
    for j in range(2):
        print(f"{a.get_time(i, j), a.get_lesson(i, j), a.get_teachers(i, j), a.get_cabs(i, j)}".ljust(80), end = ' ')
    print()'''
