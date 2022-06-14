import os
from urllib import response
from matplotlib import ticker
import telegram
import pandas_datareader as web

from turtle import update
from urllib.request import Request
from dotenv import load_dotenv
from sqlalchemy import true
from telegram import Bot,Update
from telegram.ext import Updater,CommandHandler
from telegram.utils.request import Request
from zmq import CONNECT_TIMEOUT
from datetime import datetime

# accessing the bot api token from the .env file
load_dotenv()
pwd=os.getenv("API_KEY")

def start(update,context):
    update.message.reply_text("Hello World!")

def Help(update,context):
    update.message.reply_text("""
    The following commands are available:

    /start - Start the bot
    /help - Get this help message
    /gettime - Get the current date and time
    /contact - Get the contact details of the bot
    /videos - Fetch recent videos from YT and FB
    /stock - Get the current price of a stock from Yahoo Finance
    
    TO DO:
    /get_timezone - Send your current location to the bot
    /settings - Get the settings of the bot
    /calc - Get the calculator of the bot
    """)

def get_time(update,context):
    now=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    update.message.reply_text(f"Current Time is : {dt_string}")

def contact(update,context):
    update.message.reply_text("""
    Contact Details:
    Name: Raihan Munim
    Email: raihan.srizon@gmail.com
    """)

def videos(update,context):
    update.message.reply_text("""
    `Videos: They will be fetched soon`
    """)

def stock(update, context):
    ticker = context.args[0]
    data = web.DataReader(ticker, 'yahoo')
    price = data.iloc[-1]['Close']
    update.message.reply_text(f"The current price of {ticker} is {price:.2f}$!")

def get_timezone(update,context):
    update.message.reply_text("""
    This is getting implemented as we speak!
    """)

def settings(update,context):
    update.message.reply_text("""
    This is getting implemented as we speak!
    """)

def calc(update,context):
    update.message.reply_text("""
    This is getting implemented as we speak!
    """)

def handle_message(update,context):
    update.message.reply_text(f"You said {update.message.text}")

def main():
    req=Request(connect_timeout=0.5)
    my_bot=Bot(token=pwd,request=req)
    updater=Updater(bot=my_bot,use_context=True)
    dp=updater.dispatcher

    # Display help in menu
    cmd=[("help","Get this help message")]
    my_bot.set_my_commands(cmd)
    

    dp.add_handler(telegram.ext.CommandHandler("start", start))
    dp.add_handler(telegram.ext.CommandHandler("gettime", get_time))
    dp.add_handler(telegram.ext.CommandHandler("contact", contact))
    dp.add_handler(telegram.ext.CommandHandler("videos", videos))
    dp.add_handler(telegram.ext.CommandHandler("stock", stock))
    dp.add_handler(telegram.ext.CommandHandler("help", Help))

    # fetaures to be added soon
    dp.add_handler(telegram.ext.CommandHandler("settings", settings))
    dp.add_handler(telegram.ext.CommandHandler("calc", calc))
    dp.add_handler(telegram.ext.CommandHandler("get_timezone", get_timezone))

    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()