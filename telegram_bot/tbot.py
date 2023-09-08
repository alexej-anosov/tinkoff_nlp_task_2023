import telebot
from telebot import types
import requests
from config import API_URL

bot = telebot.TeleBot('6422363145:AAGa-fvbt21c_-CdH3OeL4Rrbv57YZmn5jU')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник! Давай пообщаемся.", reply_markup=markup)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    url = f'{API_URL}/tinkoffbot_api'
    response = requests.post(url, json={'input_text': message.text})
    response_data = response.json()
    print(response_data)
    bot.send_message(message.from_user.id, response_data['output'])


bot.polling(none_stop=True, interval=0)