from consts import *


class StudentLesson:
    def __init__(self, lesson_name: str, teachers: list, cabs: list, time: str):
        self.__lesson_name = lesson_name
        self.__teachers = teachers
        self.__cabs = cabs
        self.__time = time

    def get_lesson_name(self):
        return self.__lesson_name

    def get_teachers(self):
        return self.__teachers

    def get_cabs(self):
        return self.__cabs

    def get_time(self):
        return self.__time

    def set_lesson_name(self, new_name: str):
        self.__lesson_name = new_name

    def set_teachers(self, new_teachers: list):
        self.__teachers = new_teachers

    def set_cabs(self, new_cabs: str):
        self.__cabs = new_cabs

    def set_time(self, new_time):
        self.__time = new_time

    def __str__(self):
        s = "StudentLesson{" + f"{self.__lesson_name}, {self.__teachers}, {self.__cabs}, {self.__time}" + "}"
        return s


NONE_STUDENT_LESSON = StudentLesson("", [], [], "")

DAYS_OF_THE_WEEK = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
CLASSES = ["5мл", "6мл", "7мл", "8м", "9м", "10м", "11м", "8хб", "9хб", "10хб", "11хб", "8г", "9г", "10г", "11г"]


def remove_non_alphabetic_filter(text: str):
    return ''.join(filter(str.isalpha, text))

def get_lesson_name_and_teachers(text: str):
    lesson_name = ""
    teachers = []
    for i in text.split():
        new_i = remove_non_alphabetic_filter(i)
        if new_i.istitle():
            new_i = new_i.lower()
            if new_i in MAP_WITH_TEACHERS_ABBREVIATION:
                teachers.append(MAP_WITH_TEACHERS_ABBREVIATION[new_i].capitalize())
            elif new_i in MAP_WITH_TEACHERS_NAMES:
                teachers.append(MAP_WITH_TEACHERS_NAMES[new_i].capitalize())
            else:
                lesson_name += i
                lesson_name += ' '
        else:
            lesson_name += i
            lesson_name += ' '
    lesson_name = lesson_name.rstrip()
    return [lesson_name, teachers]