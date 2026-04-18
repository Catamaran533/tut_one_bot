import telebot
from ClassesTable import *
from TeachersTable import *
from TeachersLesson import *
from telebot import apihelper
import socks
import logging

apihelper.CONNECT_TIMEOUT = 60
apihelper.READ_TIMEOUT = 60

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(message)s')
logger = logging.getLogger('SchoolBot')

telebot.apihelper.proxy = {'https': 'socks4://171.99.147.85:4153'}

TOKEN = '8275369590:AAGkscc0P7PDBLGmiIfus73IVj2zRB2pgkM' # токен бота
bot = telebot.TeleBot(token=TOKEN) # бот - @UrokPlusBot
grades = ['5мл', '6мл', '7мл', '8м', '8хб', '8г', '9м', '9хб', '9г', '10м', '10хб', '10г', '11м', '11хб', '11г'] # все классы
waiting_grade = {} # ожидаем ли ввод класса в этом чате
waiting_teacher = {} # ожидаем ли ввод фамилии в этом чате
waiting_location_teacher = {}  # ожидаем ввод фамилии для поиска кабинета
waiting_teacher_contacts = {} # ожидаем ли ввод фамилии для инфы о преподах
all_chats_id = set() # сет всех чатов
user_role = {}  # chat_id → 'student' или 'teacher'
user_class = {}  # chat_id → класс (например, '9м_left_left')
user_teacher = {}  # chat_id → фамилия учителя
last_schedule_msg = {}  # Здесь будем хранить {chat_id: message_id} для посдеднего расписания
notifications_enabled = {}  # chat_id → True (вкл) или False (выкл)
days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресенье'
} # все дни недели
day_cuts = {
    'mon': 'ПН',
    'tue': 'ВТ',
    'wed': 'СР',
    'thu': 'ЧТ',
    'fri': 'ПТ',
    'sat': 'СБ',
    'sun': 'ВС'
} # сокращения всех дней
day_cuts_for_bot = {
    'ПН': 'mon',
    'ВТ': 'tue',
    'СР': 'wed',
    'ЧТ': 'thu',
    'ПТ': 'fri',
    'СБ': 'sat',
    'ВС': 'sun'
} # наоборот для бота
day_cuts_reverse = {
    'ПН': 'Понедельник',
    'ВТ': 'Вторник',
    'СР': 'Среда',
    'ЧТ': 'Четверг',
    'ПТ': 'Пятница',
    'СБ': 'Суббота',
    'ВС': 'Воскресенье',
} # расшифровка дней
days_map = {0: 'ПН', 1: 'ВТ', 2: 'СР', 3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}
vacations = [
    {'name': 'Осенние', 'start': '26-10-2025', 'end': '04-11-2025'},
    {'name': 'Зимние', 'start': '31-12-2025', 'end': '11-01-2026'},
    {'name': 'Весенние', 'start': '29-03-2026', 'end': '05-04-2026'},
    {'name': 'Летние', 'start': '27-05-2026', 'end': '31-08-2026'}
]
admins = {'ProArtem567', 'mishagrib', 'dzaicev'} # админы бота
teachers = [
    "кряжева-чёрная", "никифорова", "битюкова", "галиулина", "борзенкова",
    "харсиева", "маковеев", "андрианова", "пичугина", "бабакин", "порецкий",
    "облендер", "спицкая", "ершова", "абакумова", "пронин", "михайлова",
    "обуховская", "кутявин", "зверев", "данилова", "минаева", "биологии",
    "студзинский", "костюченко", "ремнёв", "кузнецова", "лужбинина",
    "цейтлин", "щавелев", "розова", "солынин", "шайдуров", "антипов",
    "абросимова", "зиннурова", "петерс", "иванова", "сотников", "теслер",
    "красоткина", "бикулова", "артамонова", "тишунин", "туманова", "щеглова",
    "макарова", "иванов", "нанобашвили", "пичугин", "зайцев", "богданова",
    "зачиняев", "левина", "пуеров", "клюев", "ханабиев", "горных",
    "александрова", "прохоренко", "холодилов", "вдовиченко", "прадун",
    "рожков", "раев", "тарабукина", "дивенков", "литература", "крылова",
    "казакова", "травникова", "соловьева", "коваленко", "сорокин",
    "коршунков", "шубинский"
] # все учителя
TEACHER_CONTACTS = {name: "Контактов этого учителя пока что нет в базе" for name in teachers} # инфа про учителей
# реальные контакты
TEACHER_CONTACTS["абакумова"] = "👩‍🏫 Абакумова Елена Андреевна\n📞 +7 (902) 985-65-57\n📧 lena.abakumova@gmail.com"
TEACHER_CONTACTS["антипов"] = "👨‍🏫 Антипов Михаил Александович\n📞 +7 (921) 778-35-86\n📧 hyperbor@list.ru"
TEACHER_CONTACTS["артамонова"] = "👩‍🏫 Артамонова Анна Олеговна\n📞 +7 (921) 404-54-28"
TEACHER_CONTACTS["битюкова"] = "👩‍🏫 Битюкова Марина Николаевна\n📞 +7 (911) 742-84-92\n📧 mar_ka0412@mail.ru"
TEACHER_CONTACTS["дивенков"] = "👨‍🏫 Дивенков Владимир Андреевич\n📧 dwa28@mail.ru"
TEACHER_CONTACTS["зачиняев"] = "👨‍🏫 Зачиняев Александр Васильевич\n📞 +7 (911) 940-57-40\n📧 zachinyaev2000@mail.ru"
TEACHER_CONTACTS["кузнецова"] = "👩‍🏫 Кузнецова Ольга Геннадьевна\n📞 +7 (981) 718-36-01\n📧 ok.13@bk.ru"
TEACHER_CONTACTS["лужбинина"] = "👩‍🏫 Лужбинина Марина Маратовна\n📞 +7 (906) 275-95-24\n📧 murtazina_marina@bk.ru"
TEACHER_CONTACTS["михайлова"] = "👩‍🏫 Михайлова Светлана Викторовна\n📞 +7 (921) 318-09-12\n📧 jdana-m@yandex.ru"
TEACHER_CONTACTS["нанобашвили"] = "👩‍🏫 Нанобашвили Татьяна Вячеславовна\n📞 +7 (921) 571-65-52\n📧 Zajazt@yandex.ru"
TEACHER_CONTACTS["облендер"] = "👩‍🏫 Облендер Анастасия Борисовна\n📞 +7 (921) 376-48-33\n📧 nastya.deikova@yandex.ru"
TEACHER_CONTACTS["пичугин"] = "👨‍🏫 Пичугин Борис Юрьевич\n📞 +7 (965) 978-87-87\n📧 boris.pichugin@gmail.com"
TEACHER_CONTACTS["пичугина"] = "👩‍🏫 Пичугина Анна Николаевна\n📞 +7 (965) 985-53-23\n📧 anna.pichugina@gmail.com"
TEACHER_CONTACTS["порецкий"] = "👨‍🏫 Порецкий Александр Маркович\n📞 +7 (921) 302-03-60\n📧 pam-online@yandex.ru"
TEACHER_CONTACTS["прадун"] = "👩‍🏫 Прадун Светлана Александровна\n📞 +7 (911) 098-55-12\n📧 sveta.pradun@gmail.com"
TEACHER_CONTACTS["солынин"] = "👨‍🏫 Солынин Андрей Александрович\n📞 +7 (965) 786-45-45\n📧 a_solynin@mail.ru"
TEACHER_CONTACTS["спицкая"] = "👩‍🏫 Спицкая Анна Александровна\n📞 +7 (953) 348-45-93\n📧 spitskaya@mail.ru"
TEACHER_CONTACTS["студзинский"] = "👨‍🏫 Студзинский Виталий Михайлович\n📞 +7 (911) 002-67-58\n📧 svm.fl@mail.ru"
TEACHER_CONTACTS["тарабукина"] = "👩‍🏫 Тарабукина Арина Валерьевна\n📞 +7 (921) 571-50-81\n📧 arina2201@yandex.ru"
TEACHER_CONTACTS["теслер"] = "👨‍🏫 Теслер Андрей Аркадьевич\n📞 +7 (904) 512-40-23\n📧 andartes@yandex.ru"
TEACHER_CONTACTS["тишунин"] = "👨‍🏫 Тишунин Алексей Викторович\n📞 +7 (911) 816-43-20\n📧 altish58@gmail.com"
TEACHER_CONTACTS["туманова"] = "👩‍🏫 Туманова Ирина Михайловна\n📞 +7 (921) 428-27-92\n📧 imtumanova@mail.ru"
TEACHER_CONTACTS["щеглова"] = "👩‍🏫 Щеглова Александра Павловна\n📞 +7 (921) 756-82-24\n📧 apsch@yandex.ru"
TEACHER_CONTACTS["ремнёв"] = "👨‍🏫 Ремнёв Денис Константинович\n📞 +7 (951) 685-37-85"

UPDATE_TIME_MINUTES = 10 # время обновления расписаний на фоне
schedule = ClassesTable() # расписание для учеников
teachers_schedule = TeachersTable() # расписание для учителей