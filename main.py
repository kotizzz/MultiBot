import telebot
from telebot import types

bot = telebot.TeleBot('6292349988:AAFffqisg-CSkZyTCHHLVzb1STOT8kE6pjc')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton('Переводчик', callback_data='translate')
    btn2 = types.InlineKeyboardButton('Калькулятор', callback_data='calculate')
    btn3 = types.InlineKeyboardButton('Погода', callback_data='weather')
    btn4 = types.InlineKeyboardButton('Мем дня', callback_data='meme')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    bot.send_message(message.chat.id, 'Выбери функцию, которой хочешь воспользоваться:', reply_markup=markup)

bot.polling(none_stop=True)