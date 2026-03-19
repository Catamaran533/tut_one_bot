from bot_consts import *
from message_sender import send_schedule

def notify_teachers(changes):
    try:
        for chat_id, teacher_name in user_teacher.items():
            if not notifications_enabled.get(chat_id, True):
                continue
            for change in changes:
                ch_teacher, ch_day = change
                if teacher_name.lower() == ch_teacher.lower():
                    try:
                        bot.send_message(
                            chat_id,
                            f"⚠️ Внимание!\nВаше расписание на {day_cuts_reverse[ch_day]} изменилось!",
                            parse_mode='HTML'
                        )
                        send_schedule(chat_id, day_cuts_for_bot[ch_day], teacher_name, delete_previous=False)
                    except Exception as e:
                        logger.error(f"notify_teachers упала из-за {e} от {chat_id}")
    except Exception as e:
        logger.error(f"notify_teachers упала из-за {e} от system")