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

    def set_cabs(self, new_cabs: list):
        self.__cabs = new_cabs

    def set_time(self, new_time: str):
        self.__time = new_time

    def __str__(self):
        s = "StudentLesson{" + f"{self.__lesson_name}, {self.__teachers}, {self.__cabs}, {self.__time}" + "}"
        return s

    def __eq__(self, other):
        ans = [self.__lesson_name == other.get_lesson_name(),
               self.__teachers == other.get_teachers(),
               self.__cabs == other.get_cabs(),
               self.__time == other.get_time()]
        return sum(ans) == len(ans)

    def __ne__(self, other):
        return not (self == other)


NONE_STUDENT_LESSON = StudentLesson("", [], [], "")

DAYS_OF_THE_WEEK = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
CLASSES = ["5мл", "6мл", "7мл", "8м", "9м", "10м", "11м", "8хб", "9хб", "10хб", "11хб", "8г", "9г", "10г", "11г"]


