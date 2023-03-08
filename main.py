# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 23:25:39 2023

@author: adril
"""

import nltk
# from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer, SnowballStemmer
# from nltk.corpus import stopwords

# import pandas as pd

# import sklearn
# from sklearn.feature_extraction.text import CountVectorizer

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

nltk.download('punktl')


def tokenize (string):
    return nltk.word_tokenize(string)


string = input("enter a sentence: ")
print(tokenize(string))