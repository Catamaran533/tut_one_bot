from bot_consts import *
from message_sender import send_schedule

def notify_students(changes):
    try:
        for chat_id, full_id in user_class.items():
            if not notifications_enabled.get(chat_id, True):
                continue
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
                        send_schedule(chat_id, day_cuts_for_bot[ch_day], full_id, delete_previous=False)
                    except Exception as e:
                        logger.error(f"notify_students упала из-за {e} от {chat_id}")
    except Exception as e:
        logger.error(f"notify_students упала из-за {e} от system")