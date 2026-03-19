from bot_consts import *
from telebot import types

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
            lesson_rooms = result.get_cabs(i, group)
            message += f"{i + 1}. <b>{lesson}</b>, {lesson_time}, каб.: {', '.join(lesson_rooms)}\n"
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
            lesson_rooms = lesson.get_cabs()
            message += f"{i + 1}. <b>{lesson_name}</b>, {lesson_class}, {lesson_time}, каб.: {', '.join(lesson_rooms)}\n"
        if message == header + "\n\n":
            message += '💤 На этот день у Вас нет уроков'
        sent_message = bot.send_message(chat_id, message, parse_mode='HTML')
    else: # на всякий пожарный
        sent_message = bot.send_message(chat_id, "😬 Не удалось определить роль. Попробуйте заново через /start")
    last_schedule_msg[chat_id] = sent_message.message_id
