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
while True:
    updates = bot.get_updates()
    print(updates)
    print("cp")
    # for u in updates:
    #     message = u.message.text
    #     print(message)

#Function that does NLP
def text_prepare(message):
    message = message.translate(string.punctuation)

    #tokenize
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_list = (tokenizer.tokenize(message))

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

# #!/usr/bin/python3
# from telegram.ext import Updater
# from telegram.ext import CommandHandler, CallbackQueryHandler
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# ############################### Bot ############################################
# def start(bot, update):
#   update.message.reply_text(main_menu_message(),
#                             reply_markup=main_menu_keyboard())

# def main_menu(bot, update):
#   query = update.callback_query
#   bot.edit_message_text(chat_id=query.message.chat_id,
#                         message_id=query.message.message_id,
#                         text=main_menu_message(),
#                         reply_markup=main_menu_keyboard())

# def first_menu(bot, update):
#   query = update.callback_query
#   bot.edit_message_text(chat_id=query.message.chat_id,
#                         message_id=query.message.message_id,
#                         text=first_menu_message(),
#                         reply_markup=first_menu_keyboard())

# def second_menu(bot, update):
#   query = update.callback_query
#   bot.edit_message_text(chat_id=query.message.chat_id,
#                         message_id=query.message.message_id,
#                         text=second_menu_message(),
#                         reply_markup=second_menu_keyboard())

# # and so on for every callback_data option
# def first_submenu(bot, update):
#   pass

# def second_submenu(bot, update):
#   pass

# ############################ Keyboards #########################################
# def main_menu_keyboard():
#   keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
#               [InlineKeyboardButton('Option 2', callback_data='m2')],
#               [InlineKeyboardButton('Option 3', callback_data='m3')]]
#   return InlineKeyboardMarkup(keyboard)

# def first_menu_keyboard():
#   keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
#               [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
#               [InlineKeyboardButton('Main menu', callback_data='main')]]
#   return InlineKeyboardMarkup(keyboard)

# def second_menu_keyboard():
#   keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
#               [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
#               [InlineKeyboardButton('Main menu', callback_data='main')]]
#   return InlineKeyboardMarkup(keyboard)

# ############################# Messages #########################################
# def main_menu_message():
#   return 'Choose the option in main menu:'

# def first_menu_message():
#   return 'Choose the submenu in first menu:'

# def second_menu_message():
#   return 'Choose the submenu in second menu:'

# ############################# Handlers #########################################
# updater = Updater('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
# updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
# updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
# updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,
#                                                     pattern='m1_1'))
# updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
#                                                     pattern='m2_1'))

# updater.start_polling()
# ################################################################################