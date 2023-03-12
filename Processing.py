"""
Created on Sun Mar 12 19:27:21 2023

@author: Sergi Vives
"""
import PreProcessing as pre
from datetime import datetime

def errorHandler(error):
    print("Out: please specify the ", error, " to better create the task")
    sentence = input("In: ")
    return pre.preProcessing(sentence)

def getType(tokens):
    while (True):
        typeString = ['meeting', 'doctor', 'family', 'friends', 'dinner', 'lunch', 'homework', 'exams', 'study']
        a = [(w, tokens.count(w)) for w in set(tokens) if w in typeString]
        
        if (len(a)) == 0: tokens = errorHandler("name")
        else: return a[0][0]

def getDay(tokens):
    typeString = ['day', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'today', 'tomorrow']
    a = [(w, tokens.count(w)) for w in set(tokens) if w in typeString]
        
    if (len(a)) == 0: return datetime.now().strftime('%A') #TODO next day is not well set
    else: return a[0][0]

def getMonth(tokens):
    typeString = ['month', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
        'october', 'november', 'december']
    a = [(w, tokens.count(w)) for w in set(tokens) if w in typeString]
        
    if (len(a)) == 0: return datetime.now().strftime('%B') #TODO next month is not well set
    else: return a[0][0]

def createEvent(tokens):
    name = getType(tokens)
    date = getDay(tokens)
    month = getMonth(tokens)

    print("Out: The event is called: ", name, ", scheduled on ", date, month)
  #  time = getTime(tokens)
  #  length = getLength(tokens)
