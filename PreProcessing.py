import sklearn
from nltk import LancasterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import Processing as pro


# nltk.download('stopwords')

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

    # print(stemmed)
    return stemmed


def updateVocab():
    vectorizer = sklearn.feature_extraction.text.CountVectorizer()
    sentences = []
    with open("data/testPhrases.txt") as f:
        lines = [line.rstrip() for line in f]
    for line in lines:
        sentences.append(' '.join([str(elem) for elem in preProcessing(line)]))

    vectorizer.fit(sentences)
    return vectorizer


def searchOptions(tokens):  # Searches for words
    notString = ['not']  # Checks for the opposite
    a = [(w, notString.count(w)) for w in set(notString) if w in tokens]
    if (len(a) != 0): return 5

    expandString = ['expand', 'question', 'query', 'inquiry', 'more',
                    'specify']  # TODO if the user wants to modify its exp.
    # changeString = ['change', 'modify', 'eliminate', 'drop', 'delete', 'remove', 'eradicate', 'exterminate', 'suspend']
    showString = ['show', 'manifest', 'display', 'appear', 'reveal', 'indicate', 'present', 'search', 'open']
    # rescheduleString = ['reschedule', 'postpone', 'rearrange']
    # updateString = ['update', 'renovate', 'recondition', 'swap', 'change', 'move']

    a = [(w, tokens.count(w)) for w in set(tokens) if w in expandString]
    # b = [(w, tokens.count(w)) for w in set(tokens) if w in cancelString]
    c = [(w, tokens.count(w)) for w in set(tokens) if w in showString]
    # d = [(w, tokens.count(w)) for w in set(tokens) if w in rescheduleString]
    # e = [(w, tokens.count(w)) for w in set(tokens) if w in updateString]

    if (len(c)) == 0 and (len(a)) == 0: return 0
    # if (len(a)) == 0 and (len(b)) == 0 and (len(c)) == 0 and (len(d)) == 0 and (len(e)) == 0: return 5
    if (len(a) != 0):
        a1 = a[0][1]
    else:
        a1 = 0
    # if (len(b) != 0): b1 = b[0][1]
    # else: b1 = 0
    if (len(c) != 0):
        c1 = c[0][1]
    else:
        c1 = 0
    # if (len(d) != 0): d1 = d[0][1]
    # else: d1 = 0
    # if (len(e) != 0): e1 = e[0][1]
    # else: e1 = 0

    if a1 > c1:
        return 1
    else:
        return 2
    # if a1 > b1 and a1 > c1 and a1 > d1 and a1 > e1: return 0
    # if b1 > a1 and b1 > c1 and b1 > d1 and b1 > e1: return 1
    # if c1 > b1 and c1 > a1 and c1 > d1 and c1 > e1: return 2
    # if d1 > b1 and d1 > c1 and d1 > a1 and d1 > e1: return 3
    # if e1 > b1 and e1 > c1 and e1 > d1 and e1 > a1: return 4
    # return 5


def menuOptions(tokens, user):  # This will execute the functions of Event, update the DB
    value = searchOptions(tokens)
    if value == 0:
        pro.createUser(tokens, user)
    elif value == 1:
        print("more questions")
    elif value == 2:
        print("show")
    # elif value == 3:
    #   print("reschedule")
    # elif value == 4:
    #   print("update")
    else:
        print("Don't know")


def generateResponse(sentence, user):
    tokens = preProcessing(sentence)
    responses = {0: 'Data accepted! You might want to ask more questions for more accurate responses:',
                 1: 'I will ask more questions:',
                 2: 'These are our recommendations',
                 #             3:'I have updated this event',
                 #             4:'I have updated your calendar',
                 5: 'I dont know how to respond'}

    menuOptions(tokens, user)  # Does the action to the event

    value = searchOptions(tokens)
    print("Out: ", responses[value], "\n")
