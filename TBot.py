import os
from click import command
import telebot

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['greet'])
def greet(message):
    bot.reply_to(message, "Hey there!")

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "hello")

# Custom function to fetch a video link with video id
# @bot.message_handler(func=fetch_ytlink)
# def send_link(message):
#     pass

bot.infinity_polling()