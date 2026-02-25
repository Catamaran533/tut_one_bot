from ClassesTable import *
from consts import *
from TeachersLesson import *

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
                        day_obj = classes_table.get_student_day(class_name, day)

                        teachers = day_obj.get_teachers(i, j)
                        cabs = day_obj.get_cabs(i, j)
                        time = day_obj.get_time(i, j)
                        lesson_name = day_obj.get_lesson(i, j)

                        for teacher in teachers:
                            teachers_days[teacher][day][i] = TeachersLesson(
                                lesson_name, class_name, cabs, time
                            )

        self.__teachers_table = teachers_days

    def get_teachers_lesson(self, teacher_name: str, day_of_the_week: str, lesson_idx: int):
        return self.__teachers_table[teacher_name][day_of_the_week][lesson_idx]

    def update(self):
        teachers_days = dict()

        # ✅ FIX — правильная инициализация
        for i in MAP_WITH_TEACHERS_NAMES.keys():
            teachers_days[i] = dict()
            for day in DAYS_OF_THE_WEEK:
                teachers_days[i][day] = [TeachersLesson("", "", [], "") for _ in range(MAX_LESSONS_PER_DAY)]

        classes_table = ClassesTable()

        for day in DAYS_OF_THE_WEEK:
            for class_name in CLASSES:
                for i in range(8):
                    for j in [0, 1]:
                        student_table = classes_table.get_student_day(class_name, day)

                        teachers = student_table.get_teachers(i, j)
                        cabs = student_table.get_cabs(i, j)
                        time = student_table.get_time(i, j)
                        lesson_name = student_table.get_lesson(i, j)

                        for teacher in teachers:
                            teachers_days[teacher][day][i] = TeachersLesson(lesson_name, class_name, cabs, time)

        diff = []

        for teacher_name in MAP_WITH_TEACHERS_NAMES.keys():
            for day in DAYS_OF_THE_WEEK:
                if self.__teachers_table[teacher_name][day] != teachers_days[teacher_name][day]:
                    diff.append([teacher_name, day])

        self.__teachers_table = teachers_days

        return diff


schedule_teacher = TeachersTable()
