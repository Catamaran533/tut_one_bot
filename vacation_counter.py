from bot_consts import *
from datetime import datetime

def get_vacation_countdown():
    try:
        now = datetime.now()
        current_date = now.date()
        for vac in vacations:
            start = datetime.strptime(vac['start'], '%d-%m-%Y').date()
            end = datetime.strptime(vac['end'], '%d-%m-%Y').date()
            if start <= current_date <= end:
                end_datetime = datetime.strptime(vac['end'] + ' 23:59:59', '%d-%m-%Y %H:%M:%S')
                delta = end_datetime - now
                days = delta.days
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                seconds = delta.seconds % 60
                return (
                    f"🎉 **{vac['name']} каникулы уже идут!**\n\n"
                    f"⏳ До конца осталось:\n"
                    f"📅 {days} дн. {hours} ч. {minutes} мин. {seconds} сек."
                )

        for vac in vacations:
            start = datetime.strptime(vac['start'], '%d-%m-%Y')
            if start > now:
                delta = start - now
                days = delta.days
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                seconds = delta.seconds % 60
                return (
                    f"🏖️ **До {vac['name']} каникул:**\n\n"
                    f"⏳ Осталось:\n"
                    f"📅 {days} дн. {hours} ч. {minutes} мин. {seconds} сек.\n\n"
                    f"📅 Начало: {vac['start']}"
                )
        return "🎓 Учебный год завершён! Следующие каникулы — осенние 2026."
    except Exception as e:
        logger.error(f"get_vacation_countdown ошибка: {e}")
        return "⚠️ Ошибка при расчёте каникул"

@bot.message_handler(commands=['vacation', 'каникулы'])
def show_vacation(message):
    try:
        bot.send_message(message.chat.id, get_vacation_countdown(), parse_mode='Markdown')
    except Exception as e:
        logger.error(f"show_vacation упала из-за {e} от {message.from_user.username}")
        try:
            bot.send_message(message.chat.id, "⚠️ Ошибка. Попробуйте позже.")
        except:
            pass