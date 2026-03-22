from bot_consts import *
import threading
import time

def delete_message_later(chat_id, message_id, delay=3600):
    def _delete():
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
    thread = threading.Thread(target=_delete)
    thread.start()

def notify_teachers(changes):
    try:
        for chat_id, teacher_name in user_teacher.items():
            if not notifications_enabled.get(chat_id, True):
                continue
            for change in changes:
                ch_teacher, ch_day = change
                if teacher_name.lower() == ch_teacher.lower():
                    try:
                        msg = bot.send_message(
                            chat_id,
                            f"⚠️ Внимание!\nВаше расписание на {day_cuts_reverse[ch_day]} изменилось!",
                            parse_mode='HTML'
                        )
                        delete_message_later(chat_id, msg.message_id)
                    except Exception as e:
                        logger.error(f"notify_teachers упала из-за {e} от {chat_id}")
    except Exception as e:
        logger.error(f"notify_teachers упала из-за {e} от system")