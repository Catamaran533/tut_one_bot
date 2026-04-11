from bot_consts import *
from datetime import datetime

def parse_lesson_time(time_str): # парсинг времени урока
    try:
        if not time_str or not isinstance(time_str, str):
            return None, None
        time_str = time_str.strip()
        time_str = time_str.replace('–', '-').replace('—', '-').replace('−', '-')
        if '-' not in time_str:
            return None, None
        parts = time_str.split('-')
        if len(parts) != 2:
            return None, None
        start_str = parts[0].strip().replace('.', ':')
        end_str = parts[1].strip().replace('.', ':')
        # время начала и конца
        start_parts = start_str.split(':')
        end_parts = end_str.split(':')
        if len(start_parts) == 2 and len(start_parts[0]) == 1:
            start_str = '0' + start_str
        if len(end_parts) == 2 and len(end_parts[0]) == 1:
            end_str = '0' + end_str
        start_time = datetime.strptime(start_str, '%H:%M').time()
        end_time = datetime.strptime(end_str, '%H:%M').time()
        # делаем это в формат времени питоновский
        return start_time, end_time
    except Exception as e:
        logger.error(f"parse_lesson_time ошибка: {e} для '{time_str}'")
        return None, None

def find_location(teacher_name):
    try:
        teacher_lower = teacher_name.lower().strip()
        teacher_found = None
        for t in teachers:
            if t.lower() == teacher_lower:
                teacher_found = t
                break
        if not teacher_found:
            return None, None, 'teacher_not_found' # не нашли препода
        current_weekday = datetime.now().weekday()
        day_cut = days_map.get(current_weekday, 'ПН')
        current_time = datetime.now().time()
        last_lesson_cab = None
        last_lesson_num = None
        has_lessons_today = False
        lessons_started = False
        for i in range(8):
            lesson = teachers_schedule.get_teachers_lesson(teacher_found, day_cut, i) # урок номер i в этот день у нужного учителя
            if not lesson:
                continue
            lesson_name = lesson.get_lesson_name()
            if not lesson_name or lesson_name == '':
                continue
            has_lessons_today = True
            time_str = lesson.get_time()
            start_time, end_time = parse_lesson_time(time_str)
            if start_time is None:
                continue
            if current_time >= start_time:
                lessons_started = True
                if end_time and current_time >= end_time: # урок закончился
                    cabs = lesson.get_cabs()
                    if cabs and len(cabs) > 0:
                        last_lesson_cab = cabs[0]
                        last_lesson_num = i + 1
                else:
                    cabs = lesson.get_cabs() # урок прям щас
                    if cabs and len(cabs) > 0:
                        last_lesson_cab = cabs[0]
                        last_lesson_num = i + 1
                    return last_lesson_cab, last_lesson_num, 'found'
        # выбираем статус который надо вернуть
        if not has_lessons_today:
            return None, None, 'no_lessons_today'
        if not lessons_started:
            return None, None, 'not_started'
        if last_lesson_cab:
            return last_lesson_cab, last_lesson_num, 'found'
        else:
            return None, None, 'no_cab_data'
    except Exception as e:
        logger.error(f"find_location упала из-за {e} для учителя {teacher_name}")
        return None, None, 'error'

def send_teacher_location(chat_id, teacher_name, cab, lesson_num, status):
    try:
        if status == 'teacher_not_found':
            message = (
                f"❌ Учитель с фамилией '{teacher_name}' не найден.\n"
                "Проверьте правильность написания или попробуйте другую фамилию.\n\n"
                "Для возврата в меню введите /menu"
            )
        elif status == 'no_lessons_today':
            message = (
                f"📅 У учителя {teacher_name.capitalize()} сегодня нет уроков.\n\n"
                "Для возврата в меню введите /menu"
            )
        elif status == 'not_started':
            message = (
                f"⏰ У учителя {teacher_name.capitalize()} уроки сегодня еще не начались.\n"
                "Попробуйте позже.\n\n"
                "Для возврата в меню введите /menu"
            )
        elif status == 'no_cab_data':
            message = (
                f"📍 Учитель {teacher_name.capitalize()} проводил уроки сегодня,\n"
                "но информация о кабинете отсутствует в расписании.\n\n"
                "Для возврата в меню введите /menu"
            )
        elif status == 'found':
            message = (
                f"✅ Последний урок ({lesson_num}) учителя {teacher_name.capitalize()} "
                f"проходил в кабинете <b>{cab}</b>.\n\n"
                "Для возврата в меню введите /menu"
            )
        else:
            message = (
                "⚠️ Произошла ошибка при поиске информации.\n"
                "Попробуйте позже или введите /menu для возврата в главное меню."
            )
        bot.send_message(chat_id, message, parse_mode='HTML')
    except Exception as e:
        logger.error(f"send_teacher_location упала из-за {e} от {chat_id}")