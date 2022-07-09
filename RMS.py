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

# cancel state
def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}!", reply_markup=telegram.ReplyKeyboardRemove()
    )
    return telegram.ext.ConversationHandler.END

# checks for new updates
def repeater(update, context):
    if context.user_data[repeater] == True:
        update.message.reply_text("You are already subscribed to the repeater")

# generates buttons with emoji to display a little sticker
def random(update: Update, context: CallbackContext) -> None:
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Basketball", callback_data='🏀')],
        [
            InlineKeyboardButton("Dice", callback_data='🎲'),
            InlineKeyboardButton("Darts", callback_data='🎯'),
        ]
    ])
    update.message.reply_text(
        f'Hello {update.effective_user.first_name}, please choose an option:',
        reply_markup=reply_buttons
    )

# calling the button fuction for the random sticker fuction
def button(update: Update, context: CallbackContext) -> None:
    # Must call answer!
    update.callback_query.answer()
    # Remove buttons
    update.callback_query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup([])
    )
    update.callback_query.message.reply_dice(emoji=update.callback_query.data)

# checks and stores personal information in data file for future refercence
def personal(update: Update, context: CallbackContext) -> int:
    reply_list = [f'Hello {update.effective_user.first_name}']
    if context.user_data:
        reply_list.append('I know these things about you')
        reply_list.extend([f'Your {key} {value_pair[0]} {value_pair[1]}' for (key, value_pair) in context.user_data.items()])
    else:
        reply_list.append('I don\'t know anything about you.')
    reply_list.extend([
        'Please tell me about yourself.',
        'Use the format: My X is/have/are Y'
    ])
    update.message.reply_text('\n'.join(reply_list))

# Ask location and contact info
def ContactLocation(update: Update, context: CallbackContext) -> None:
    location_keyboard = telegram.KeyboardButton(text='Send location', request_location=True)
    contact_keyboard = telegram.KeyboardButton(text='Send contact', request_contact=True)
    CL = [[location_keyboard, contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(CL)

    update.message.reply_text(
        f'Hello {update.effective_user.first_name}, would you share these information',
        reply_markup=reply_markup)
    
# accepts only these parameters from the user
INFO_REGEX = r'^My (.+) (is|have|are) (.+)$'
def receive_info(update: Update, context: CallbackContext) -> int:
    # Extract the three capture groups
    info = re.match(INFO_REGEX, update.message.text).groups()
    # Using the first capture group as key, the second and third capture group are saved as a pair to the context.user_data
    context.user_data[info[0]] = (info[1], info[2])

    # Quote the information in the reply
    update.message.reply_text(
        f'So your {info[0]} {info[1]} {info[2]}, how interesting'
    )

def main():
    req=Request(connect_timeout=1.0)
    # updater object with api key
updater = telegram.ext.Updater(pwd, persistence=PicklePersistence(filename='bot_data'))
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


# add the handler to the dispatcher
dispatcher.add_handler(handler1)
dispatcher.add_handler(telegram.ext.CommandHandler('random', random))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('personal', personal))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(INFO_REGEX), receive_info))
updater.dispatcher.add_handler(CommandHandler('ContactLocation', ContactLocation))

dispatcher.add_handler(telegram.ext.CommandHandler('repeater', repeater))


# start polling for updates from Telegram
updater.start_polling()
# block until a signal (like one sent by CTRL+C) is sent
updater.idle()

if __name__=="__main__":
    main()
    sys.exit(0)
