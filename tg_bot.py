import telebot
from telebot import types
bot = telebot.TeleBot(token='8275369590:AAG2CUbhj6Kf6qsCg3V3bAZp6Ve4XxcTp74') # бот - @UrokPlusBot

@bot.message_handler(commands=['start']) # /start
def send_welcome(message):
    markup = types.InlineKeyboardMarkup() # кнопки
    site_button = types.InlineKeyboardButton('Открыть общее расписание', url='https://clck.ru/3QZjCY') # расписание
    markup.row(site_button)
    student_role = types.InlineKeyboardButton('Ученик или родитель', callback_data='student') # выбор ученика
    teacher_role = types.InlineKeyboardButton('Учитель', callback_data='teacher') # выбор учителя
    markup.row(student_role, teacher_role)
    bot.send_message(
        message.chat.id,
        'Приветствую!\nВы можете увидеть общее расписание уроков, либо посмотреть специализированный вариант специально для Вас - для этого выберите роль - <b>школьник(родитель школьника)</b> или <b>учитель</b>.',
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    if call.data == 'student': # если выбран ученик
        bot.send_message(call.message.chat.id, 'привет, школьник')
    elif call.data == 'teacher': # если выбран учитель
        bot.send_message(call.message.chat.id, 'привет, учитель')

bot.polling(none_stop=True)