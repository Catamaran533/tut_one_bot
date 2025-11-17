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
    def __init__(self, number, subject, teacher, room):
        self.__number = number                                                  #Номер урока
        self.__subject = subject                                                  #Название урока
        self.__teacher = teacher                                                   #Учитель
        self.__room = room                                                      #Кабинет

    def get_number(self):
        return self.__number

    def set_number(self, new_number):
        self.__number = new_number

    def get_subject(self):
        return self.__subject

    def set_subject(self, new_subject):
        self.__subject = new_subject

    def get_teacher(self):
        return self.__teacher

    def set_teacher(self, new_teacher):
        self.__teacher = new_teacher

    def get_room(self):
        return self.__room

    def set_room(self, new_room):
        self.__room = new_room



MAP_WITH_TEACHERS_ABBREVIATION = {
    "а" : "абакумова",
    "б" :  "богданова",
    "борз" : "борзенкова",
    "в" : "вдовиченко",
    "к" : "кузнецова",
    "кр" : "кряжева-чёрная",
    "л" : "левина",
    "мак" : "макарова",
    "мин" : "минаева",
    "о" :  "облендер",
    "п" :  "пичугина",
    "с" : "сотников",
    "сп" : "спицкая",
    "ц" :  "цейтлин",
    "ш" :  "шайдуров",
    "щав" : "щавелев",
    "щ" : "щеглова",
    "и" : "иванова",


    "никифорова" : "никифорова",
    "битюкова" : "битюкова",
    "галиулина" : "галиулина",
    "борзенкова" : "борзенкова",
    "харсиева" : "харсиева",
    "маковеев" : "маковеев",
    "андрианова" : "андрианова",
    "пичугина" : "пичугина",
    "бабакин" : "бабакин",
    "порецкий" : "порецкий",
    "облендер" : "облендер",
    "спицкая" : "спицкая",
    "ершова" : "ершова",
    "абакумова" : "абакумова",
    "пронин" : "пронин",
    "михайлова" : "михайлова",
    "обуховская" : "обуховская",
    "кутявин" : "кутявин",
    "зверев" : "зверев",
    "данилова" : "данилова",
    "минаева" : "минаева",
    "биологии" : "биологии",
    "студзинский" : "студзинский",
    "костюченко" : "костюченко",
    "ремнёв" : "ремнёв",
    "кузнецова" : "кузнецова",
    "лужбинина" : "лужбинина",
    "цейтлин" : "цейтлин",
    "щавелев" : "щавелев",
    "розова" : "розова",
    "солынин" : "солынин",
    "шайдуров" : "шайдуров",
    "антипов" : "антипов",
    "абросимова" : "абросимова",
    "зиннурова" : "зиннурова",
    "петерс" : "петерс",
    "иванова" : "иванова",
    "сотников" : "сотников",
    "теслер" : "теслер",
    "красоткина" : "красоткина",
    "бикулова" : "бикулова",
    "артамонова" : "артамонова",
    "тишунин" : "тишунин",
    "туманова" : "туманова",
    "щеглова" : "щеглова",
    "макарова" : "макарова",
    "иванов" : "иванов",
    "нанобашвили" : "нанобашвили",
    "пичугин" : "пичугин",
    "зайцев" : "зайцев",
    "богданова" : "богданова",
    "зачиняев" : "зачиняев",
    "левина" : "левина",
    "пуеров" : "пуеров",
    "клюев" : "клюев",
    "ханабиев" : "ханабиев",
    "горных" : "горных",
    "александрова" : "александрова",
    "прохоренко" : "прохоренко",
    "холодилов" : "холодилов",
    "вдовиченко" : "вдовиченко",
    "прадун" : "прадун",
    "рожков" : "рожков",
    "раев" : "раев",
    "тарабукина" : "тарабукина",
    "дивенков" : "дивенков",
    "литература" : "литература",
    "крылова" : "крылова",
    "казакова" : "казакова",
    "травникова" : "травникова",
    "соловьева" : "соловьева"






}
#TODO ПЕРЕДЕЛАТЬ ВСЁ НАФИГ!!!

def parse_teacher(teachers_name):
    ans = ""
    for i in teachers_name.lower():
        if (i.isalpha()):
            ans += i

    #return MAP_WITH_TEACHERS_ABBREVIATION[ans]
    return ans


def null_lesson():
    return Lesson(-1, "хз", "хз", "хз")


MAX_LESSONS_PER_DAY = 8

MAX_STRING_LENGTH_BEFORE_AUTO_ENTER_FOR_LESSON_WITH_TWO_GROUPS = len("кружок по литературе(Цейтлин)")
MAX_STRING_LENGTH_BEFORE_AUTO_ENTER_FOR_LESSON_WITH_ONE_GROUP = len("литература 333")

#TODO функция parse_teacher, которая получает полное имя учителя по тому что есть в табличке


def parse_lessons(x, y):                    #координаты начало столбца с классом
    ans = [[null_lesson(), null_lesson()] for _ in range(MAX_LESSONS_PER_DAY)]      #возвращает вектор векторов из 2-ух элементов, по которым занимаются группы
    for i in range(x + 1, x + MAX_LESSONS_PER_DAY + 1):
        if (GOOGLE_SHEET_DATA[i][y] == ''):
            continue
        if (GOOGLE_SHEET_DATA[i][y + 1] == '' and GOOGLE_SHEET_DATA[i][y + 2] == ''):       #проверка на урок у обеих групп

            lesson_data = GOOGLE_SHEET_DATA[i][y]
            lesson_room = GOOGLE_SHEET_DATA[i][y + 3]

            splited_lesson_data = lesson_data.split()
            teacher = splited_lesson_data[-1]

            lesson_name = ' '.join(splited_lesson_data[:-1])
            lesson_name.strip()


            ans[i - x - 1][0] = Lesson(i - x, lesson_name, teacher, lesson_room)
            ans[i - x - 1][1] = Lesson(i - x, lesson_name, teacher, lesson_room)

            if ('\n' in lesson_data or len(lesson_data) > MAX_STRING_LENGTH_BEFORE_AUTO_ENTER_FOR_LESSON_WITH_TWO_GROUPS): #проверка является ли урок парой
                ans[i - x][0] = Lesson(i - x + 1, lesson_name, teacher, lesson_room)    #эксель иногда может сам энтер поставить
                ans[i - x][1] = Lesson(i - x + 1, lesson_name, teacher, lesson_room)    #при слишком длинной строке

        else:
            lesson_data = GOOGLE_SHEET_DATA[i][y]
            lesson_room = GOOGLE_SHEET_DATA[i][y + 1]

            splited_lesson_data = lesson_data.split()
            teacher = splited_lesson_data[-1]

            lesson_name = ' '.join(splited_lesson_data[:-1])
            lesson_name.strip()

            ans[i - x - 1][0] = Lesson(i - x, lesson_name, teacher, lesson_room)

            if ('\n' in lesson_data or len(lesson_data) > MAX_STRING_LENGTH_BEFORE_AUTO_ENTER_FOR_LESSON_WITH_ONE_GROUP):  #проверка является ли урок парой
                ans[i - x][0] = Lesson(i - x + 1, lesson_name, teacher, lesson_room)

    #//тут вторая группа будет и тут уже y + 2

    for i in range(x + 1, x + MAX_LESSONS_PER_DAY + 1):
        if (ans[i - x - 1][1] != null_lesson() or GOOGLE_SHEET_DATA[i][y + 2] == ''):
            continue
        lesson_data = GOOGLE_SHEET_DATA[i][y + 2]
        lesson_room = GOOGLE_SHEET_DATA[i][y + 3]

        splited_lesson_data = lesson_data.split()
        teacher = splited_lesson_data[-1]

        lesson_name = ' '.join(splited_lesson_data[:-1])
        lesson_name.strip()

        ans[i - x - 1][1] = Lesson(i - x, lesson_name, teacher, lesson_room)
        if ('\n' in lesson_data or len(lesson_data) > MAX_STRING_LENGTH_BEFORE_AUTO_ENTER_FOR_LESSON_WITH_ONE_GROUP):  # проверка является ли урок парой
            ans[i - x][1] = Lesson(i - x + 1, lesson_name, teacher, lesson_room)





    return ans



















#TODO надо к чертям переделать
'''class StudentDay:
    def __init__(self, x, y):              #координаты с началом дня расписания класса(названия включительно)
        self.__class = GOOGLE_SHEET_DATA[x][y]
        lessons = []
        for i in range(x + 1, x + MAX_LESSONS_PER_DAY + 1):
            lessons.append(GOOGLE_SHEET_DATA[i][y])
        self.__lessons = lessons

    def get_class(self):
        return self.__class

    def get_lessons(self):
        return self.__lessons'''

#Тут иногда могут пояаляться мои тесты
'''b = StudentDay(9, 4)
print(b.get_lessons())'''


s = set()
for x in range(9, 60, 10):
    for y in range(65, 65 + 15 + 1, 5):
        for i in parse_lessons(x, y):
            t1, t2 = parse_teacher(i[0].get_teacher()), parse_teacher(i[1].get_teacher())
            if (t1 == "классов" or t2 == "классов"):
                print(x, y)
            if (t1 not in MAP_WITH_TEACHERS_ABBREVIATION.keys() and t1 != "хз"):
                s.add(t1)
            if (t2 not in MAP_WITH_TEACHERS_ABBREVIATION.keys() and t2 != "хз"):
                s.add(t2)

for i in parse_lessons(9, 65):
    print(i[0].get_teacher())
print()
for i in parse_lessons(9, 61 + 20):
    print(i[0].get_teacher())
print()


for i in s:
    print('"', i, '" : "', i, '",', sep = '')
