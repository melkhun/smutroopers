
#Our Chatbot API
url = "https://api.telegram.org/bot983827853:AAFgNAfleRKi2F-9imywEtRD-9A8ermlrQA/"

#Import libraries
import requests as requests
import random
import telegram
import pandas as pd
import os
import json
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk import pos_tag
import numpy as np
import pickle
import string
import timeit
import sklearn

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer 

import warnings
warnings.simplefilter('ignore')


DIR='/Desktop/smutroopers/'


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

# Make our bot_reply.csv into a a JSON file called 'bot_reply.json'
convdata = pd.read_csv('Desktop/smutroopers/bot_reply.csv')

convdata_json = json.loads(convdata.to_json(orient='records')) #Covert dataframes to json
with open('bot_reply.json', 'w') as outfile:
    json.dump(convdata_json, outfile)

# Function - to respond to Greetings 
GREETING_INPUTS = ("hello", "hi", "greetings", "hello i need help", "good day","hey","i need help", "greetings", "good morning")
GREETING_RESPONSES = ["Good day, How may i of help?", "Hello, How can i help?", "hello", "I am glad! You are talking to me."]
           
def greeting(message):
    for word in message.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


#Functions that does NLP
lemmer = nltk.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

# Remove punctuation
def RemovePunction(tokens):
    return[t for t in tokens if t not in string.punctuation]

# Create a stopword list from the standard list of stopwords available in nltk
stop_words = set(stopwords.words('english'))
print(len(stop_words))

# Main Chatbot

def text_prepare(message):
    json_file_path = "bot_reply.json" 
    tfidf_vectorizer_pickle_path = "tfidf_vectorizer.pkl"
    tfidf_matrix_pickle_path = "tfidf_matrix_train.pkl"
    
    i = 0
    sentences = []
    
    # ---------------Tokenisation of user input -----------------------------#
    
    tokens = RemovePunction(nltk.word_tokenize(message))
    pos_tokens = [word for word,pos in pos_tag(tokens, tagset='universal')]
    
    word_tokens = LemTokens(pos_tokens)
    
    filtered_sentence = []
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)  
    
    filtered_sentence =" ".join(filtered_sentence).lower()
            
    test_set = (filtered_sentence, "")
    
    #For Tracing, comment to remove from print.
    #print('USER INPUT:'+filtered_sentence)
    
    # -----------------------------------------------------------------------#
        
    try: 
        # ---------------Use Pre-Train Model------------------#
        f = open(tfidf_vectorizer_pickle_path, 'rb')
        tfidf_vectorizer = pickle.load(f)
        f.close()
        
        f = open(tfidf_matrix_pickle_path, 'rb')
        tfidf_matrix_train = pickle.load(f)
        # ---------------------------------------------------#
    except: 
        # ---------------To Train------------------#
        
        start = timeit.default_timer()
        
        with open(json_file_path) as sentences_file:
            reader = json.load(sentences_file)
            
            # ---------------Tokenisation of training input -----------------------------#    
            
            for row in reader:
                db_tokens = RemovePunction(nltk.word_tokenize(row['words']))
                pos_db_tokens = [word for word,pos in pos_tag(db_tokens, tagset='universal')]
                db_word_tokens = LemTokens(pos_db_tokens)
                
                db_filtered_sentence = [] 
                for dbw in db_word_tokens: 
                    if dbw not in stop_words: 
                        db_filtered_sentence.append(dbw)  
                
                db_filtered_sentence =" ".join(db_filtered_sentence).lower()
                
                #Debugging Checkpoint
                print('TRAINING INPUT: '+db_filtered_sentence)
                
                sentences.append(db_filtered_sentence)
                i +=1                
            # ---------------------------------------------------------------------------#
                
        tfidf_vectorizer = TfidfVectorizer() 
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)
        
        #train timing
        stop = timeit.default_timer()
        print ("Training Time : ")
        print (stop - start) 
    
        f = open(tfidf_vectorizer_pickle_path, 'wb')
        pickle.dump(tfidf_vectorizer, f) 
        f.close()
    
        f = open(tfidf_matrix_pickle_path, 'wb')
        pickle.dump(tfidf_matrix_train, f) 
        f.close 
        # ------------------------------------------#
        
    #use the learnt dimension space to run TF-IDF on the query
    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

    #then run cosine similarity between the 2 tf-idfs
    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
    
    #if not in the topic trained.no similarity 
    idx= cosine.argsort()[0][-2]
    flat =  cosine.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if (req_tfidf==0): #Threshold A
        
        not_understood = "Apology, I do not understand. Can you rephrase?"
        
        return not_understood, not_understood, 2
        
    else:
        
        cosine = np.delete(cosine, 0)

        #get the max score
        max = cosine.max()
        response_index = 0

        #if max score is lower than < 0.34 > (we see can ask if need to rephrase.)
        if (max <= 0.34): #Threshold B
            
            not_understood = "Apology, I do not understand. Can you rephrase?"
            
            return not_understood,not_understood, 2
        else:

                #if score is more than 0.91 list the multi response and get a random reply
                if (max > 0.91): #Threshold C
                    
                    new_max = max - 0.05 
                    # load them to a list
                    list = np.where(cosine > new_max) 
                   
                    # choose a random one to return to the user 
                    response_index = random.choice(list[0])
                else:
                    # else we would simply return the highest score
                    response_index = np.where(cosine == max)[0][0] + 2 

                j = 0 

                with open(json_file_path, "r") as sentences_file:
                    reader = json.load(sentences_file)
                    for row in reader:
                        j += 1 
                        if j == response_index: 
                            return row["reply"], row["words"], max
                            break

# def text_prepare(message):
#     message = message.translate(string.punctuation)
#     message = message.lower()

#     #tokenize
#     tokenizer = RegexpTokenizer(r'\w+')
#     tokenized_list = (tokenizer.tokenize(message))

#     #remove stopwords
#     stopWords = set(stopwords.words('english'))

#     wordsFiltered = []
#     for w in tokenized_list:
#         if w not in stopWords:
#             wordsFiltered.append(w)

#     #stemming
#     ps = PorterStemmer()

#     wordsFiltered2 = []
#     for word in wordsFiltered:
#         wordsFiltered2.append(ps.stem(word))

#     return wordsFiltered2


#Bot Reply based on user input
# bot_reply = pd.read_csv('Desktop/smutroopers/bot_reply.csv')
# bot_reply_dict = bot_reply.set_index('words').T.to_dict()

# def main():
#     reply = "Sorry I don't have any answer."
#     update_id = last_update(url)["update_id"]
#     while True:
#         update = last_update(url)
#         if update_id == update["update_id"]:
#             for key, value in bot_reply_dict.items():
#                 key = text_prepare(key)    
#                 if(set(text_prepare(get_message_text(update))) == set(key)):
#                     reply = value['reply']
#                 else:
#                     pass
#             send_message(get_chat_id(update), reply)
#             update_id += 1
            
def main():
    update_id = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        if update_id == update["update_id"]:
            message =  get_message_text(update)
            if(message.lower()!='bye'):
                if(greeting(message.lower())!=None):
                    reply = greeting(message.lower())
                    send_message(get_chat_id(update), reply)
                else:
                    response_primary, response_message, line_id_primary = text_prepare(message)
                    reply = response_primary
                send_message(get_chat_id(update), reply)
                update_id += 1

# call the function to make it reply
main()
