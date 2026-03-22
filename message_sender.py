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
def send_schedule(chat_id, day_key, variable):
    try:
        last_msg = last_schedule_msg.get(chat_id)
        if last_msg:
            try:
                bot.delete_message(chat_id, last_msg)
            except:
                pass
        day_name = days[day_key]
        day_cut = day_cuts[day_key]

        if variable.endswith('_both'):
            real_grade = variable.replace('_both', '')
            header = f"📅 Расписание на {day_name.lower()}: для класса {real_grade}"
            result = schedule.get_student_day(real_grade, day_cut)
            lessons_left = []
            for i in range(8):
                lesson = result.get_lesson(i, 0)
                if lesson == '':
                    lessons_left.append(None)
                    continue
                lessons_left.append({
                    'name': lesson,
                    'time': result.get_time(i, 0),
                    'rooms': sorted(result.get_cabs(i, 0))
                })
            lessons_right = []
            for i in range(8):
                lesson = result.get_lesson(i, 1)
                if lesson == '':
                    lessons_right.append(None)
                    continue
                lessons_right.append({
                    'name': lesson,
                    'time': result.get_time(i, 1),
                    'rooms': sorted(result.get_cabs(i, 1))
                })
            schedules_match = True
            for i in range(8):
                left = lessons_left[i]
                right = lessons_right[i]
                if left is None and right is None:
                    continue
                if left is None or right is None:
                    schedules_match = False
                    break
                if left['name'] != right['name'] or left['time'] != right['time'] or left['rooms'] != right['rooms']:
                    schedules_match = False
                    break
            if schedules_match:
                message = header + "\n\n🔵🔴 <b>Для обеих групп:</b>\n"
                has_lessons = False
                for idx, l in enumerate(lessons_left):
                    if l is None:
                        continue
                    has_lessons = True
                    message += f"{idx + 1}. <b>{l['name']}</b>, {l['time']}, каб.: {', '.join(l['rooms'])}\n"
                if not has_lessons:
                    message += "💤 Нет уроков\n"
            else:
                message = header + "\n\n🔵 <b>Левая группа:</b>\n"
                if any(l is not None for l in lessons_left):
                    for idx, l in enumerate(lessons_left):
                        if l is None:
                            continue
                        message += f"{idx + 1}. <b>{l['name']}</b>, {l['time']}, каб.: {', '.join(l['rooms'])}\n"
                else:
                    message += "💤 Нет уроков\n"
                message += "\n🔴 <b>Правая группа:</b>\n"
                if any(l is not None for l in lessons_right):
                    for idx, l in enumerate(lessons_right):
                        if l is None:
                            continue
                        message += f"{idx + 1}. <b>{l['name']}</b>, {l['time']}, каб.: {', '.join(l['rooms'])}\n"
                else:
                    message += "💤 Нет уроков\n"
            sent_message = bot.send_message(chat_id, message, parse_mode='HTML')
            last_schedule_msg[chat_id] = sent_message.message_id
            return
        arr = variable.split('_')
        if len(arr) == 1:
            target = arr[0]
            math = None
            eng = None
        elif len(arr) == 3:
            target, math, eng = arr
        else:
            logger.error(f"Непонятный формат переменной: {variable}")
            bot.send_message(chat_id, "😬 Ошибка формата данных. Попробуйте выбрать класс заново.")
            return
        header = f"📅 Расписание на {day_name.lower()}: для класса {target}"
        if target in grades:
            lessons_list = []
            result = schedule.get_student_day(target, day_cut)
            for i in range(8):
                group = 0 if math == 'left' else 1
                if 'англ' in result.get_lesson(i, 0) or 'англ' in result.get_lesson(i, 1):
                    group = 0 if eng == 'left' else 1
                lesson = result.get_lesson(i, group)
                if lesson == '': continue
                lessons_list.append({
                    'name': lesson,
                    'time': result.get_time(i, group),
                    'rooms': result.get_cabs(i, group)
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

        elif target.lower() in [t.lower() for t in teachers]:
            header = f"📅 Расписание на {day_name.lower()} для учителя {target.capitalize()}: "
            message = header + "\n\n"
            lessons_list = []
            for i in range(8):
                lesson = teachers_schedule.get_teachers_lesson(target, day_cut, i)
                if not lesson: continue
                lesson_name = lesson.get_lesson_name()
                if lesson_name == '': continue
                lessons_list.append(
                    f"{i + 1}. <b>{lesson_name}</b>, {lesson.get_class_name()}, {lesson.get_time()}, каб.: {', '.join(lesson.get_cabs())}\n")
            if lessons_list:
                message += "".join(lessons_list)
            else:
                message += '💤 На этот день у Вас нет уроков'
        else:
            message = "😬 Не удалось определить роль."
        sent_message = bot.send_message(chat_id, message, parse_mode='HTML')
        last_schedule_msg[chat_id] = sent_message.message_id

    except Exception as e:
        logger.error(f"send_schedule упала из-за {e} от {chat_id}")
        try:
            bot.send_message(chat_id, "⚠️ Ошибка при выводе расписания. Попробуйте позже.")
        except:
            pass