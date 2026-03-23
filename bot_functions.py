from telebot import types
from bot_consts import *
from TeachersTable import *
from TeachersLesson import *
from message_sender import send_schedule, send_days
from teacher_location import *

def get_menu_keyboard(): # функция, чтобы кнопка "/menu" всегда отображалась снизу
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn_menu = types.KeyboardButton('/menu')
    markup.row(btn_menu)
    return markup

@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'video_note',
                                    'document', 'sticker', 'location', 'contact',
                                    'venue', 'invoice', 'animation'])
def warn_user(message): # обрабатываем любое сообщение кроме текста
    try:
        bot.reply_to(message, "Бот не поддерживает такой формат, только текст. ✍️")
    except Exception as e:
        logger.error(f"warn_user упала из-за {e} от {message.from_user.username}")

@bot.message_handler(commands=['start', 'старт']) # стартовая функция
def send_welcome(message):
    try:
        all_chats_id.add(message.chat.id)
        text = (
            "👋 Приветствую! Для начала работы введите /menu \n"
            "Чтобы получить справку о работе бота - введите /help"
        )
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup = get_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"send_welcome упала из-за {e} от {message.from_user.username}")

@bot.message_handler(commands=['menu', 'меню'])
def show_menu(message): # главное меню бота
    try:
        all_chats_id.add(message.chat.id)
        chat_id = message.chat.id
        # очищаем всё, т.к. эта функция - фактический перезапуск бота
        user_role.pop(chat_id, None)
        user_class.pop(chat_id, None)
        user_teacher.pop(chat_id, None)
        waiting_grade.pop(chat_id, None)
        waiting_teacher.pop(chat_id, None)
        waiting_location_teacher.pop(chat_id, None)
        markup = types.InlineKeyboardMarkup() # кнопки
        site_button = types.InlineKeyboardButton('Открыть общее расписание', url='https://clck.ru/3QZjCY') # расписание
        markup.row(site_button)
        student_role = types.InlineKeyboardButton('🧑‍🎓 Ученик', callback_data='student') # выбор ученика
        teacher_role = types.InlineKeyboardButton('👩‍🏫 Учитель', callback_data='teacher') # выбор учителя
        markup.row(student_role, teacher_role)
        location_btn = types.InlineKeyboardButton('📍 Узнать, где учитель', callback_data='teacher_location')
        markup.row(location_btn)
        bot.send_message(
            message.chat.id,
            '👀 Вы можете увидеть общее расписание уроков, либо посмотреть специализированный вариант специально для Вас - для этого выберите роль - 🧑‍🎓школьник(родитель школьника) или 👩‍🏫учитель.\n\n'
            '📍 Также вы можете быстро узнать, в каком кабинете находится учитель прямо сейчас!',
            reply_markup=markup,
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"show_menu упала из-за {e} от {message.from_user.username}")

@bot.message_handler(commands=['help', 'помощь']) # /help
def help_user(message):
    try:
        text = (
            "Этот телеграм-бот создан для оперативного получения школьного расписания в ЮМШ.\n\n"
            "📋 Команды бота:\n"
            "/start – начать работу с ботом\n"
            "/menu или /меню - выйти обратно в главное меню с выбором роли\n"
            "/help или /помощь – получить справку при непонимании\n"
            "/notifications или /уведомления – включить/выключить уведомления об изменениях в расписании\n\n"
            "После ввода /menu выберите роль - ученик или учитель. После чего введите класс для ученика либо фамилию для учителя.\n"
            "Если вы выбрали школьника, то выберите ещё группу по математике и по английскому(в случае ошибки эти настройки можно изменить)\n"
            "Теперь осталось только выбрать день недели и всё!"
        )
        bot.send_message(message.chat.id, text)
    except Exception as e:
        logger.error(f"help_user упала из-за {e} от {message.from_user.username}")

@bot.message_handler(commands=['notifications', 'уведомления'])
def toggle_notifications(message):
    try:
        current = notifications_enabled.get(message.chat.id, True)
        notifications_enabled[message.chat.id] = not current
        if not current:
            text = "✅ Уведомления <b>включены</b>!\nТеперь бот будет присылать изменения."
        else:
            text = "🔕 Уведомления <b>отключены</b>!\nБот больше не будет беспокоить вас сообщениями."
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    except Exception as e:
        logger.error(f"toggle_notifications упала из-за {e} от {message.from_user.username}")

@bot.callback_query_handler(func=lambda call: True) # ответ на функции кнопок
def callback_answer(call):
    if call.from_user.username == 'Anton1991ASDF':
        return
    try:
        bot.answer_callback_query(call.id)
        waiting_grade.pop(call.message.chat.id, None)
        waiting_teacher.pop(call.message.chat.id, None)
        waiting_location_teacher.pop(call.message.chat.id, None)
        # удаляем его из списка тех, где ожидаем ввод
        if call.data == 'student':  # если выбран школьник
            user_role[call.message.chat.id] = 'student'
            waiting_grade[call.message.chat.id] = True
            # ждём ввод класса
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='✏️ Введите свой класс (например, 9м, 11хб)',
                    reply_markup=None
                )
            except Exception:
                pass

        elif call.data == 'teacher': # если выбран учитель
            user_role[call.message.chat.id] = 'teacher'
            waiting_teacher[call.message.chat.id] = True
            # ждём ввод фамилии
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='✏️ Введите свою фамилию без пробелов, регистр не важен. Например: "вдовиченко", "Зачиняев"',
                    reply_markup=None
                )
            except Exception:
                pass

        elif call.data.startswith('both_groups_'): # юзер выбрал расписание для обеих групп
            grade = call.data.split('_')[2] # достаём его класс
            user_role[call.message.chat.id] = 'student' # помечаем его
            user_class[call.message.chat.id] = f"{grade}_both"
            waiting_grade.pop(call.message.chat.id, None)
            waiting_teacher.pop(call.message.chat.id, None)
            # удаляем его ото всюду
            markup = types.InlineKeyboardMarkup()
            change_btn = types.InlineKeyboardButton("🔄 Изменить настройки", callback_data="change_settings")
            markup.row(change_btn)
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=f"👌 Отлично! Настройки сохранены:\nКласс: {grade}\nРежим: 🔵🔴 Обе группы (левая и правая)",
                    reply_markup=markup
                )
            except:
                pass
            send_days(call.message.chat.id, f"{grade}_both")

        elif call.data.startswith('day_'): # выбран день недели и все настройки
            arr = call.data.split('_')
            day_key = arr[1]
            if len(arr) == 3: # значит учитель
                teacher = arr[2]
                send_schedule(call.message.chat.id, day_key, teacher)
            elif len(arr) == 4 and arr[3] == 'both': # ученик выбрал обе группы
                grade = arr[2]
                variable = f"{grade}_both"
                send_schedule(call.message.chat.id, day_key, variable)
            else: # ученик выбрал расписание только для 1 группы по профильному и по английскому
                grade = arr[2]
                math = arr[3]
                eng = arr[4]
                variable = f"{grade}_{math}_{eng}"
                send_schedule(call.message.chat.id, day_key, variable)

        elif call.data.startswith('choose_math_'): # выбор группы по профильному (позже выяснили, что профиль != математика, но уже забил в коде)
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
                    text="🇬🇧 Какая у вас группа по английскому языку?",
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
            user_class[call.message.chat.id] = full_id # запоминаем настройки для него
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

        elif call.data == 'change_settings': # возможность изменить выбранные настройки у ученика
            last_schedule_msg.pop(call.message.chat.id, None)
            waiting_grade[call.message.chat.id] = True # значит заново ждём класс и группы
            waiting_teacher.pop(call.message.chat.id, None)  # на всякий случай
            user_role[call.message.chat.id] = 'student'  # оставляем роль ученика
            user_class.pop(call.message.chat.id, None)
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            ) # удаляем прошлое сообщение
            bot.send_message(
                chat_id=call.message.chat.id,
                text='✏️ Введите свой класс заново (например, 9м, 11хб):'
            )

        elif call.data == 'teacher_location': # юзер хочет узнать, где сейчас препод
            waiting_location_teacher[call.message.chat.id] = True
            waiting_grade.pop(call.message.chat.id, None)
            waiting_teacher.pop(call.message.chat.id, None)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='📍 Введите фамилию учителя (регистр не важен):\nНапример: вдовиЧЕНко, Клюев, АБАКУМОВА',
                reply_markup=None
            )

    except Exception as e:
        logger.error(f"callback_answer упала из-за {e} от {call.from_user.username}")

@bot.message_handler(func=lambda message: True) # выбор класса/личности
def text_request(message):
    try:
        if message.forward_date or message.forward_from: # обрабатываем пересланный текст
            bot.reply_to(message, "❌ Пересылка сообщений в бота - не поддерживается")
            return
        if message.chat.id in waiting_grade and waiting_grade[message.chat.id]: # ждём ввод класса в этом чате
            grade = message.text.lower().replace(' ', '')
            if grade in grades: # если введён верно
                del waiting_grade[message.chat.id] # удаляем этот чат из списка тех где ожидаем ввод класса
                markup = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton("Продолжить (выбор групп)", callback_data=f"choose_math_{grade}")
                both_btn = types.InlineKeyboardButton("Выводить расписание обеих групп",
                                                      callback_data=f"both_groups_{grade}")
                markup.row(button)
                markup.row(both_btn)
                bot.send_message(
                    message.chat.id,
                    "↔️ Теперь нужно выбрать ваши группы для предметов.\nНажмите 'Продолжить', чтобы выбрать группы, или 'Выводить обе', чтобы видеть всё сразу. ",
                    reply_markup=markup
                )
            else:
                bot.reply_to(message, f'❌ Неправильно введён класс. Введите его ещё раз. Список предложенных классов: \n{", ".join(grades)}')
                # теперь надо ввести класс ещё раз
        elif message.chat.id in waiting_teacher and waiting_teacher[message.chat.id]: # ждём ввод фамилии в этом чате
            teacher = message.text.lower()
            if teacher in teachers: # если верно введена
                del waiting_teacher[message.chat.id] # удаляем этот чат из списка тех где ожидаем ввод фамилии
                user_teacher[message.chat.id] = teacher
                send_days(message.chat.id, teacher) # просим выбрать день недели
            else:
                bot.reply_to(message, '❌ Неправильно введена фамилия. Введите ещё раз без пробелов. Примеры: "Зачиняев", "прадун"')
                # ждём ввода опять
        elif message.chat.id in waiting_location_teacher and waiting_location_teacher[message.chat.id]: # ждём ввод фамилии для поиска
            teacher_name = message.text.strip()
            if not teacher_name: # если пустое соо
                bot.reply_to(message, '❌ Введите фамилию учителя.')
                return
            cab, lesson_num, status = find_location(teacher_name) # ищём где он
            send_teacher_location(message.chat.id, teacher_name, cab, lesson_num, status) # выводим пользователю
            if status == 'found': # если нашли - убираем чат из списка
                waiting_location_teacher.pop(message.chat.id, None)
        else:
            # если ваще хрень какая то, то просим начать заново всё
            bot.reply_to(message, '😬 Произошла ошибка. Пожалуйста, выберите заново роль через команду "/menu"')
    except Exception as e:
        logger.error(f"text_request упала из-за {e} от {message.from_user.username}")
