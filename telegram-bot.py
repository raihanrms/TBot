# Importing all the packages from a separate file
import logging
from Packages import *

# accessing the bot api token from the .env file
load_dotenv()
pwd=os.getenv("API_KEY")

# Global Variables
LANG = "EN"
SET_LANG = range(8)

from Testing_buttons import *
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Hello! Im Raihan, I'm just testing the bot!", reply_markup=keyboard1)

@dp.callback_query_handler(text=["randomvalue_of10", "randomvalue_of100"])
async def random_value(call: types.CallbackQuery):
    if call.data == "randomvalue_of10":
        await call.message.answer(randint(1, 10))
    if call.data == "randomvalue_of100":
        await call.message.answer(randint(1, 100))
    await call.answer()

@dp.callback_query_handler(text=["3", "4", "5", "6", "7", "8"])
async def button(call: types.CallbackQuery):
    if call.data == "3":
        await start(call.message, call.context)
    if call.data == "4":
        await Help(call.message, call.context)

def start(update: Update, context: CallbackContext):
    """Start function. Displayed whenever the /start command is called.
       This function sets the language of the bot."""
    update.message.reply_text(f"""
    Hey, I'm RMS-Bot! \nআমি আরএমএস-বট!\n
    """)

    # Create the buttons for language selection
    keyboard1 = [
        [
            InlineKeyboardButton("বাংলা", callback_data="1"),
            InlineKeyboardButton("English", callback_data="2")
        ]]

    reply_markup = InlineKeyboardMarkup(keyboard1)
    update.message.reply_text(f"""Please select your language:
    \n অনুগ্রহ করে ভাষা নির্বাচন করুন। """, reply_markup=reply_markup)
    

# connect buttons with the fuctions
# def callback(update,context):
#     query = update.callback_query
#     if query.data == "1":
#         LANG = "BN"
#         query.edit_message_text(text="আপনার ভাষা নির্বাচন করা হয়েছে।")
#     elif query.data == "2":
#         LANG = "EN"
#         query.edit_message_text(text="Your language has been selected.")


def Help(update,context):
    #update.message.reply_text("""
    # The following commands are available:""")
    # /start - Start the bot
    # /help - Help menu
    # /gettime - Current date and time
    # /contact - Contact details of the bot
    # /videos - Fetch YT-FB videos
    # /stock - Stock from Yahoo Finance
    
    # TO DO:
    # /get_timezone - Recieve location
    # /settings - Custom Settings
    # /calc - Calculate some stuff
    # /translate - Bangla to English
    # /notf - Read notifications.
    # """)

    keyboard2 = [
    [   
        InlineKeyboardButton("Start", callback_data="3"),
        InlineKeyboardButton("Help", callback_data=str("4")),
        InlineKeyboardButton("Get Time", callback_data="5")
    ],[
        InlineKeyboardButton("Contact", callback_data="6"),
        InlineKeyboardButton("Videos", callback_data="7"),
        InlineKeyboardButton("Stock", callback_data="8")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard2)
    update.message.reply_text("List of Commands:", reply_markup=reply_markup)

def get_time(update,context):
    now=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    update.message.reply_text(f"Current Time is : {dt_string}")

def contact(update,context):
    update.message.reply_text("""
    Contact Details:
    Name: N/A
    Email: N/A
    """)

def videos(update,context):
    update.message.reply_text("""
    Videos: They will be fetched soon!
    """)

def stock(update, context):
    ticker = context.args[0]
    data = web.DataReader(ticker, 'yahoo')
    price = data.iloc[-1]['Close']
    update.message.reply_text(f"The current price of {ticker} is {price:.2f}$!")

def get_timezone(update: Update, context: CallbackContext):
    current_postion = (update.message.location.latitude, update.message.location.longitude)
    update.message.reply_text(current_postion)
    
def settings(update,context):
    update.message.reply_text("""
    This is getting implemented as we speak!
    """)

def calc(update,context):
    update.message.reply_text("""
    This is getting implemented as we speak!
    """)

def translate(update,context):
    update.message.reply_text("""
    This will be difficult to implement!
    """)

def notf(update,context):
    update.message.reply_text("""
    This is read the notifications from phone!
    """)

def handle_message(update,context):
    update.message.reply_text(f"You said {update.message.text}")

def main():
    req=Request(connect_timeout=1.0)
    my_bot=Bot(token=pwd,request=req)
    updater=Updater(bot=my_bot,use_context=True)
    dp=updater.dispatcher

    # Display help in menu
    cmd=[("help","Get this help message")]
    my_bot.set_my_commands(cmd)
    
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CallbackQueryHandler(inlinebutton))

    dp.add_handler(telegram.ext.CommandHandler("gettime", get_time))
    dp.add_handler(telegram.ext.CommandHandler("contact", contact))
    dp.add_handler(telegram.ext.CommandHandler("videos", videos))
    dp.add_handler(telegram.ext.CommandHandler("stock", stock))
    dp.add_handler(telegram.ext.CommandHandler("help", Help))

    # fetaures to be added soon
    dp.add_handler(telegram.ext.CommandHandler("settings", settings))
    dp.add_handler(telegram.ext.CommandHandler("calc", calc))
    # dp.add_handler(telegram.ext.CommandHandler(Filter.location, Location))
    dp.add_handler(telegram.ext.CommandHandler("get_timezone", get_timezone))
    dp.add_handler(telegram.ext.CommandHandler("translate", translate))
    dp.add_handler(telegram.ext.CommandHandler("notf", notf))
    
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()