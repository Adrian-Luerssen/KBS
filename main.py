# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 23:25:39 2023

@author: adril
"""

import nltk
# from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords

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
    tokens = nltk.word_tokenize(string)
    tokens = [w for w in tokens if not w.lower() in stop_words]
            
    return tokens

def updateVocab ():
    vectorizer = sklearn.feature_extraction.text.CountVectorizer()
    sentences = []
    with open("data/testPhrases.txt") as file:
        sentences.append(file.read())
        
    vectorizer.fit(sentences)
    return vectorizer
        
    
    
    
string = "hello how are you?"#input("enter a sentence: ")
tokens = preProcessing(string)
print (tokens)
    
string = "Can you schedule an event for tomorrow at 2pm"#input("enter a sentence: ")
tokens = preProcessing(string)
print (tokens)
    
string = "when is the next 2h gap i have?"#input("enter a sentence: ")
tokens = preProcessing(string)
print (tokens)

#print(pd.get_dummies(tokens))


#print(updateVocab().vocabulary_)


