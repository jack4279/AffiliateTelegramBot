# bot.py
import os
import re
import logging
import requests
import bitlyshortener
import telegram as tg

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import MessageEntity

tokens_pool = ['4fae9902744ef33f75a12df129858928f6c9b663']  # Use your own.
shortener = bitlyshortener.Shortener(tokens=tokens_pool)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Read env variables
TOKEN = os.environ['TOKEN']
baseURL = os.environ['baseURL']
affiliate_tag = os.environ['affiliate_tag']

def start(update, context):
    username = update.message.chat.username
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello @" +username+ " , Welcome to @steallootdeal affiliate converter bot\n\n Its just a basic bot that will help in your daily affiliate work")

def newReferURL(pcode, update):
    msg = update.message.text
    URLless_string = re.sub(r'^https?:\/\/.*[\r\n]*', '', msg, flags=re.MULTILINE)
    return URLless_string + "https://" + baseURL + pcode + "?tag=" + affiliate_tag

def unshortURL(url):
    session = requests.Session()
    resp = session.head("https://"+url, allow_redirects=True)
    return resp.url
        
def filterText(update, context):
    pCode = ""
    msg = update.message.text
    start = msg.find("amzn.to")
    if start != -1:
        msg = unshortURL(msg[start:].split()[0])
    start = msg.find(baseURL)
    if start != -1:
        m = re.search(r'(?:dp\/[\w]*)|(?:gp\/product\/[\w]*)',msg[start:].split()[0])
        if m != None:
            pCode = m.group(0)
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=newReferURL(pCode, update))
       
def main():
    """ Start the bot. """

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(    
                   Filters.text & (Filters.entity(MessageEntity.URL) |
                                    Filters.entity(MessageEntity.TEXT_LINK)), filterText))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print('Bot is going to start...')
    main()
