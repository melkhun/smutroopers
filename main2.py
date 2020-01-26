import requests as requests
import random

url = "https://api.telegram.org/bot983827853:AAFgNAfleRKi2F-9imywEtRD-9A8ermlrQA/"

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

# create func that get chat id
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id


# create function that get message text
def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


# create function that get last_update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]  # get last record message update


# create function that let bot send message to user
def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text}
    response = requests.post(url + "sendMessage", data=params)
    return response


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

def main():
    reply = "Sorry I don't have any answer."
    update_id = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        if update_id == update["update_id"]:
            for key, value in bot_reply_dict.items():
                key = text_prepare(key)    
                if(set(text_prepare(get_message_text(update))) == set(key)):
                    reply = value['reply']
                else:
                    pass
            send_message(get_chat_id(update), reply)
            update_id += 1
            

# call the function to make it reply
main()
