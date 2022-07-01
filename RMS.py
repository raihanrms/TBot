# Importing all the packages from a separate file
from tkinter.messagebox import CANCEL, QUESTION
from Packages import *

# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# accessing the bot api token from the .env file
load_dotenv()
pwd=os.getenv("API_KEY")

# updater object with api key
updater = telegram.ext.Updater(pwd)

# get dispatcher to add handlers
dispatcher = updater.dispatcher

# states as integers
WELCOME = 0
QUESTION = 1
CANCEL = 2
CORRECT = 3

# entry function
def start(update_obj, context):
    # ask questions and show suggested answer in buttons
    update_obj.message.reply_text("This is a test, be a part of it? (Yes/No)",
    reply_markup=ReplyKeyboardMarkup(['Yes', 'No'], one_time_keyboard=True))
    # return to welcome state
    return WELCOME

