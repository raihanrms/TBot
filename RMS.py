# Importing all the packages from a separate file
from Packages import *

# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# accessing the bot api token from the .env file
load_dotenv()
pwd=os.getenv("API_KEY")

# states as integers
WELCOME = 0
QUESTION = 1
CANCEL = 2
CORRECT = 3
HELP = 4


# The entry function
def start(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    update_obj.message.reply_text("Hello there, do you want to answer a question? (Yes/No)",
        reply_markup=telegram.ReplyKeyboardMarkup([['Yes', 'No']], resize_keyboard=True, one_time_keyboard=True)
    )
    # go to the WELCOME state
    return WELCOME

# helper function, generates new numbers and sends the question
def randomize_numbers(update_obj, context):
    # store the numbers in the context
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(0,10000), randint(0, 10000)
    # send the question
    update_obj.message.reply_text(f"Calculate {context.user_data['rand_x']}+{context.user_data['rand_y']}")

# in the WELCOME state, check if the user wants to answer a question
def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        # send question, and go to the QUESTION state
        randomize_numbers(update_obj, context)
        return QUESTION
    else:
        # go to the CANCEL state
        return CANCEL

# in the QUESTION state
def question(update_obj, context):
    # expected solution
    solution = int(context.user_data['rand_x']) + int(context.user_data['rand_y'])
    # check if the solution was correct
    if solution == int(update_obj.message.text):
        # correct answer, ask the user if he found tutorial helpful, and go to the CORRECT state
        update_obj.message.reply_text("Correct answer!")
        update_obj.message.reply_text("Was this tutorial helpful to you?")
        return CORRECT
    else:
        # wrong answer, reply, send a new question, and loop on the QUESTION state
        update_obj.message.reply_text("Wrong answer! 😞")
        # send another random numbers calculation
        randomize_numbers(update_obj, context)
        return QUESTION

# in the CORRECT state
def correct(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        update_obj.message.reply_text("Glad it was useful! 😀")
    else:
        update_obj.message.reply_text("You must be a programming wizard already!")
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(f"See you {first_name}!, bye")
    return telegram.ext.ConversationHandler.END

def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}!", reply_markup=telegram.ReplyKeyboardRemove()
    )
    return telegram.ext.ConversationHandler.END

def help(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text("""
    Hi {first_name}! The following commands are available:
    /start - start the bot
    /help - show this help
    /get_time - get the current time
    """)

    helpInlineKeyboard = [
        [   
            InlineKeyboardButton("Start", callback_data="start"),
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("Get Time", callback_data="get_time"),
        ]]
    reply_markup = InlineKeyboardMarkup(helpInlineKeyboard)
    update.message.reply_text("List of Commands:", reply_markup=reply_markup)
    return HELP


def main():
    req=Request(connect_timeout=1.0)
    # updater object with api key
updater = telegram.ext.Updater(pwd)
    # get dispatcher to add handlers
dispatcher = updater.dispatcher

# a regular expression that matches yes or no
yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)
# Create our ConversationHandler, with only one state
handler1 = telegram.ext.ConversationHandler(
      entry_points=[telegram.ext.CommandHandler('start', start)],
      states={
            WELCOME: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), welcome)],
            QUESTION: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), question)],
            CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), cancel)],
            CORRECT: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), correct)],
      },
      fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
      )

handler2 = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.CommandHandler('help', help)],
        states={
                HELP: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), help)],
        },
        fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
        )

# add the handler to the dispatcher
dispatcher.add_handler(handler1)
dispatcher.add_handler(handler2)
# start polling for updates from Telegram
updater.start_polling()
# block until a signal (like one sent by CTRL+C) is sent
updater.idle()

if __name__=="__main__":
    main()
    sys.exit(0)
