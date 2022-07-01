# Importing all the packages from a separate file
from Packages import *
# accessing the bot api token from the .env file
load_dotenv()
pwd=os.getenv("API_KEY")

# Global Variables
LANG = "EN"
SET_LANG = range(8)

def start(update: Update, context: CallbackContext):
    """Start function. Displayed whenever the /start command is called.
       This function sets the language of the bot."""
    update.message.reply_text(f"""
    Hey, I'm RMS-Bot! \nআমি আরএমএস-বট!\n
    """)

    # Create the buttons for language selection
    # keyboard1 = [
    #     [
    #         InlineKeyboardButton("বাংলা", callback_data="1"),
    #         InlineKeyboardButton("English", callback_data="2")
    #     ]]

    # kbd1 = InlineKeyboardMarkup(keyboard1)
    # update.message.reply_text(f"""Please select your language:
    # \n অনুগ্রহ করে ভাষা নির্বাচন করুন। """, reply_markup=kbd1)
    

# Read: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/inlinekeyboard2.py
#       https://github.com/lzzy12/python-aria-mirror-bot/blob/main/bot/__main__.py
#       https://github.com/nimiology/spotify_downloader_telegram__bot
#       

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
    # /getLoc - Recieve location
    # /settings - Custom Settings
    # /calc - Calculate some stuff
    # /translate - Bangla to English
    # /notf - Read notifications.
    # """)

    keyboard2 = [
        [   
            InlineKeyboardButton("Start", callback_data="start"),
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("Get Time", callback_data="get_time"),
        ]]

    reply_markup = InlineKeyboardMarkup(keyboard2)
    update.message.reply_text("List of Commands:", reply_markup=reply_markup)
    pass

def get_time(update,context):
    now=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    update.message.reply_text(f"Current Time is : {dt_string}")

# def contact(update,context):
#     update.message.reply_text("""
#     Contact Details:
#     Name: N/A
#     Email: N/A
#     """)

# def videos(update,context):
#     update.message.reply_text("""
#     Videos: They will be fetched soon!
#     """)

# def stock(update, context):
#     ticker = context.args[0]
#     data = web.DataReader(ticker, 'yahoo')
#     price = data.iloc[-1]['Close']
#     update.message.reply_text(f"The current price of {ticker} is {price:.2f}$!")

# def getLoc(update: Update, context: CallbackContext):
#     current_postion = (update.message.location.latitude, update.message.location.longitude)
#     update.message.reply_text(current_postion)
    
# def settings(update,context):
#     update.message.reply_text("""
#     This is getting implemented as we speak!
#     """)

# def calc(update,context):
#     update.message.reply_text("""
#     This is getting implemented as we speak!
#     """)

# def translate(update,context):
#     update.message.reply_text("""
#     This will be difficult to implement!
#     """)

# def notf(update,context):
#     update.message.reply_text("""
#     This is read the notifications from phone!
#     """)



def handle_commands(update,context):
    """Handle all Commands."""
    query: CallbackQuery = update.callback_query
    query.answer()
    query.edit_message_text(text=f"You selected: {query.command}")

# def message_handler(update,context):
#     if update.message.text == "/start":
#         start(update,context)
#     elif update.message.text == "/help":
#         Help(update,context)
#     elif update.message.text == "/gettime":
#         get_time(update,context)

# def error(update: Update, context: CallbackContext):
#     """Log Errors caused by Updates."""
#     sys.stderr.write("ERROR: '%s' caused by '%s'" % context.error, update)
#     pass

def gui():
    layout = [[sg.Text('Bot Status: '), sg.Text('Stopped', key='status')],
              [sg.Button('Start'), sg.Button('Stop'), sg.Exit()]]

    window = sg.Window('Finxter Bot Tutorial', layout)

    while True:
        event, _ = window.read()
            
        if event == 'Start':
            if update is None:
                start()
            else:
                update.start_polling()
            window.FindElement('status').Update('Running')
        if event == 'Stop':
            update.stop()
            window.FindElement('status').Update('Stopped')

        if event in (None, 'Exit'):
            break

    if update is not None and update.running:
        update.stop()
    window.close()

def main():
    req=Request(connect_timeout=1.0)
    my_bot=Bot(token=pwd,request=req)
    updater=Updater(bot=my_bot,use_context=True)
    dp=updater.dispatcher

    # Display help in menu
    cmd=[("help","Get this help message")]
    my_bot.set_my_commands(cmd)
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(telegram.ext.CommandHandler("help", Help))
    dp.add_handler(telegram.ext.CommandHandler("gettime", get_time))
    # dp.add_handler(telegram.ext.CommandHandler("contact", contact))
    # dp.add_handler(telegram.ext.CommandHandler("videos", videos))
    # dp.add_handler(telegram.ext.CommandHandler("stock", stock))
    

    # fetaures to be added soon
    # dp.add_handler(telegram.ext.CommandHandler("settings", settings))
    # dp.add_handler(telegram.ext.CommandHandler("calc", calc))
    # dp.add_handler(telegram.ext.CommandHandler(Filter.location, Location))
    # dp.add_handler(telegram.ext.CommandHandler("getLoc", getLoc))
    # dp.add_handler(telegram.ext.CommandHandler("translate", translate))
    # dp.add_handler(telegram.ext.CommandHandler("notf", notf))
    
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_commands))
    dp.add_handler(telegram.ext.CallbackQueryHandler(handle_commands))
    #dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()