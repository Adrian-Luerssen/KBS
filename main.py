# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 23:25:39 2023

@author: adril
"""
import random as r
import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import pandas as pd

import sklearn
from sklearn.feature_extraction.text import CountVectorizer

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


def preProcessing (string):
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(string)
    tokens = [w for w in tokens if not w.lower() in stop_words]
    #lancaster = LancasterStemmer()
    stemmed=[]
    for w in tokens:
        #stemmed.append(lancaster.stem(w))
        stemmed.append(w.lower())
            
    return stemmed

def updateVocab ():
    vectorizer = sklearn.feature_extraction.text.CountVectorizer()
    sentences = []
    with open("data/testPhrases.txt") as f:
        lines = [line.rstrip() for line in f]
    for line in lines:
        sentences.append(' '.join([str(elem) for elem in preProcessing(line)]))
        
    vectorizer.fit(sentences)
    return vectorizer
        
    
def generateResponse(sentence):
    tokens = preProcessing(sentence)
    responses = {'add':'i will add this task to your schedule ',
                 'cancel':'this event has been canceled ',
                 'show':'Here are the events you have',
                 'schedule':'i have put this in your calendar ',
                 'reschedule':'i have updated this event',
                 'update':'i have updated your calendar '}
    
    response = 'i dont know how to respond'
    #print(tokens)
    if tokens[0] in responses:
        response = responses[tokens[0]]
    return response
    

string = "Can you schedule an event for tomorrow at 2pm"#input("enter a sentence: ")
tokens = preProcessing(string)
#print (tokens)
    
string = "when is the next 2h gap i have?"#input("enter a sentence: ")
tokens = preProcessing(string)
#print (tokens)

with open("data/testPhrases.txt") as f:
    lines = [line.rstrip() for line in f]
limit = 5
for line in lines:
    if (limit >= 1 and r.randint(0,100) > 60):
        print("in:  ",line)
        print("out: ",generateResponse(line))
        print()
        limit-=1;
#print(pd.get_dummies(tokens))


#print(updateVocab().vocabulary_)

#sting = input ("please type a sentence: ")
#print ("chatbot: "+generateResponse(sting))
