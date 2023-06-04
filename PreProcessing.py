#import sklearn
import nltk
from nltk import LancasterStemmer
from nltk.corpus import stopwords, wordnet, words
from nltk.tokenize import RegexpTokenizer
from nltk.metrics import edit_distance


import re
with open('data/dictionarySpellcheck') as word_file:
    valid_words = set(word_file.read().split(","))
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('maxent_ne_chunker')
nltk.download('words')

stop_words = set(stopwords.words('english'))
stop_words.remove('not')
stop_words.remove('no')
stop_words.remove('nor')
stop_words.remove('but')
stop_words.remove('against')
stop_words.add('want')
tokenizer = RegexpTokenizer(r'\w+')
lancaster = LancasterStemmer()
def preProcessing(string,debug=False):


    tokens = tokenizer.tokenize(string)
    tokens = [w for w in tokens if not w.lower() in stop_words]
    if debug:print(tokens)
    stemmed = {}
    # TODO: Fix spelling mistakes on input
    for w in tokens:
        if debug:print(w)
        a = lancaster.stem(spellcheck(w))
        stemmed[a] = synonym_extractor(w)
        stemmed[a].append(a)
        # stemmed.append(w.lower())


    return stemmed


def spellcheck(word,distance_threshold=2,debug=False):
    #if the word is a number, return it
    if word.isdigit() or re.search(r'^(?=.*\d)[a-zA-Z\d]+$', word):
        return word
    if word.lower() not in words.words():
        # find the closest matching word from the set of valid English words
        closest_word = min(valid_words, key=lambda w: edit_distance(word.lower(), w))

        # calculate the Levenshtein distance between the misspelled word and the closest valid word
        distance = edit_distance(word.lower(), closest_word)

        # if the distance is less than or equal to the threshold, add the misspelled word and its correction to the dictionary
        if distance <= distance_threshold:
            if debug:print("Word not in english vocab. word: " + word+"  closest match: "+closest_word)
            return closest_word
    return word


def synonym_extractor(word):

    # create a dictionary of the original words and their synonyms
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            a= lancaster.stem(l.name())
            if len(a) > 0:
                synonyms.append(a)




    return synonyms

