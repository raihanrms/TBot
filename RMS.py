# Importing all the packages from a separate file
from io import BytesIO
from Packages import *

# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# prints bot is running with start time
print("Bot is running...")
timezonelist = ['Asia/Dhaka']
for zone in timezonelist:
    now = datetime.now(timezone(zone))
print(now.strftime('%Y/%m/%d %I:%M:%S'))

# accessing the bot api token from the .env file
load_dotenv()
pwd=os.getenv("TELEGRAM_API_KEY")
YKey=os.getenv("YOUTUBE_API_KEY")
channel_id = "UCjXfkj5iapKHJrhYfAF9ZGg"

# states as integers
WELCOME = 0
QUESTION = 1
CANCEL = 2
CORRECT = 3

result_storage_path = 'tmp' 

# The start function 
def start(update, context):
    update.message.reply_text("""
    The bot is still in development, while you wait
    you can check out the following features that has
    been implemented:
    /start - Display this start message
    /settings - Bilingual support (EN/BN)
    /add2verify - Add two numbers
    /random - Send emoji (3 options)
    /conloc - Send contact and location information
    
    TO DO:
    /channel - Find YT channel with search ID
    /comments - Fetch YT comments from last 10 YT videos
    /translate - Add real-time translation to your messages
    """)

# Bilingual suppot
def settings(update: Update, context: CallbackContext) -> None:
    EnKey = telegram.KeyboardButton(text='English (EN)')
    BnKey = telegram.KeyboardButton(text='বাংলা (BN)')
    LanKey = [[EnKey, BnKey]]
    reply_markup = telegram.ReplyKeyboardMarkup(LanKey, resize_keyboard=True, one_time_keyboard=true)

    update.message.reply_text(
        f'Hello {update.effective_user.first_name}! Which language do you prefer? English (EN) or বাংলা (BN)?',
        reply_markup=reply_markup)


# The Add2Verify function
def Add2Verify(update_obj, context):
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

# get youtube id from youtube url
def getYTID(update, videoURL):
    update.message.reply_text("Please enter the youtube url")
    videoID = str(videoURL).split('/')
    videoID = videoID[-1]
    return videoID


# Ask location and contact info
def conloc(update: Update, context: CallbackContext) -> None:
    EnKey = telegram.KeyboardButton(text='Send location', request_location=True)
    BnKey = telegram.KeyboardButton(text='Send contact', request_contact=True)
    LanKey = [[EnKey, BnKey]]
    reply_markup = telegram.ReplyKeyboardMarkup(LanKey, resize_keyboard=True, one_time_keyboard=true)

    update.message.reply_text(
        f'Hello {update.effective_user.first_name}, would you share these information?',
        reply_markup=reply_markup)

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


# fetching youtube channel stats
def channelStats(youtube, channel_id):
    request = youtube.channels().list(
                part="snippit,contentDetails,statistics",
                id=channel_id)

    response = request.execute()

    channelData = dict(ChannelName = response['items'][0]['snippet']['title'],
                       Subscribers = response['items'][0]['statistics']['subscriberCount'],
                       Views = response['items'][0]['statistics']['viewCount'],
                       TotalVideos = response['items'][0]['statistics']['videoCount'])
    
    return channelData

# find regex matches in the text
# def findRegex(text, regex):

def channelData(object_id, update, context):
    youtube = build('youtube', 'v3', YKey)
    channel_id = object_id
    channelData = channelStats(youtube, channel_id)
    update.message.reply_text(f"Channel Name: {channelData['ChannelName']}\nSubscribers: {channelData['Subscribers']}\nViews: {channelData['Views']}\nTotal Videos: {channelData['TotalVideos']}")

# get location from image
def getLoc(update, context):
    update.message.reply_text("Please send me a photo")
    context.user_data['photo'] = True

# handle image sent to bot
# def handle_photo(update, context):
#     file = context.bot.get_file(update.message.photo[-1].file_id)
#     f = BytesIO(file.download_as_bytearray())
#     file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)

#     img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     cv2.imwrite('test1.jpg', img)
#     update.message.reply_text("Image received")

#     # get the location from the image
#     array = np.arange(0, 60000, 1, dtype=np.uint8)
#     image = PIL.Image.fromarray(array)
#     image.save('test1.jpg')

#     update.message.reply_text("Photo saved as test1.jpg")
 
def get_image_id_from_message(Update, context):
  # there are multiple array of images, check the biggest
  return Update.photo[len(Update.photo)-1].file_id


def save_image_from_message(update, context):
    cid = Update.chat.id
    image_id = get_image_id_from_message(Update)

    update.send_message(cid, '🔥 Saving image, be patient ! 🔥')

    # prepare image for downlading
    file_path = update.get_file(image_id).file_path
    
    # generate image download url
    image_url = "https://api.telegram.org/file/bot{0}/{1}".format(pwd['TELEGRAM_API_KEY'], file_path)
    print(image_url)

    # create folder to store pic temporary, if it doesnt exist
    if not os.path.exists(result_storage_path):
        os.makedirs(result_storage_path)

    # retrieve and save image
    image_name = "{0}.jpg".format(image_id)
    urllib.request.urlretrieve(image_url, "{0}/{1}".format(result_storage_path,image_name))

    # pimage = PIL.Image.open('test1.jpg')

    # from get_location import get_location
    # get_location()
    # exif = {
    #     PIL.ExifTags.TAGS[k]: v
    #     for k, v in pimage._getexif().items()
    #     if k in PIL.ExifTags.TAGS
    # }

    # if 'GPSInfo' in exif:
    #     north = exif['GPSInfo'][2]
    #     east = exif['GPSInfo'][4]
    #     lat = north[0][0] + (north[1][0] / 60) + (north[2][0] / 3600)
    #     lon = east[0][0] + (east[1][0] / 60) + (east[2][0] / 3600)
    #     lat, lon = float(lat), float(lon)
    #     update.message.reply_text(f"Latitude: {lat}\nLongitude: {lon}")

    # else:
    #     update.message.reply_text("No location found")


def main():
    req=Request(connect_timeout=1.0)
    # updater object with api key
updater = telegram.ext.Updater(pwd, use_context=true, persistence=PicklePersistence(filename='bot_data'))
    # get dispatcher to add handlers
dispatcher = updater.dispatcher


# a regular expression that matches yes or no
yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)
# Create our ConversationHandler, with only one state
handler1 = telegram.ext.ConversationHandler(
      entry_points=[telegram.ext.CommandHandler('Add2Verify', Add2Verify)],
      states={
            WELCOME: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), welcome)],
            QUESTION: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), question)],
            CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), cancel)],
            CORRECT: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), correct)],
      },
      fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
      )

# a regular expression to extract the youtube channel id
# YTregex = r'(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/watch\?.+&v=))([\w\-]{10,12})([\&\?\#].*)?$'

# handler2 = telegram.ext.ConversationHandler(
#     detectLink = [telegram.ext.CommandHandler('getYTID', getYTID)],
#     states={
#         getYTID: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(YTregex), channelData)],}     
# )

# add the handler to the dispatcher
dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('settings', settings))
dispatcher.add_handler(handler1)
# dispatcher.add_handler(handler2)
dispatcher.add_handler(telegram.ext.CommandHandler('random', random))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(telegram.ext.CommandHandler('getYTID', getYTID))
updater.dispatcher.add_handler(CommandHandler('conloc', conloc))
updater.dispatcher.add_handler(CommandHandler('channel', channelData))
# updater.dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, get_image_id_from_message))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, save_image_from_message))


dispatcher.add_handler(telegram.ext.CommandHandler('repeater', repeater))

# start polling for updates from Telegram
updater.start_polling()
# block until a signal (like one sent by CTRL+C) is sent
updater.idle()

if __name__=="__main__":
    main()
    sys.exit(0)

# working on it