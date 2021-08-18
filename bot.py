# bot.py
import telegram as tg
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import MessageEntity
import re
import requests
import os
import pyshorteners
import bitlyshortener

tokens_pool = ['4fae9902744ef33f75a12df129858928f6c9b663']  # Use your own.
shortener = bitlyshortener.Shortener(tokens=tokens_pool)

print('Bot is going to start...')
def __init__(self):
        super().__init__(
            plugins={
                "root": "plugins/__init__.py"
            }
        )
        self.LOGGER = LOGGER

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
#Read env variables
TOKEN = os.environ['TOKEN']
baseURL = os.environ['baseURL']
affiliate_tag = os.environ['affiliate_tag']
HEROKU_URL = os.environ['HEROKU_URL']

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    username = update.message.chat.username
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello @" +username+ " , Welcome to @steallootdeal affiliate converter bot\n\n Its just a basic bot that will help in your daily affiliate work")

# Create the new URL with the refer tag
def newReferURL(pcode, update):
    msg = update.message.text
    thestring = msg
    URLless_string = re.sub(r'^https?:\/\/.*[\r\n]*', '', thestring, flags=re.MULTILINE)
    return "https://"+baseURL+pcode+"?tag="+affiliate_tag


#Expand shorted URL (amzn.to links) to normal Amazon URL
def unshortURL(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head("https://"+url, allow_redirects=True)
    return resp.url

#Filter the msg text to extract the URL if found. Then send the corresponding reply
# with the new affiliate URL
def filterText(update, context):
    pCode=""
    msg = update.message.text
    start = msg.find("amzn.to")
    if start!=-1:
        msg = unshortURL(msg[start:].split()[0])
    start = msg.find(baseURL)
    if start != -1:
        #Regular expression to extract the product code. Adjust if different URL schemes are found.
        m = re.search(r'(?:dp\/[\w]*)|(?:gp\/product\/[\w]*)',msg[start:].split(" ")[0])
        if m != None:
            pCode = m.group(0)
        context.bot.send_message(chat_id=update.message.chat_id,reply_to_message_id=update.message.message_id, text=newReferURL(pcode, update))

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(    
                   Filters.text & (Filters.entity(MessageEntity.URL) |
                                    Filters.entity(MessageEntity.TEXT_LINK)),filterText))
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(HEROKU_URL + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
