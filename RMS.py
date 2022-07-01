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

# helper function to get the current time
def get_time():
    # get the current time
    time = datetime.datetime.now()
    # return the time in a string
    return time.strftime("%H:%M:%S")

# welcome state to check if the user wants to be a part of the test
def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'no']:
        # send the curent time
        update_obj.message.reply_text(get_time())
        # return to question state
        return QUESTION
    else:
        # go to cancel state
        return CANCEL