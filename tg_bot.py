import telebot
from telebot import types
bot = telebot.TeleBot(token='8275369590:AAG2CUbhj6Kf6qsCg3V3bAZp6Ve4XxcTp74') # бот - @UrokPlusBot
grades = ['5мл', '6мл', '7мл', '8м', '8хб', '8г', '9м', '9хб', '9г', '10м', '10хб', '10г', '11м', '11хб', '11г'] # все классы
waiting_grade = {} # ожидаем ли ввод класса в этом чате
waiting_teacher = {} # ожидаем ли ввод фамилии в этом чате
user_role = {}  # chat_id → 'student' или 'teacher'
days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресенье'
} # все дни недели
teachers = {
    'абакумова', 'абросимова', 'александрова', 'андрианова', 'антипов',
    'артамонова', 'бабакин', 'бикулова', 'битюкова', 'богданова',
    'борзенкова', 'вдовиченко', 'горных', 'данилова', 'дивенков',
    'ершова', 'зайцев', 'зачиняев', 'зверев', 'зиннурова',
    'иванов', 'иванова', 'клюев', 'красоткина', 'крыловa',
    'кузнецова', 'кутявин', 'костюченко', 'кряжева-чёрная', 'лужбинина',
    'левина', 'макарова', 'маковеев', 'минаева', 'михайлова',
    'нанобашвили', 'никифорова', 'облендер', 'обуховская', 'петерс',
    'пичугин', 'пичугина', 'порецкий', 'прадун', 'прохоренко',
    'пронин', 'пуеров', 'раев', 'ремнёв', 'рожков',
    'розова', 'соловьева', 'сотников', 'спицкая', 'студзинский',
    'тарабукина', 'теслер', 'тишунин', 'травникова', 'туманова',
    'ханабиев', 'харсиева', 'холодилов', 'щавелев', 'щеглова'
} # все учителя
admins = {'ProArtem567', 'mishagrib', 'dzaicev'} # админы бота
lessons = [
    {"subject": "Предмет", "time": "9:15–9:55", "room": 306},
    {"subject": "Предмет", "time": "10:00–10:40", "room": 306},
    {"subject": "Предмет", "time": "10:55–11:35", "room": 306},
    {"subject": "Предмет", "time": "11:50–12:30", "room": 306},
    {"subject": "Предмет", "time": "13:00–13:40", "room": 306},
    {"subject": "Предмет", "time": "13:55–14:35", "room": 306}
] # для примера возьмём 6 уроков

@bot.message_handler(commands=['start']) # /start
def send_welcome(message):
    markup = types.InlineKeyboardMarkup() # кнопки
    site_button = types.InlineKeyboardButton('Открыть общее расписание', url='https://clck.ru/3QZjCY') # расписание
    markup.row(site_button)
    student_role = types.InlineKeyboardButton('🧑‍🎓 Ученик', callback_data='student') # выбор ученика
    teacher_role = types.InlineKeyboardButton('👩‍🏫 Учитель', callback_data='teacher') # выбор учителя
    markup.row(student_role, teacher_role)
    bot.send_message(
        message.chat.id,
        'Приветствую!\nВы можете увидеть общее расписание уроков, либо посмотреть специализированный вариант специально для Вас - для этого выберите роль - <b>школьник(родитель школьника)</b> или <b>учитель</b>.',
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['help']) # /help
def help_user(message):
    bot.send_message('Описание хелпа, добавим в конце проекта')

@bot.callback_query_handler(func=lambda call: True) # ответ на функции кнопок
def callback_answer(call):
    waiting_grade.pop(call.message.chat.id, None)
    waiting_teacher.pop(call.message.chat.id, None)

    if call.data == 'student': # если выбран школьник
        user_role[call.message.chat.id] = 'student'
        bot.send_message(call.message.chat.id, '✏️ Введите свой класс (например, 9м, 11 хб)')
        waiting_grade[call.message.chat.id] = True # запоминаем - нужен ли ввод

    elif call.data == 'teacher': # если выбран учитель
        user_role[call.message.chat.id] = 'teacher'
        bot.send_message(call.message.chat.id, '✏️ Введите свою фамилию без пробелов, регистр не важен. Например: "вдовиченко", "Облендер"')
        waiting_teacher[call.message.chat.id] = True # также запомниаем

    elif call.data.startswith('day_'): # выбран уже и день недели и класс
        arr = call.data.split('_')
        if len(arr) == 3: # нужно расписание для учителя
            _, day_key, teacher = arr # ничего, день, учитель
            send_schedule(call.message.chat.id, day_key, teacher) # пишем расписание
        else: # нужно расписание для школьника
            _, day_key, grade, math, eng = arr
            send_schedule(call.message.chat.id, day_key, grade + '_' + math + '_' + eng) # пишем расписание

    elif call.data.startswith('choose_math_'): # выбор группы по математике
        arr = call.data.split('_')
        grade = arr[2]
        markup = types.InlineKeyboardMarkup()
        left = types.InlineKeyboardButton("Левая", callback_data=f'math_left_{grade}')
        right = types.InlineKeyboardButton('Правая', callback_data=f'math_right_{grade}')
        markup.row(left, right)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Какая у вас группа по математике?",
            reply_markup=markup
        )

    elif call.data.startswith('math_'): # уже выбрана группа по математике -> надо выбрать группу по английскому
        parts = call.data.split('_')
        math_group = parts[1]
        grade = parts[2]
        markup = types.InlineKeyboardMarkup()
        left = types.InlineKeyboardButton("Левая", callback_data=f"eng_left_{math_group}_{grade}")
        right = types.InlineKeyboardButton("Правая", callback_data=f"eng_right_{math_group}_{grade}")
        markup.row(left, right)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Какая у вас группа по английскому языку?",
            reply_markup=markup
        )

    elif call.data.startswith('eng_'):  # Выбрана группа по математике и по английскому
        parts = call.data.split('_')
        eng_group = parts[1]
        math_group = parts[2]
        grade = parts[3]
        full_id = f"{grade}_{math_group}_{eng_group}"  # Формат: 9м_left_left (класс_мат_англ)
        markup = types.InlineKeyboardMarkup()
        change_btn = types.InlineKeyboardButton("🔄 Изменить настройки", callback_data="change_settings")
        markup.row(change_btn)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Отлично! Все настройки сохранены:\n"
                 f"Класс: {grade}\n"
                 f"Математика: {'левая группа' if math_group == 'left' else 'правая группа'}\n"
                 f"Английский: {'левая группа' if eng_group == 'left' else 'правая группа'}",
            reply_markup=markup
        )
        send_days(call.message.chat.id, full_id)

    elif call.data == 'change_settings':
        waiting_grade[call.message.chat.id] = True
        waiting_teacher.pop(call.message.chat.id, None)  # на всякий случай
        user_role[call.message.chat.id] = 'student'  # оставляем роль ученика
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text='✏️ Введите свой класс заново (например, 9м, 11хб):'
        )

    bot.answer_callback_query(call.id) # убираем бесячий таймер на кнопках

@bot.message_handler(func=lambda message: True) # выбор класса/личности
def grade_choice(message):
    if message.chat.id in waiting_grade and waiting_grade[message.chat.id]: # ждём ввод класса в этом чате
        grade = message.text.lower().replace(' ', '')
        if grade in grades:
            del waiting_grade[message.chat.id] # удаляем этот чат из списка тех где ожидаем ввод класса
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Продолжить", callback_data=f"choose_math_{grade}")
            markup.row(button)
            bot.send_message(
                message.chat.id,
                "Теперь нужно выбрать ваши группы для предметов.\nНажмите 'Продолжить', чтобы начать.",
                reply_markup=markup
            ) # выбор групп по английскому и математике
        else:
            bot.reply_to(message, f'❌ Неправильно введён класс. Введите его ещё раз. Список предложенных классов: \n{", ".join(grades)}')
            # теперь надо ввести класс ещё раз
    elif message.chat.id in waiting_teacher and waiting_teacher[message.chat.id]: # ждём ввод фамилии в этом чате
        teacher = message.text.lower()
        if teacher in teachers:
            del waiting_teacher[message.chat.id] # удаляем этот чат из списка тех где ожидаем ввод фамилии
            send_days(message.chat.id, teacher) # просим выбрать день недели
        else:
            bot.reply_to(message, '❌ Неправильно введена фамилия. Введите ещё раз без пробелов. Примеры: "Зачиняев", "прадун"')
            # ждём ввода опять
    else:
        # если ваще хрень какая то, то просим начать заново всё
        bot.reply_to(message, 'Пожалуйста, сначала выберите роль через команду "/start"')

# функция выбора дня недели
def send_days(chat_id, variable):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Пн", callback_data=f"day_mon_{variable}"),
        types.InlineKeyboardButton("Вт", callback_data=f"day_tue_{variable}")
    )
    markup.row(
        types.InlineKeyboardButton("Ср", callback_data=f"day_wed_{variable}"),
        types.InlineKeyboardButton("Чт", callback_data=f"day_thu_{variable}")
    )
    markup.row(
        types.InlineKeyboardButton("Пт", callback_data=f"day_fri_{variable}"),
        types.InlineKeyboardButton("Сб", callback_data=f"day_sat_{variable}")
    )
    bot.send_message(chat_id, "📅 Выберите день недели:", reply_markup=markup)

# отправка расписания пользователю
def send_schedule(chat_id, day_key, variable):
    arr = variable.split('_')
    if len(arr) == 1:
        target = arr[0]
    else:
        target, math, eng = arr
    day_name = days[day_key]
    if target in grades: # для школьников
        header = f"📅 Расписание на {day_name.lower()}:" # тут мы также знаем класс, группу по математике, группу по английскому
        message = header + "\n\n"
        for lesson in lessons:
            message += f"<b>{lesson['subject']}</b>, {lesson['time']}, каб. {lesson['room']}\n"
        bot.send_message(chat_id, message, parse_mode='HTML')
    elif target in teachers: # для учителей
        header = f"📅 Расписание на {day_name.lower()} для учителя {target.capitalize()}:"
        if day_key == 'sun':
            bot.send_message(chat_id, f"{header}\n\nВ воскресенье занятий нет. Отдыхайте! ✨")
            return
        message = header + "\n\n"
        for lesson in lessons:
            message += f"<b>{lesson['subject']}</b> (9м), {lesson['time']}, каб. {lesson['room']}\n"
        bot.send_message(chat_id, message, parse_mode='HTML')
    else: # на всякий пожарный
        bot.send_message(chat_id, "Не удалось определить роль. Попробуйте заново через /start")

bot.polling(none_stop=True)