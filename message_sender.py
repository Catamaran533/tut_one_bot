from bot_consts import *
from telebot import types

# функция выбора дня недели
def send_days(chat_id, variable):
    try:
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
    except Exception as e:
        logger.error(f"send_days упала из-за {e} от {chat_id}")

# отправка расписания пользователю
def send_schedule(chat_id, day_key, variable, delete_previous=True):
    try:
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
            lessons_list = []
            result = schedule.get_student_day(target, day_cut)
            for i in range(8):
                group = 0 if math == 'left' else 1
                if 'англ' in result.get_lesson(i, 0) or 'англ' in result.get_lesson(i, 1):
                    group = 0 if eng == 'left' else 1
                lesson = result.get_lesson(i, group)
                if lesson == '': continue
                lesson_time = result.get_time(i, group)
                lesson_rooms = result.get_cabs(i, group)
                lessons_list.append({
                    'name': lesson,
                    'time': lesson_time,
                    'rooms': lesson_rooms
                })

            is_all_same = False
            if len(lessons_list) == 8:
                first_lesson = lessons_list[0]
                all_match = True
                for l in lessons_list:
                    if l['name'] != first_lesson['name'] or l['rooms'] != first_lesson['rooms']:
                        all_match = False
                        break
                if all_match:
                    is_all_same = True
                    start_time = lessons_list[0]['time'].split('-')[0]
                    end_time = lessons_list[-1]['time'].split('-')[1]
                    rooms_str = ', '.join(first_lesson['rooms'])
                    message = header + "\n\n"
                    message += f"1-8. <b>{first_lesson['name']}</b>, {start_time}-{end_time}, каб.: {rooms_str}\n"

            if not is_all_same:
                message = header + "\n\n"
                for idx, l in enumerate(lessons_list):
                    message += f"{idx + 1}. <b>{l['name']}</b>, {l['time']}, каб.: {', '.join(l['rooms'])}\n"
                if message == header + "\n\n":
                    message += '💤 На этот день у Вас нет уроков'

        elif target.lower() in [t.lower() for t in teachers]: # для учителей
            header = f"📅 Расписание на {day_name.lower()} для учителя {target.capitalize()}:"
            message = header + "\n\n"
            lessons_list = []
            for i in range(8):
                lesson = teachers_schedule.get_teachers_lesson(target, day_cut, i)
                if not lesson:
                    continue
                lesson_name = lesson.get_lesson_name()
                if lesson_name == '':
                    continue
                lesson_class = lesson.get_class_name()
                lesson_time = lesson.get_time()
                lesson_rooms = lesson.get_cabs()
                lessons_list.append(
                    f"{i + 1}. <b>{lesson_name}</b>, {lesson_class}, {lesson_time}, каб.: {', '.join(lesson_rooms)}\n")
            if lessons_list:
                message += "".join(lessons_list)
            else:
                message += '💤 На этот день у Вас нет уроков'
        else: # на всякий пожарный
            message = "😬 Не удалось определить роль. Попробуйте заново через /menu"

        sent_message = bot.send_message(chat_id, message, parse_mode='HTML')
        last_schedule_msg[chat_id] = sent_message.message_id
    except Exception as e:
        logger.error(f"send_schedule упала из-за {e} от {chat_id}")
