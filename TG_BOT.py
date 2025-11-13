import csv
import io
import urllib.request


LINK_TO_GOOGLE_SHEETS = "https://clck.ru/XKJkh"
URL_FOR_EXPORT = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSiceT3WwlE-_sMrVWP8_WNehn__yN3vbwSDh4GZPZ_IxZUkshIWSG58wiNkOsL2nNApiiXpUCHPlFz/pub?gid=30599713&single=true&output=csv'


def get_data_from_google_sheets():                      #получает данные из таблички
    # Используем URL для экспорта в CSV
    response = urllib.request.urlopen(URL_FOR_EXPORT)
    with io.TextIOWrapper(response, encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)  # Читаем все данные в список
    return data  # Возвращаем готовые данные



GOOGLE_SHEET_DATA = get_data_from_google_sheets()


class Lesson:
    def __init__(self, number, type, teacher):
        self.__number = number                                                  #Номер урока
        self.__type = type                                                  #Название урока
        self.__teacher = teacher                                                 #Учитель
    def get_number(self):
        return self.__number
    def set_number(self, new_number):
        self.__number = new_number
    def get_type(self):
        return self.__type
    def set_type(self, new_type):
        self.__number = new_type
    def get_teacher(self):
        return self.__teacher
    def set_teacher(self, new_teacher):
        self.__number = new_teacher












MAX_LESSONS_PER_DAY = 8




#завтра(или в воскресенье) доделаю(P.S. затвра для меня наступает только когда я посплю)
class StudentDay:
    def __init__(self, x, y):              #координаты с началом дня расписания класса(названия включительно)
        self.__class = GOOGLE_SHEET_DATA[x][y]
        lessons = []
        for i in range(x + 1, x + MAX_LESSONS_PER_DAY + 1):
            lessons.append(GOOGLE_SHEET_DATA[i][y])
        self.__lessons = lessons

    def get_class(self):
        return self.__class

    def get_lessons(self):
        return self.__lessons

#Тут иногда могут пояаляться мои тесты
'''b = StudentDay(9, 4)
print(b.get_lessons())'''

