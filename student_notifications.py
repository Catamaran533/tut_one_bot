from bot_consts import *
import threading
import time

def delete_message_later(chat_id, message_id, delay=3600): # функция удаления уведомленея
    def delete_mes():
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
    thread = threading.Thread(target=delete_mes) # запускаем фоново
    thread.start()

def notify_students(changes):
    try:
        for chat_id, full_id in user_class.items(): # перебираем школьников
            if not notifications_enabled.get(chat_id, True): # отключены уведомления
                continue
            only_class = full_id.split('_')[0]
            notified_days = [] # измененные дни
            for change in changes:
                ch_class, ch_day = change
                if only_class == ch_class and ch_day not in notified_days: # день ещё не прислан
                    try:
                        msg = bot.send_message(
                            chat_id,
                            f"⚠️ Внимание!\nРасписание на {day_cuts_reverse[ch_day]} изменилось!",
                            parse_mode='HTML'
                        )
                        delete_message_later(chat_id, msg.message_id)
                        notified_days.append(ch_day)
                    except Exception as e:
                        logger.error(f"notify_students упала из-за {e} от {chat_id}")
    except Exception as e:
        logger.error(f"notify_students упала из-за {e} от system")