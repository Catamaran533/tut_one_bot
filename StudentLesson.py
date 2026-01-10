from SplittingDays import *
from consts import MAP_WITH_TEACHERS_ABBREVIATION, MAP_WITH_TEACHERS_NAMES





class StudentLesson:
    def __init__(self, lesson_name: str, teachers: list, cabs: list, time: str):           # в конструктор передаем только строки или списки строк
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


def remove_non_alphabetic_filter(text: str):        # Фильтрует только буквенные символы
    return ''.join(filter(str.isalpha, text))

def get_lesson_name_and_teachers(text: str):
    lesson_name = ""
    teachers = []
    for i in text.split():
        new_i = remove_non_alphabetic_filter(i)
        if (new_i.istitle()):
            new_i = new_i.lower()
            if (new_i in MAP_WITH_TEACHERS_ABBREVIATION.keys()):
                teachers.append(MAP_WITH_TEACHERS_ABBREVIATION[new_i].capitalize())
            elif (new_i in MAP_WITH_TEACHERS_NAMES):
                teachers.append(MAP_WITH_TEACHERS_NAMES[new_i].capitalize())
            else:
                lesson_name += i
                lesson_name += ' '
        else:
            lesson_name += i
            lesson_name += ' '
    lesson_name.rstrip()
    return [lesson_name, teachers]


class StudentDay:
    def __init__(self, student_class: str, day_of_the_week: str):
        self.__day_of_the_week = day_of_the_week
        self.__student_class = student_class
        self.__lessons = [[NONE_STUDENT_LESSON, NONE_STUDENT_LESSON] for _ in range(MAX_LESSONS_PER_DAY)]
        self.__download()

    def get_lessons(self):
        return self.__lessons

    def __download(self):
        lessons = [[NONE_STUDENT_LESSON, NONE_STUDENT_LESSON] for _ in range(MAX_LESSONS_PER_DAY)]
        l = get_day(self.__student_class, self.__day_of_the_week)

        lesson_idx = 0
        while lesson_idx < MAX_LESSONS_PER_DAY:
            if (l[lesson_idx][0].get_text() == ""):
                lesson_idx += 1
                continue

            is_same_in_two_groups = False
            #TODO отдебажить
            print("debug color", l[lesson_idx][0].get_color(), l[lesson_idx][2].get_color(), lesson_idx + 1)
            if (l[lesson_idx][0].get_color() == l[lesson_idx][2].get_color()):
                is_same_in_two_groups = True

            is_double_long = False

            need_to_add_to_lesson_idx = 0

            if (lesson_idx < MAX_LESSONS_PER_DAY - 1):
                if (is_same_in_two_groups):
                    if (l[lesson_idx + 1][0].get_color() == l[lesson_idx + 1][2].get_color() == l[lesson_idx][0].get_color()
                            and l[lesson_idx + 1][0].get_text() == ""
                            and l[lesson_idx + 1][1].get_text() == ""
                            and l[lesson_idx + 1][2].get_text() == ""
                            and l[lesson_idx + 1][3].get_text() == ""):
                        is_double_long = True
                        need_to_add_to_lesson_idx = 2
                    else:
                        need_to_add_to_lesson_idx = 1
                else:
                    if (l[lesson_idx + 1][0].get_color() == l[lesson_idx][0].get_color()
                            and l[lesson_idx + 1][0].get_text() == ""
                            and l[lesson_idx + 1][1].get_text() == ""):
                        is_double_long = True
                        need_to_add_to_lesson_idx = 2
                    else:
                        need_to_add_to_lesson_idx = 1


            lesson_name, teachers = get_lesson_name_and_teachers(l[lesson_idx][0].get_text())
            cabs = l[lesson_idx][3].get_text()
            time = get_lesson_time(self.__student_class, lesson_idx)
            current_lesson = StudentLesson(lesson_name, teachers, cabs, time)

            if (is_same_in_two_groups):
                lessons[lesson_idx][0] = current_lesson
                lessons[lesson_idx][1] = current_lesson
            else:
                lessons[lesson_idx][0] = current_lesson

            if (is_double_long):
                lessons[lesson_idx + 1][0] = lessons[lesson_idx][0]
                lessons[lesson_idx + 1][1] = lessons[lesson_idx][1]


            lesson_idx +=need_to_add_to_lesson_idx

        self.__lessons = lessons



a = StudentDay("5мл", "ПН")

for i in a.get_lessons():
    print(i[0].get_lesson_name(), i[1].get_lesson_name())









