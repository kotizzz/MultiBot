import telebot
from telebot import types
from googletrans import Translator
import requests
import json
import random
import os

bot = telebot.TeleBot('6292349988:AAFffqisg-CSkZyTCHHLVzb1STOT8kE6pjc')
API_weather = '3d9de74844d28377e81415151cbe6a66'

states = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📖Переводчик')
    item2 = types.KeyboardButton('📝Калькулятор')
    item3 = types.KeyboardButton('🌤Погода')
    item4 = types.KeyboardButton('🤡Мем дня')

    markup.row(item1, item2)
    markup.row(item3, item4)

    bot.send_message(message.chat.id, 'Выберите функцию, которую вы хотите использовать', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    start(message)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == '📖Переводчик':
        show_language_selection(message)
    elif message.text == '🏠Главное меню':
        start(message)
    elif message.text == '🌤Погода':
        bot.send_message(message.chat.id, 'Вы выбрали функцию прогноза погоды. Впишите свой город:')
        states[message.chat.id] = 'weather_city'
    elif message.text == '📝Калькулятор':
        calculator_handler(message)
    elif message.text == '🤡Мем дня':
        send_daily_meme(message)
    elif states.get(message.chat.id) == 'weather_city':
        get_weather(message)

def show_language_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🇬🇧Английский')
    item2 = types.KeyboardButton('🇷🇺Русский')
    item3 = types.KeyboardButton('🇫🇷Французский')
    item4 = types.KeyboardButton('🇩🇪Немецкий')
    item5 = types.KeyboardButton('🇪🇸Испанский')
    item6 = types.KeyboardButton('🏠Главное меню')

    markup.row(item1, item2)
    markup.row(item3, item4, item5)
    markup.row(item6)

    bot.send_message(message.chat.id, 'Выберите язык перевода', reply_markup=markup)
    states[message.chat.id] = 'select_language'
    bot.register_next_step_handler(message, language_selection_handler)

def language_selection_handler(message):
    if message.chat.id in states and states[message.chat.id] == 'select_language':
        if message.text == '🏠Главное меню':
            start(message)
            return

        dest = get_language_code(message.text)
        if dest:
            states[message.chat.id] = dest
            bot.send_message(message.chat.id, 'Введите текст для перевода')
            bot.register_next_step_handler(message, translation_handler)
        else:
            bot.send_message(message.chat.id, 'Неверный выбор языка')

def translation_handler(message):
    if message.chat.id in states and states[message.chat.id] in ['en', 'ru', 'fr', 'de', 'es']:
        if message.text == '📖Переводчик':
            bot.send_message(message.chat.id, 'Введите текст для перевода')
            return
        elif message.text in ['🇬🇧Английский', '🇷🇺Русский', '🇫🇷Французский', '🇩🇪Немецкий', '🇪🇸Испанский']:
            states[message.chat.id] = get_language_code(message.text)
            bot.send_message(message.chat.id, 'Введите текст для перевода')
            return

        translator = Translator()
        dest = states[message.chat.id]
        translated_text = translator.translate(message.text, dest=dest).text
        bot.send_message(message.chat.id, translated_text)
    else:
        bot.send_message(message.chat.id, 'Неверный выбор языка')

def get_language_code(language):
    language_codes = {
        '🇬🇧Английский': 'en',
        '🇷🇺Русский': 'ru',
        '🇫🇷Французский': 'fr',
        '🇩🇪Немецкий': 'de',
        '🇪🇸Испанский': 'es'
    }
    return language_codes.get(language)

def get_weather(message):
    if message.content_type == 'text':
        city = message.text.strip().lower()
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_weather}&units=metric')
        if res.status_code == 200:
            data = json.loads(res.text)
            temp = data["main"]["temp"]
            bot.send_message(message.chat.id, f'Сейчас погода: {temp}')
        else:
            bot.send_message(message.chat.id, 'Город указан неверно')

def calculator_handler(message):
    bot.send_message(message.chat.id, 'Введите выражение для расчета:')
    states[message.chat.id] = 'calculator'
    bot.register_next_step_handler(message, calculate_expression)

def calculate_expression(message):
    if message.chat.id in states and states[message.chat.id] == 'calculator':
        if message.text == '📝Калькулятор':
            bot.send_message(message.chat.id, 'Введите выражение для расчета:')
            return
        elif message.text == '🏠Главное меню':
            start(message)
            return

        try:
            result = eval(message.text)
            bot.send_message(message.chat.id, f'Результат: {result}')
        except Exception:
            bot.send_message(message.chat.id, 'Неверное выражение')
    else:
        bot.send_message(message.chat.id, 'Неверный выбор')

def send_daily_meme(message):
    meme_folder = 'C:/Users/krz20/OneDrive/Документы/GitHub/MultiBot/meme'  # Укажите путь к папке с мемами

    meme_files = os.listdir(meme_folder)
    if meme_files:
        random_meme = random.choice(meme_files)
        meme_path = os.path.join(meme_folder, random_meme)
        with open(meme_path, 'rb') as file:
            bot.send_photo(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, 'Папка с мемами пуста')

bot.polling(none_stop=True)