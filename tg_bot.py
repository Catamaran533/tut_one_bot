from bot_consts import *
from bot_functions import *
from student_notifications import *
from teachers_notifications import *
import threading
import time

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

bot.polling(none_stop=True)