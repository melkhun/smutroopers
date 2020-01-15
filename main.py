import telegram

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


#need to write a filter for random replies
### Note: The Filters class contains a number of functions that filter incoming messages for text, images, status updates and more. 
# Any message that returns True for at least one of the filters passed to MessageHandler will be accepted. You can also write your own filters if you want. 
# See more in Advanced Filters. https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Advanced-Filters
###

#Reply if unknown command given
def unknown(update, context):
    error_msg_counter = 0
    if error_msg_counter == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="This not a valid command! Try another command can?")
        error_msg_counter += 1
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Nope, that's not it either.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

from telegram.ext import BaseFilter

#Custom Filters

class HelloFilter(BaseFilter):
    #def filter(self, message):
        #return 'hi' in message.text
    def filter(self, message):
        message_text = message.text
        lower_message_text = message_text.lower()
        if lower_message_text in ['hi', 'hey', 'hello']:
            return True

def hello(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! How are you doing?")

#Initialize the class.
hello_filter = HelloFilter()
hello_handler = MessageHandler(hello_filter, hello)
dispatcher.add_handler(hello_handler)
