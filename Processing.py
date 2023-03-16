"""
Created on Sun Mar 12 19:27:21 2023

@author: Sergi Vives
"""
import PreProcessing as pre
import User 
import random as r

def errorHandler(error):
    print("Out: please specify the ", error, " to better understand what you mean")
    sentence = input("In: ")
    return pre.preProcessing(sentence)

def setCarSentence(tokens, user, initial, value):
    loop = True
    while (loop):
        typeString = ['mdx', 'ilx', 'rdx', 'nsx', 'rlx', 'tlx', 'tl', 'tsx', 'zdx', 'rl', 'cl',
                      'integra', 'slx', 'legend', 'vigor', '4c', 'gt', 'db9', 'rapide', 'vantage',
                      'vanquish', 'virage', 'a3', 'a4', 'a5', 'a6', 'a7']
        a = [(w, tokens.count(w)) for w in set(tokens) if w in typeString]

        if (len(a) == 0 and initial): loop = False
        elif (len(a)) == 0: tokens = errorHandler("name")
        else: 
            user.setFavCar(a[0][0])
            return value + 1    
    return value
            

def setManufacturerSentence(tokens, user, initial, value):
    loop = True
    while (loop):
        typeString = ['acura', 'audi', 'romeo', 'aston', 'alfa']
        a = [(w, tokens.count(w)) for w in set(tokens) if w in typeString]
            
        if (len(a) == 0 and initial): loop = False
        elif (len(a)) == 0: tokens = errorHandler("manufacturer")
        else: 
            user.setFavManufacturers(a[0][0])
            return value + 1    
    return value

def setCategorySentence(tokens, user, initial, value):
    loop = True
    while (loop):
        typeString = ['compact', 'luxury', 'performance', 'crossover', 'factory', 'midsize', 'exotic',
                      'hatchback']
        a = [(w, tokens.count(w)) for w in set(tokens) if w in typeString]
            
        if (len(a) == 0 and initial): loop = False
        elif (len(a)) == 0: tokens = errorHandler("category")
        else: 
            user.setCategories(a[0][0])
            return value + 1    
    return value

def createUser(tokens, user):
    value = 0
    value = setCarSentence(tokens, user, True, value)
    value = setManufacturerSentence(tokens, user, True, value)
    value = setCategorySentence(tokens, user, True, value)

    if (value == 0):
        while (True):
            random = r.randint(0,5)
            if (random == 0 and user.getFavCar() == 0):
                tokens = pre.preProcessing(input("Which are your favourite car models?"))
                setCarSentence(tokens,user,False, value)
                break
            elif (random == 1 and user.getFavManufacturers() == 0):
                tokens = pre.preProcessing(input("Which is the brand of your dreams?"))
                setManufacturerSentence(tokens,user,False, value)
                break
            elif (random == 2 and user.getCategories() == 0):
                tokens = pre.preProcessing(input("How would you describe your ideal car category?"))
                setCategorySentence(tokens,user,False, value)
                break
            elif (random == 3 and user.getStyles() == 0):
                tokens = pre.preProcessing(input("Which is your car style do you fit better?"))
                setCarSentence(tokens,user,False, value) #TODO change to car style once it is adapted
                break
            elif (random == 4 and user.getFuelTypes() == 0):
                tokens = pre.preProcessing(input("Which are fuel type is of your liking?"))
                setCarSentence(tokens,user,False, value) #TODO change to fuel types once it is adapted
                break
            elif (random == 5 and user.getTransmissionTypes() == 0):
                tokens = pre.preProcessing(input("Which transmission type do you prefer?"))
                setCarSentence(tokens,user,False, value) #TODO change to transmission types once it is adapted
                break
            else:
                print("You can only change the data you entered!") 
                break

   # print("Out: The user likes the car: ", use, ", scheduled on ", date, month)
  #  time = getTime(tokens)
  #  length = getLength(tokens)
