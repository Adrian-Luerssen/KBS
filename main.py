# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 23:25:39 2023

@author: adril
"""

import random as r


from datetime import datetime

import PreProcessing as prep
import User



# import sklearn
# from sklearn import datasets, metrics, feature_extraction
# from sklearn.feature_extraction.text import CountVectorizer
# import sklearn.manifold

# import glob
# import codecs
# import re
# import gensim
# import gensim.models.word2vec as w2v
# import seaborn as sns
# import scipy

#nltk.download('punktl')
#nltk.download('stopwords')
#nltk.download('wordnet')
    

def examplesTest():
    with open("data/testPhrases.txt") as f:
        lines = [line.rstrip() for line in f]
    limit = 5
    for line in lines:
        if (limit >= 1 and r.randint(0,100) > 60):
            print("in:  ",line)
            print("out: ",prep.generateResponse(line))
            print()
            limit-=1;

def mainExecute():
    print("This is the KBS Event Chatbot, at your disposal.")
    print("The current date is: ", datetime.now().strftime('%A'),",", datetime.now().day,
            datetime.now().strftime('%B'), datetime.now().hour, ":", datetime.now().minute)
    print("How can I help you?\n")
    
    user = User.User()

    value = True
    while (value):
        string = input("In: ")
        if string == 'Bye' or string == 'bye': value = False
        else: prep.generateResponse(string, user)
        
#string = "Can you schedule an event for tomorrow at 2pm"#input("enter a sentence: ")
#tokens = prep.preProcessing(string)
#print (tokens)
    
#string = "when is the next 2h gap i have?"#input("enter a sentence: ")
#tokens = prep.preProcessing(string)
#print (tokens)

#examplesTest()
mainExecute()





#print(pd.get_dummies(tokens))


#print(updateVocab().vocabulary_)

#sting = input ("please type a sentence: ")
#print ("chatbot: "+generateResponse(sting))
