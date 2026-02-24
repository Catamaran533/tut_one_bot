class TeachersLesson:
    def __init__(self, lesson_name: str, class_name: str, cabs: list, time: str):
        self.__lesson_name = lesson_name
        self.__class_name = class_name
        self.__cabs = cabs
        self.__time = time

    def set_lesson_name(self, new_lesson_name: str):
        self.__lesson_name = new_lesson_name

    def get_lesson_name(self):
        return self.__lesson_name

    def set_class_name(self, new_class_name: str):
        self.__class_name = new_class_name

    def get_class_name(self):
        return self.__class_name

    def set_cabs(self, new_cabs: list):
        self.__cabs = new_cabs

    def get_cabs(self):
        return self.__cabs

    def set_time(self, new_time: str):
        self.__time = new_time

    def get_time(self):
        return self.__time

    def __eq__(self, other):
        l = [self.__lesson_name == other.get_lesson_name(),
             self.__class_name == other.get_class_name(),
             self.__cabs == other.get_cabs(),
             self.__time == other.get_time()]
        return sum(l) == len(l)

    def __ne__(self, other):
        return not (self == other)