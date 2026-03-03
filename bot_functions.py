from telebot import types
from bot_consts import *
from TeachersTable import *
from TeachersLesson import *
from room_formatter import format_rooms

def get_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn_menu = types.KeyboardButton('/menu')
    markup.row(btn_menu)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    all_chats_id.add(message.chat.id)
    text = (
        "👋 Приветствую! Для начала работы введите /menu \n"
        "Чтобы получить подробную информацию о работе бота - введите /help"
    )
    bot.send_message(
        message.chat.id,
        text,
        parse_mode='HTML',
        reply_markup = get_menu_keyboard()
    )

@bot.message_handler(commands=['menu'])
def show_menu(message):
    all_chats_id.add(message.chat.id)
    chat_id = message.chat.id
    user_role.pop(chat_id, None)
    user_class.pop(chat_id, None)
    user_teacher.pop(chat_id, None)
    waiting_grade.pop(chat_id, None)
    waiting_teacher.pop(chat_id, None)
    markup = types.InlineKeyboardMarkup() # кнопки
    site_button = types.InlineKeyboardButton('Открыть общее расписание', url='https://clck.ru/3QZjCY') # расписание
    markup.row(site_button)
    student_role = types.InlineKeyboardButton('🧑‍🎓 Ученик', callback_data='student') # выбор ученика
    teacher_role = types.InlineKeyboardButton('👩‍🏫 Учитель', callback_data='teacher') # выбор учителя
    markup.row(student_role, teacher_role)
    bot.send_message(
        message.chat.id,
        '👀 Вы можете увидеть общее расписание уроков, либо посмотреть специализированный вариант специально для Вас - для этого выберите роль - <b>🧑‍🎓школьник(родитель школьника)</b> или <b>👩‍🏫учитель</b>.',
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['help']) # /help
def help_user(message):
    text = (
        "Этот телеграм-бот создан для оперативного получения школьного расписания в ЮМШ.\n\n"
        "📋 Команды бота:\n"
        "/start – начать работу с ботом\n"
        "/menu - выйти обратно в главное меню с выбором роли\n"
        "/help – получить помощь при непонимании\n"
        "/notifications – включить/выключить уведомления об изменениях в расписании\n\n"
        "После ввода /menu выберите роль - ученик или учитель. После чего введите класс для ученика либо фамилию для учителя.\n"
        "Если вы выбрали школьника, то выберите ещё группу по математике и по английскому(в случае ошибки эти настройки можно изменить)\n"
        "Теперь осталось только выбрать день недели и всё!"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['notifications'])
def toggle_notifications(message):
    current = notifications_enabled.get(message.chat.id, True)
    notifications_enabled[message.chat.id] = not current
    if not current:
        text = "✅ Уведомления <b>включены</b>!\nТеперь бот будет присылать изменения."
    else:
        text = "🔕 Уведомления <b>отключены</b>!\nБот больше не будет беспокоить вас сообщениями."
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True) # ответ на функции кнопок
def callback_answer(call):
    bot.answer_callback_query(call.id)
    waiting_grade.pop(call.message.chat.id, None)
    waiting_teacher.pop(call.message.chat.id, None)

    if call.data == 'student': # если выбран школьник
        user_role[call.message.chat.id] = 'student'
        bot.send_message(call.message.chat.id, '✏️ Введите свой класс (например, 9м, 11 хб)')
        waiting_grade[call.message.chat.id] = True # запоминаем - нужен ли ввод
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        except:
            pass

    elif call.data == 'teacher': # если выбран учитель
        user_role[call.message.chat.id] = 'teacher'
        bot.send_message(call.message.chat.id, '✏️ Введите свою фамилию без пробелов, регистр не важен. Например: "вдовиченко", "Облендер"')
        waiting_teacher[call.message.chat.id] = True # также запомниаем
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        except:
            pass

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
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🔢 Какая у вас группа по профильному предмету? ",
                reply_markup=markup
            )
        except:
            pass

    elif call.data.startswith('math_'): # уже выбрана группа по математике -> надо выбрать группу по английскому
        parts = call.data.split('_')
        math_group = parts[1]
        grade = parts[2]
        markup = types.InlineKeyboardMarkup()
        left = types.InlineKeyboardButton("Левая", callback_data=f"eng_left_{math_group}_{grade}")
        right = types.InlineKeyboardButton("Правая", callback_data=f"eng_right_{math_group}_{grade}")
        markup.row(left, right)
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🇬🇧 Какая у вас группа по английскому языку? ",
                reply_markup=markup
            )
        except:
            pass

    elif call.data.startswith('eng_'):  # Выбрана группа по математике и по английскому
        parts = call.data.split('_')
        eng_group = parts[1]
        math_group = parts[2]
        grade = parts[3]
        full_id = f"{grade}_{math_group}_{eng_group}"  # Формат: 9м_left_left (класс_мат_англ)
        user_class[call.message.chat.id] = full_id

        markup = types.InlineKeyboardMarkup()
        change_btn = types.InlineKeyboardButton("🔄 Изменить настройки", callback_data="change_settings")
        markup.row(change_btn)
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"👌 Отлично! Все настройки сохранены:\n"
                     f"Класс: {grade}\n"
                     f"Профиль: {'левая группа' if math_group == 'left' else 'правая группа'}\n"
                     f"Английский: {'левая группа' if eng_group == 'left' else 'правая группа'}",
                reply_markup=markup
            )
        except:
            pass
        send_days(call.message.chat.id, full_id)

    elif call.data == 'change_settings':
        waiting_grade[call.message.chat.id] = True
        waiting_teacher.pop(call.message.chat.id, None)  # на всякий случай
        user_role[call.message.chat.id] = 'student'  # оставляем роль ученика
        user_class.pop(call.message.chat.id, None)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text='✏️ Введите свой класс заново (например, 9м, 11хб):'
        )

@bot.message_handler(func=lambda message: True) # выбор класса/личности
def text_request(message):
    if message.forward_date or message.forward_from:
        bot.reply_to(message, "❌ Пересылка сообщений в бота - запрещена")
        return
    if message.text.lower() == 'обновить' and message.from_user.username in admins:
        from student_notifications import notify_students
        from teachers_notifications import notify_teachers
        changes_students = schedule.update()
        if len(changes_students) > 0:
            notify_students(changes_students)
        else:
            bot.send_message(
                message.chat.id,
                'Расписание для школьников не изменилось.'
            )
        changes_teachers = teachers_schedule.update()
        if len(changes_teachers) > 0:
            notify_teachers(changes_teachers)
        else:
            bot.send_message(
                message.chat.id,
                'Расписание для учителей не изменилось.'
            )
        bot.reply_to(
            message,
            'Привет, информация о расписание была обновлена.'
        )
    elif message.chat.id in waiting_grade and waiting_grade[message.chat.id]: # ждём ввод класса в этом чате
        grade = message.text.lower().replace(' ', '')
        if grade in grades:
            del waiting_grade[message.chat.id] # удаляем этот чат из списка тех где ожидаем ввод класса
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Продолжить", callback_data=f"choose_math_{grade}")
            markup.row(button)
            bot.send_message(
                message.chat.id,
                "↔️ Теперь нужно выбрать ваши группы для предметов.\nНажмите 'Продолжить', чтобы начать.",
                reply_markup=markup
            ) # выбор групп по английскому и математике
        else:
            bot.reply_to(message, f'❌ Неправильно введён класс. Введите его ещё раз. Список предложенных классов: \n{", ".join(grades)}')
            # теперь надо ввести класс ещё раз
    elif message.chat.id in waiting_teacher and waiting_teacher[message.chat.id]: # ждём ввод фамилии в этом чате
        teacher = message.text.lower()
        if teacher in teachers:
            del waiting_teacher[message.chat.id] # удаляем этот чат из списка тех где ожидаем ввод фамилии
            user_teacher[message.chat.id] = teacher
            send_days(message.chat.id, teacher) # просим выбрать день недели
        else:
            bot.reply_to(message, '❌ Неправильно введена фамилия. Введите ещё раз без пробелов. Примеры: "Зачиняев", "прадун"')
            # ждём ввода опять
    else:
        # если ваще хрень какая то, то просим начать заново всё
        bot.reply_to(message, '😬 Пожалуйста, сначала выберите роль через команду "/start"')

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
def send_schedule(chat_id, day_key, variable, delete_previous=True):
    if delete_previous:
        last_msg = last_schedule_msg.get(chat_id)
        if last_msg:
            try:
                bot.delete_message(chat_id, last_msg)
            except:
                pass
    arr = variable.split('_')
    if len(arr) == 1:
        target = arr[0]
    else:
        target, math, eng = arr
    day_name = days[day_key]
    day_cut = day_cuts[day_key]
    if target in grades: # для школьников
        header = f"📅 Расписание на {day_name.lower()}: для класса {target}" # тут мы также знаем класс, группу по математике, группу по английскому
        message = header + "\n\n"
        result = schedule.get_student_day(target, day_cut)
        for i in range(8):
            group = 0 if math == 'left' else 1
            if 'англ' in result.get_lesson(i, 0) or 'англ' in result.get_lesson(i, 1):
                group = 0 if eng == 'left' else 1
            lesson = result.get_lesson(i, group)
            if lesson == '': continue
            lesson_time = result.get_time(i, group)
            lesson_rooms = format_rooms(result.get_cabs(i, group))
            message += f"{i + 1}. <b>{lesson}</b>, {lesson_time}, каб.: {lesson_rooms}\n"
        if message == header + "\n\n":
            message += '💤 На этот день у Вас нет уроков'
        sent_message = bot.send_message(chat_id, message, parse_mode='HTML')
    elif target.lower() in [t.lower() for t in teachers]: # для учителей
        header = f"📅 Расписание на {day_name.lower()} для учителя {target.capitalize()}:"
        message = header + "\n\n"
        for i in range(8):
            lesson = teachers_schedule.get_teachers_lesson(target, day_cut, i)
            if not lesson: continue
            lesson_name = lesson.get_lesson_name()
            if lesson_name == '': continue
            lesson_class = lesson.get_class_name()
            lesson_time = lesson.get_time()
            lesson_rooms = format_rooms(lesson.get_cabs())
            message += f"{i + 1}. <b>{lesson_name}</b>, {lesson_class}, {lesson_time}, каб.: {lesson_rooms}\n"
        if message == header + "\n\n":
            message += '💤 На этот день у Вас нет уроков'
        sent_message = bot.send_message(chat_id, message, parse_mode='HTML')
    else: # на всякий пожарный
        sent_message = bot.send_message(chat_id, "😬 Не удалось определить роль. Попробуйте заново через /start")
    last_schedule_msg[chat_id] = sent_message.message_id
