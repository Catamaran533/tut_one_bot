from bot_consts import *
import bot_functions
import threading
import time
from bot_functions import send_schedule


def background_update():
    while True:
        time.sleep(UPDATE_TIME_MINUTES * 60)
        try:
            changes = schedule.update()
            for chat_id, full_id in user_class.items():
                only_class = full_id.split('_')[0]
                for change in changes:
                    ch_class, ch_day = change
                    if only_class == ch_class:
                        try:
                            bot.send_message(
                                chat_id,
                                f"⚠️ <b>Внимание!</b>\nРасписание на <b>{day_cuts_reverse[ch_day]}</b> изменилось!",
                                parse_mode='HTML'
                            )
                            send_schedule(chat_id, day_cuts_for_bot[ch_day], full_id)
                        except:
                            pass # если бот заблокан
        except:
            pass

schedule.update()
print('Расписание получено')
update_thread = threading.Thread(target=background_update, daemon=True)
update_thread.start()

bot.polling(none_stop=True)