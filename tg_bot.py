import telebot
from telebot import types
bot = telebot.TeleBot(token='8275369590:AAG2CUbhj6Kf6qsCg3V3bAZp6Ve4XxcTp74') # бот - @UrokPlusBot

# полезные доп значения
grades = ['5мл', '6мл', '7мл', '8м', '8хб', '8г', '9м', '9хб', '9г', '10м', '10хб', '10г', '11м', '11хб', '11г'] # все классы
waiting_grade = {} # ожидаем ли ввод класса в этом чате
days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресенье'
} # все дни недели

@bot.message_handler(commands=['start']) # /start
def send_welcome(message):
    markup = types.InlineKeyboardMarkup() # кнопки
    site_button = types.InlineKeyboardButton('Открыть общее расписание', url='https://clck.ru/3QZjCY') # расписание
    markup.row(site_button)
    student_role = types.InlineKeyboardButton('Ученик или родитель', callback_data='student') # выбор ученика
    teacher_role = types.InlineKeyboardButton('Учитель', callback_data='teacher') # выбор учителя
    markup.row(student_role, teacher_role)
    bot.send_message(
        message.chat.id,
        'Приветствую!\nВы можете увидеть общее расписание уроков, либо посмотреть специализированный вариант специально для Вас - для этого выберите роль - <b>школьник(родитель школьника)</b> или <b>учитель</b>.',
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: True) # ответ на функции кнопок
def callback_answer(call):
    if call.data == 'student': # если выбран школьник
        bot.send_message(call.message.chat.id, 'Введите свой класс без пробелов (например, 9м, 11хб)')
        waiting_grade[call.message.chat.id] = True # запоминаем - нужен ли ввод
    elif call.data == 'teacher': # если выбран учитель
        bot.send_message(call.message.chat.id, 'привет, учитель (тут ниче нет пока что плоке плоке)')
    elif call.data.startswith('day_'): # выбран уже и день недели и класс
        arr = call.data.split('_')
        _, day, grade = arr
        bot.send_message(call.message.chat.id, f'Вы выбрали расписание на <b>{days[day].lower()}</b> для класса <b>{grade}.</b>', parse_mode='HTML')
    bot.answer_callback_query(call.id) # убираем бесячий таймер на кнопках

@bot.message_handler(func=lambda message: True) # выбор класса
def grade_choice(message):
    if message.chat.id in waiting_grade and waiting_grade[message.chat.id]:
        grade = message.text.lower()
        if grade in grades:
            bot.send_message(message.chat.id, f'Отлично! Вы выбрали класс: {grade}.')
            del waiting_grade[message.chat.id] # удаляем этот чат из списка тех где ожидаем ввод класса
            send_days(message.chat.id, grade) # просим выбрать день недели
        else:
            bot.reply_to(message, f'Неправильно введён класс. Введите его ещё раз. Список предложенных классов: \n{", ".join(grades)}')
            # теперь надо ввести класс ещё раз
    else:
        # если ваще хрень какая то, то просим начать заново всё
        bot.reply_to(message, 'Пожалуйста, сначала выберите роль через команду "/start"')

def send_days(chat_id, grade):  # функция выбора дня недели
    markup = types.InlineKeyboardMarkup()
    row1 = [
        types.InlineKeyboardButton("Пн", callback_data=f"day_mon_{grade}"),
        types.InlineKeyboardButton("Вт", callback_data=f"day_tue_{grade}"),
        types.InlineKeyboardButton("Ср", callback_data=f"day_wed_{grade}")
    ]
    markup.row(*row1)
    row2 = [
        types.InlineKeyboardButton("Чт", callback_data=f"day_thu_{grade}"),
        types.InlineKeyboardButton("Пт", callback_data=f"day_fri_{grade}")
    ]
    markup.row(*row2)
    row3 = [
        types.InlineKeyboardButton("Сб", callback_data=f"day_sat_{grade}"),
        types.InlineKeyboardButton("Вс", callback_data=f"day_sun_{grade}")
    ]
    markup.row(*row3)
    bot.send_message(chat_id, "Выберите день недели:", reply_markup=markup)

bot.polling(none_stop=True)