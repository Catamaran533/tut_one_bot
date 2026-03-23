import telebot
from ClassesTable import *
from TeachersTable import *
from TeachersLesson import *
from telebot import apihelper
import socks
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(message)s')
logger = logging.getLogger('SchoolBotYumsh')

PROXY_HOST = '104.164.32.234'
PROXY_PORT = 62887
PROXY_LOGIN = 'BKXNvGYr9'
PROXY_PASS = 'HHcx8Kw7u'
apihelper.proxy = {
    'https': f'socks5://{PROXY_LOGIN}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'
}

TOKEN = '8275369590:AAGkscc0P7PDBLGmiIfus73IVj2zRB2pgkM' # токен бота
bot = telebot.TeleBot(token=TOKEN) # бот - @UrokPlusBot
grades = ['5мл', '6мл', '7мл', '8м', '8хб', '8г', '9м', '9хб', '9г', '10м', '10хб', '10г', '11м', '11хб', '11г'] # все классы
waiting_grade = {} # ожидаем ли ввод класса в этом чате
waiting_teacher = {} # ожидаем ли ввод фамилии в этом чате
waiting_location_teacher = {}  # ожидаем ввод фамилии для поиска кабинета
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
teachers = {i for i in MAP_WITH_TEACHERS_NAMES.keys()} # все учителя
admins = {'ProArtem567', 'mishagrib', 'dzaicev'} # админы бота

UPDATE_TIME_MINUTES = 10 # время обновления расписаний на фоне
schedule = ClassesTable() # расписание для учеников
teachers_schedule = TeachersTable() # расписание для учителей