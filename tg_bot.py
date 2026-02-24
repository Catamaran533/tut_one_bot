from bot_consts import *
from bot_functions import *
from notifications import *
import threading
import time

def background_update():
    while True:
        time.sleep(UPDATE_TIME_MINUTES * 60)
        try:
            changes = schedule.update()
            notify(changes)
        except:
            pass

schedule.update()
print('Расписание получено')

update_thread = threading.Thread(target=background_update, daemon=True)
update_thread.start()

bot.polling(none_stop=True)