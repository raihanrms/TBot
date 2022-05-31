from email import message
import telebot
import os
import parse

from click import command
from urllib.parse import urlparse

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

PARSE_MODE = "MarkdownV2"
AVAILABLE_COMMANDS = ["/start", "/help", "/test"]

STARTER = """
Hi\! I am RmsBot\, a bot built by [raihanrms](https://github.com/raihanrms)
`This is a work in progress bot, that can save time for \open-source researchers and volenteers`"""



@bot.message_handler(commands=["start"])
def greet(message):
    bot.send_message(message.chat.id, STARTER, parse_mode=PARSE_MODE)

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "hello")

@bot.message_handler(commands=["test"])
def test(message):
    bot.send_message(message.chat.id, "*I'm up\!*", parse_mode=PARSE_MODE)

@bot.message_handler(commands=['help'])
def greet(message):
    bot.reply_to(message, "Hey there!")

# @bot.message_handler(commands=['name'])
# def ask_name(**kwargs):
#     bot.send_message(message.chat.id, ['user_id'],
#                          text='Tell me your name, please :D')
#     bot.state_manager.set_state(kwargs['user_id'], 'telling_name')

bot.infinity_polling()