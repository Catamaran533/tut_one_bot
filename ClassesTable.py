from Student_table import *
import SplittingDays
DAYS_OF_THE_WEEK = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
CLASSES = ["5мл", "6мл", "7мл", "8м", "9м", "10м", "11м", "8хб", "9хб", "10хб", "11хб", "8г", "9г", "10г", "11г"]
MAX_LESSONS_PER_DAY = 8

class ClassesTable:
    def __init__(self):
        global SCHOOL_TABLE
        SCHOOL_TABLE = get_school_table_sheet()
        SplittingDays.SCHOOL_TABLE = SCHOOL_TABLE
        classes = dict()
        for class_name in CLASSES:
            classes[class_name] = dict()
            for day in DAYS_OF_THE_WEEK:
                classes[class_name][day] = StudentDay(class_name, day)
        self.__classes = classes

    def get_student_day(self, class_name: str, day: str):
        return self.__classes[class_name][day]

    def update(self):               #возвращает список классов и дней неделей которых надо оповестить об изменении
        global SCHOOL_TABLE
        SCHOOL_TABLE = get_school_table_sheet()
        SplittingDays.SCHOOL_TABLE = SCHOOL_TABLE
        new_classes = dict()
        for class_name in CLASSES:
            new_classes[class_name] = dict()
            for day in DAYS_OF_THE_WEEK:
                new_classes[class_name][day] = StudentDay(class_name, day)

        diff = []
        for class_name in CLASSES:
            for day in DAYS_OF_THE_WEEK:
                if (self.__classes[class_name][day] != new_classes[class_name][day]):
                    diff.append([class_name, day])
        self.__classes = new_classes
        return diff