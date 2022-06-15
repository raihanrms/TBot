from email import message
import logging
from lang_dict import *
from geo_app import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler
from telegram.ext import ConversationHandler, CallbackQueryHandler, Filters

# for token
from credentials import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# global variables
LANG = "EN"
SET_LANG, MENU, SET_STAT, REPORT, MAP, FAQ, ABOUT, LOCATION = range(8)
STATE = SET_LANG

def start(update, context):
    """Start function. Displayed whenever the /start command is called.
    This function sets the language of the bot."""
    
    # Create the buttons for language selection
    keyboard = [['BN', 'EN']]

    # Create initial message
    message = "Hey, I'm RMS-Bot! / আসসালামু আলাইকুম, আমি আরএমএস-বট! \n\n Please select a language. / অনুগ্রহ করে ভাষা নির্বাচন করুন।"

    reply_markup = ReplyKeyboardMarkup(keyboard, 
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)
    return SET_LANG

def set_lang(bot, update):
    """
    First handler to receive the language globally.
    """
    # set the language
    global LANG
    LANG = update.message.text
    user = update.message.from_user

    logger.info("Language set by {} to {}.".format(user.first_name, LANG))
    update.message.reply_text(lang_selected[LANG],
                              reply_markup=ReplyKeyboardRemove())
    return MENU