
from bot_functions import *



def notify_teachers(changes):
    for chat_id, teacher_name in user_teacher.items():
        for change in changes:
            ch_teacher, ch_day = change
            if teacher_name == ch_teacher:
                try:
                    bot.send_message(
                        chat_id,
                        f"⚠️ Внимание!\nВаше расписание на {day_cuts_reverse[ch_day]} изменилось!",
                        parse_mode='HTML'
                    )
                    send_schedule(chat_id, day_cuts_for_bot[ch_day], teacher_name)
                except:
                    pass