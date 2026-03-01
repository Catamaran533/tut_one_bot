from bot_consts import *
from bot_functions import *
from student_notifications import *
from teachers_notifications import *
import threading
import time

def stop_bot():
    all_chats = set(user_class.keys()) | set(user_teacher.keys())
    for chat in all_chats:
        try:
            bot.send_message(
                chat,
                "⚠️ <b>Внимание!</b>\nРабота бота временно остановлена на техническое обслуживание.",
                parse_mode='HTML'
            )
        except Exception as e:
            pass

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
            print(f"Ошибка обновления: {e}")

schedule.update()
print('Расписание получено')
update_thread = threading.Thread(target=background_update, daemon=True)
update_thread.start()

try:
    bot.polling(none_stop=True)
finally:
    stop_bot()