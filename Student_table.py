from cell import *
from SplittingDays import *
from StudentLesson import *
from consts import *
from Teachers_by_colors import get_teacher_by_color, have_color

HORIZONTAL_TABLE_SIZE = 4
MAX_LESSONS_PER_DAY = 8

BAD_SYMBOLS = [";", ":", "()", "+", "->", "<-"]

def get_teachers(text: str):
    for i in BAD_SYMBOLS:
        text = text.replace(i, ' ')
    text = text.split()
    teachers = []
    for i in text:
        only_letters = ''.join([c for c in i if c.isalpha() or c.isnumeric()])
        if (len(only_letters) == 0):
            continue
        if only_letters[0].isupper():
            only_letters = only_letters.lower()
            if only_letters in MAP_WITH_TEACHERS_NAMES.keys():
                teachers.append(only_letters)
            elif only_letters in MAP_WITH_TEACHERS_ABBREVIATION.keys():
                teachers.append(MAP_WITH_TEACHERS_ABBREVIATION[only_letters])
    return teachers

def get_lesson(text: str):
    for i in BAD_SYMBOLS:
        text = text.replace(i, ' ')
    text = text.split()
    lesson_list = []
    for i in text:
        only_letters = ''.join([c for c in i if c.isalpha() or c.isnumeric()])
        if (len(only_letters) == 0):
            continue
        if only_letters[0].isupper():
            only_letters = only_letters.lower()
            if only_letters in MAP_WITH_TEACHERS_NAMES.keys():
                break
            elif only_letters in MAP_WITH_TEACHERS_ABBREVIATION.keys():
                break
        lesson_list.append(i)
    lesson = ""
    for i in lesson_list:
        lesson += i + " "
    lesson = lesson.rstrip()
    return lesson

def get_cabs(text: str):
    return text.split()


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

            if len(class_table[lesson_idx][1].get_teachers()) == 0 and len(class_table[lesson_idx][1].get_lesson_name()) != 0 and have_color(l[lesson_idx][0].get_color()):
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

'''#Чутка тестов
class_name = "11м"
day_of_the_week = "ВТ"
l = get_day(class_name, day_of_the_week)
a = StudentDay(class_name, day_of_the_week)         # - пример создания
for i in range(MAX_LESSONS_PER_DAY):
    for j in range(2):
        print(f"{a.get_time(i, j), a.get_lesson(i, j), a.get_teachers(i, j), a.get_cabs(i, j)}".ljust(80), end = ' ')
    print()'''
