#import sklearn
import nltk
from nltk import LancasterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


import re

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('wordnet')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

def preProcessing(string):
    stop_words = set(stopwords.words('english'))
    stop_words.remove('not')
    stop_words.remove('no')
    stop_words.remove('nor')
    stop_words.remove('but')
    stop_words.remove('against')
    tokenizer = RegexpTokenizer(r'\w+')

    tokens = tokenizer.tokenize(string)
    tokens = [w for w in tokens if not w.lower() in stop_words]
    lancaster = LancasterStemmer()
    stemmed = []

    # TODO: Fix spelling mistakes on input
    for w in tokens:

        stemmed.append(lancaster.stem(w))
        # stemmed.append(w.lower())


    return stemmed


def spellcheck(word, max_distance=2):

    return word