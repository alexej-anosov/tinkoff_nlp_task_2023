import telebot
from telebot import types
import requests
from config import API_URL
from utils import *

bot = telebot.TeleBot('6422363145:AAGa-fvbt21c_-CdH3OeL4Rrbv57YZmn5jU')
chat_history = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, f"Давай пообщаемся.")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    url = f'{API_URL}/tinkoffbot_api'

    user_id = message.from_user.id
    if user_id not in chat_history:
        chat_history[user_id] = []
    chat_history[user_id].append(message.text)
    chat_history[user_id] = cut_chat_history(chat_history[user_id])

    formatted_request = request_formatter(chat_history[user_id])
    response = requests.post(url, json={'input_text': formatted_request})
    response_data = response.json()
    formatted_response = response_formatter(message.text, response_data['output'])
    chat_history[user_id].append(formatted_response)
    bot.send_message(message.from_user.id, formatted_response)


bot.polling(none_stop=True, interval=0)