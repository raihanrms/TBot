# Importing all the packages from a separate file
from cgitb import handler
from Packages import *
from tkinter.messagebox import CANCEL, QUESTION
from random import randint

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

# # helper function to get the current time
# def get_time():
#     # get the current time
#     time = datetime.datetime.now()
#     # return the time in a string
#     return time.strftime("%H:%M:%S")

# helper function, generates new numbers and sends the question
def randomize_numbers(update_obj, context):
    # store the numbers in the context
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(0,1000), randint(0, 1000)
    # send the question
    update_obj.message.reply_text(f"Calculate {context.user_data['rand_x']}+{context.user_data['rand_y']}")

# welcome state to check if the user wants to be a part of the test
def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'no']:
        # send the curent time
        update_obj.message.reply_text(update_obj, context)
        # return to question state
        return QUESTION
    else:
        # go to cancel state
        return CANCEL

# question state
def question(update_obj, context):
    # expected answer
    solution = context.user_data['rand_x'] + context.user_data['rand_y']
    # check if the answer is correct
    if solution == int(update_obj.message.text):
        # Okay the answer is correct but would you like the test?
        update_obj.message.reply_text("Correct answer!")
        update_obj.message.reply_text("Then the test is working!")
        return CORRECT
    else:
        # the answer is wrong, send another question and loop on the question state
        update_obj.message.reply_text("Wrong answer:  u'\U0001F61E'")
        
        # send another random numbers calculation
        randomize_numbers(update_obj, context)
        return QUESTION

# correct state
def correct(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
       update_obj.message.reply_text("Okay, the test is working!")
    else:
        update_obj.message.reply_text("Okay, Go debug the code!")

    # get user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(f"See you {first_name}!, bye")
    return telegram.ext.ConversationHandler.END

# cancel state
def cancel(update_obj, context):
    # get user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"See you later, {first_name}!", reply_keyboard=ReplyKeyboardRemove()
    )
    return telegram.ext.ConversationHandler.END

# regular expression that matches yes or no
yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)

# conversation handler
handler = telegram.ext.ConversationHandler(
    entry_points=[telegram.ext.CommandHandler('start', start)],
    states={
        WELCOME: [telegram.ext.MessageHandler(Filters.text, welcome)],
        QUESTION: [telegram.ext.MessageHandler(Filters.text, question)],
        CANCEL: [telegram.ext.MessageHandler(Filters.text, cancel)],
        CORRECT: [telegram.ext.MessageHandler(Filters.text, correct)]
    },
    fallbacks=[telegram.ext.CommandHandler('cancel', cancel)]
)

# add the handler to the dispatcher
dispatcher.add_handler(handler)

# start polling for updates from telegram
updater.start_polling()

# block until the user presses Ctrl+C
updater.idle()