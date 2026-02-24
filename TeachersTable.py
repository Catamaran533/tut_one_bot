from ClassesTable import *
from consts import *
from TeachersLesson import *

#TODO написать класс TeachersLesson

DAYS_OF_THE_WEEK = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
CLASSES = ["5мл", "6мл", "7мл", "8м", "9м", "10м", "11м", "8хб", "9хб", "10хб", "11хб", "8г", "9г", "10г", "11г"]

class TeachersTable:
    def __init__(self):
        teachers_days = dict()
        for i in MAP_WITH_TEACHERS_NAMES.keys():
            teachers_days[i] = dict()
            for day in DAYS_OF_THE_WEEK:
                teachers_days[i][day] = [TeachersLesson("", "", [], "") for _ in range(MAX_LESSONS_PER_DAY)]
        classes_table = ClassesTable()
        for day in DAYS_OF_THE_WEEK:
            for class_name in CLASSES:
                for i in range(8):
                    for j in [0, 1]:
                        teachers = classes_table.get_student_day(class_name, day).get_teachers(i, j)
                        cabs = classes_table.get_student_day(class_name, day).get_cabs(i, j)
                        time = classes_table.get_student_day(class_name, day).get_time(i, j)
                        lesson_name = classes_table.get_student_day(class_name, day).get_lesson(i, j)
                        for teacher in teachers:
                            if (teacher not in teachers_days.keys()):
                                teachers_days[teacher][day][i] = TeachersLesson("", "", [], "")
                            else:
                                teachers_days[teacher][day][i] = TeachersLesson(lesson_name, class_name, cabs, time)
        self.__teachers_table = teachers_days


    def get_teachers_lesson(self, teacher_name : str, day_of_the_week : str, lesson_idx : int):
        return self.__teachers_table[teacher_name][day_of_the_week][lesson_idx]

    def update(self):
        teachers_days = dict()
        for i in MAP_WITH_TEACHERS_NAMES.keys():
            for day in DAYS_OF_THE_WEEK:
                teachers_days[i] = dict()
                teachers_days[i][day] = [TeachersLesson("", "", [], "") for _ in range(MAX_LESSONS_PER_DAY)]
        classes_table = ClassesTable()
        for day in DAYS_OF_THE_WEEK:
            for class_name in CLASSES:
                for i in range(8):
                    for j in [0, 1]:
                        teachers = classes_table.get_student_day(class_name, day).get_teachers(i, j)
                        cabs = classes_table.get_student_day(class_name, day).get_cabs(i, j)
                        time = classes_table.get_student_day(class_name, day).get_time(i, j)
                        lesson_name = classes_table.get_student_day(class_name, day).get_lesson(i, j)
                        for teacher in teachers:
                            if (teacher not in teachers_days.keys()):
                                teachers_days[teacher][day][i] = TeachersLesson("", "", [], "")
                            else:
                                teachers_days[teacher][day][i] = TeachersLesson(lesson_name, class_name, cabs, time)

        diff = []

        for teacher_name in MAP_WITH_TEACHERS_NAMES.keys():
            for day in DAYS_OF_THE_WEEK:
                if (self.__teachers_table[teacher_name][day] != teachers_days[teacher_name][day]):
                    diff.append([teacher_name, day])
        return diff


schedule_teacher = TeachersTable()