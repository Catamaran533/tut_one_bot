from bot_consts import *
from bot_functions import *
from student_notifications import *
from teachers_notifications import *
import threading
import time

def stop_bot():
    for chat in all_chats_id:
        try:
            bot.send_message(
                chat,
                "⚠️ Работа бота временно остановлена на техническое обслуживание.",
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"stop_bot упала из-за {e} от system")

def background_update():
    while True:
        time.sleep(UPDATE_TIME_MINUTES * 60)
        try:
            changes_students = schedule.update()
            if len(changes_students) > 0:
                notify_students(changes_students)
            changes_teachers = teachers_schedule.update()
            if len(changes_teachers) > 0:
                notify_teachers(changes_teachers)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"background_update упала из-за {e} от system")

schedule.update()
print('Расписание получено')
update_thread = threading.Thread(target=background_update, daemon=True)
update_thread.start()

try:
    user_class.clear()
    last_schedule_msg.clear()
    waiting_grade.clear()
    waiting_teacher.clear()
    bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
except Exception as e:
    logger.error(f"polling упала из-за {e} от system")
finally:
    stop_bot()