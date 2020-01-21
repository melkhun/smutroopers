#Import libraries
import telegram
import numpy as np
import pandas as pd

DIR='/Desktop/smutroopers/'

#Import libraries for NLP
import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

#Import the telegram bot
bot = telegram.Bot(token='983827853:AAFgNAfleRKi2F-9imywEtRD-9A8ermlrQA')

print(bot.get_me())
{"first_name": "Toledo's Palace Bot", "username": "ToledosPalaceBot"}

from telegram.ext import Updater
updater = Updater(token='983827853:AAFgNAfleRKi2F-9imywEtRD-9A8ermlrQA', use_context=True)

dispatcher = updater.dispatcher

#For error logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I am YouTrip's Superbot. How can I help you today?")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#to start the bot
updater.start_polling()

#Handler that echos to all text messages
# def echo(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
# echo_handler = MessageHandler(Filters.text, echo)
# dispatcher.add_handler(echo_handler)


#Store all messages as 'message'
updates = bot.get_updates()
for u in updates:
    message = u.message.text


#Function that does NLP
def text_prepare(message):
    #remove punctuation
    punctuation = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(punctuation) for w in message]

    #tokenize
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_list = (tokenizer.tokenize(stripped))

    #remove stopwords
    stopWords = set(stopwords.words('english'))

    wordsFiltered = []
    for w in tokenized_list:
        if w not in stopWords:
            wordsFiltered.append(w)

    #stemming
    ps = PorterStemmer()

    wordsFiltered2 = []
    for word in wordsFiltered:
        wordsFiltered2.append(ps.stem(word))

    return wordsFiltered2



#Bot Reply based on user input
bot_reply = pd.read_csv('Desktop/smutroopers/bot_reply.csv')
bot_reply_dict = bot_reply.set_index('words').T.to_dict()

for key, value in bot_reply_dict.items():
    key = text_prepare(key)
    #print(key)
    #print(text_prepare(message))
    if(set(text_prepare(message)) == set(key)):
        #print(value['reply'])
        reply = value['reply']
    else:
        reply = "Sorry I didn't quite get you."
        #print(reply)


#Reply handler    
def reply_user(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

bot_reply_handler = MessageHandler(True, reply_user)
dispatcher.add_handler(bot_reply_handler)

# #Reply if unknown command given
# def unknown(update, context):
#     error_msg_counter = 0
#     if error_msg_counter == 0:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="This not a valid command! Try another command can?")
#         error_msg_counter += 1
#     else:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Nope, that's not it either.")

# unknown_handler = MessageHandler(Filters.command, unknown)
# dispatcher.add_handler(unknown_handler)

# from telegram.ext import BaseFilter



#Custom Filters

# class BotReplyFilter(BaseFilter):
#     #def filter(self, message):
#         #return 'hi' in message.text
#     def filter(self, message):
#         message_text = message.text
#         lower_message_text = message_text.lower()
#         if lower_message_text in ['hi', 'hey', 'hello']:
#             return True

#     def reply(update, context):
#             context.bot.send_message(chat_id=update.effective_chat.id, reply)

# #Initialize the class.
# hello_filter = BotReplyFilter()
# bot_reply_handler = MessageHandler(True, reply)
# dispatcher.add_handler(bot_reply_handler)
