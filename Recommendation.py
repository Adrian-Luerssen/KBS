import PreProcessing as prep

import re
import DAO


class profile:
    min_price = 0
    max_price = 0
    # priorities = []
    limit = {}

    def __int__(self):
        # define priorities
        self.min_price = 0
        self.max_price = 0
        # self.priorities = []  # the priorities from the decision tree will move
        self.limit = {}  # the limitations of the recommendations, key is the limited factor : values are what we will be limiting by


class questions:
    def __init__(self):
        self.profile = profile()

        self.dao = DAO.DAO("data/data.csv")

        for parameter in self.dao.columns:
            self.profile.limit[parameter] = "any"

        self.questionToKey = {}
        self.questions = {}
        self.answerBank = {}
        self.answered = {}
        self.end_reached = False
        self.mpg = ""

        self.questions["price"] = "What is your price range?"
        self.answerBank["price"] = []
        self.answered["price"] = False

        self.questions["priority"] = "What is your priority when buying a car?"
        self.answerBank["priority"] = ["reliability", "efficiency", "fun",
                                       "space", "use", "fast", "safety"]
        self.answered["priority"] = False

        self.questions["environment"] = "Do you prefer a faster car or an eco-friendly one?"
        self.answerBank["environment"] = ["fast", "eco", "friendly", "efficient", "balanced"]
        self.answered["environment"] = False

        self.questions["terrain"] = "What type of terrain do you drive on?"
        self.answerBank["terrain"] = ["city", "highway", "offroad"]
        self.answered["terrain"] = False

        self.questions["circuit"] = "Will you take the car to a circuit?"
        self.answerBank["circuit"] = ["yes", "no"]
        self.answered["circuit"] = False

        self.questions["area"] = "Where do you live?"
        self.answerBank["area"] = ["urban", "suburb",
                                   "rural"]  # can assume suburb takes highway often and rural takes off-road often
        self.answered["area"] = False

        self.questions["use"] = "What are you going to use the car for?"
        self.answerBank["use"] = ["groceries", "commute", "family", "sports", "work", "travel"]
        # can assume groceries and commute are city and suburb, family is suburb, sports is off-road, luxury is highway, work is city, travel is highway
        self.answered["use"] = False

        for key in self.answerBank:
            a = self.answerBank[key]
            self.answerBank[key]={}
            for i in range(len(a)):
                new = prep.preProcessing(a[i])
                self.answerBank[key][list(new.keys())[0]] = list(new.values())[0]

        print(self.answerBank)
    def validWord(self, question, known_word, input):
        known_synonyms = self.answerBank[question][known_word]
        # Check if any of the input synonyms coincide with the known synonyms
        common_synonyms = [value for value in known_synonyms if value in input]
        #print(input)
        #print(known_synonyms)
        if common_synonyms:
            #print( f"The input word is a synonym of the known word '{known_word}' through the following synonyms: {common_synonyms}")
            return True

        return False

    def obtainPriceRange(self, question, response):
        lst = []
        # print(response)
        # join thousand or k to the number
        pos = 0
        while pos < len(response) - 1:
            # print(response)
            if re.search("^[0-9]*$", response[pos]):
                if "thousand" == response[pos + 1] or "k" == response[pos + 1]:
                    response[pos] = response[pos] + "k"
                    response = response[:pos + 1] + response[pos + 2:]
                elif  "m" == response[pos + 1] or "million" == response[pos + 1]:
                    response[pos] = response[pos] + "m"
                    response = response[:pos + 1] + response[pos + 2:]
            pos += 1

        # print(response)
        for tok in response:
            if re.search("[0-9]k", tok) or re.search("[0-9]thousand", tok):
                lst.append(float(tok.replace("k", "").replace("thousand", "")) * 1000)
            elif re.search("[0-9]m", tok) or re.search("[0-9]million", tok):
                lst.append(float(tok.replace("mil", "").replace("m", "")) * 1000000)
            elif re.search("[0-9]", tok):
                lst.append(float(tok))
        print(lst)
        if (len(lst)) == 0:
            self.answered[question] = False
            return False
        else:
            self.answered[question] = True
            if len(lst) == 1:
                self.profile.max_price = lst[0]
            else:
                if lst[0] < lst[1]:
                    self.profile.min_price = lst[0]
                    self.profile.max_price = lst[1]
                else:
                    self.profile.min_price = lst[1]
                    self.profile.max_price = lst[0]
            return True

    def getResponse(self, question, response):
        self.answered[question] = True
        print(response)
        for token in response:
            if token in self.answerBank[question]:
                if question == "priority":
                    self.profile.priorities.append(token)
                else:
                    if question not in self.profile.limit:
                        self.profile.limit[question] = []
                    self.profile.limit[question].append(
                        token)  # TODO: change to set values, if cares about fuel -> electric or low mpg, choose

    def saveAnswer(self, question, response):
        if question == "price":
            self.profile.limit["price"] = str(self.profile.max_price)
            self.profile.limit["price_min"] = str(self.profile.min_price)
            return

        for word,synonyms in response.items():
            print(synonyms)
            if question == "priority":
                #print(self.validWord(question, "", synonyms))
                if self.validWord(question, "spac", synonyms):
                    self.profile.limit["doors"] = "4"
                    self.profile.limit["size"] = "large,midsize"
                if self.validWord(question, "efficy", synonyms):
                    self.mpg = "high"
                if self.validWord(question, "fun", synonyms):
                    self.profile.limit["hp"] = "high"
                if self.validWord(question, "fast", synonyms):
                    self.profile.limit["hp"] = "high"
                    self.profile.limit["category"] = "exotic,factory tuner,performance,high-performance"
                if self.validWord(question, "saf", synonyms):
                    self.profile.limit["year"] = "2012"
                if self.validWord(question, "rely", synonyms):
                    self.profile.limit["year"] = "2014"
                    self.profile.limit["transmission"] = "automatic"
            elif question == "environment":
                if self.validWord(question, "fast", synonyms):
                    self.profile.limit["hp"] = "high"
                    self.profile.limit["category"] = "exotic,factory tuner,performance"
                if self.validWord(question, "eco", synonyms) or self.validWord(question, "friend", synonyms) or self.validWord(question, "efficy", synonyms):
                    self.profile.limit["mpg"] = "high"
                    self.profile.limit["fuel_type"] = "electric"
                if self.validWord(question, "bal", synonyms):
                    self.profile.limit["hp"] = "high"
            elif question == "terrain":
                if self.validWord(question, "city", synonyms):
                    self.profile.limit["city_mpg"] = "high"
                if self.validWord(question, "highway", synonyms):
                    self.profile.limit["highway_mpg"] = "high"
                if self.validWord(question, "offroad", synonyms):
                    self.profile.limit["driven_wheels"] = "all wheel drive,four wheel drive"
            elif question == "circuit":
                if self.validWord(question, "ye", synonyms):
                    self.profile.limit["cylinders"] = "high"
                    #self.profile.limit["transmission"] = "manual"
            elif question == "area":
                if self.validWord(question, "urb", synonyms):
                    self.profile.limit["category"] = "hybrid,luxury,hatchback"
                    if self.mpg == "high":
                        self.profile.limit["city_mpg"] = "high"
                if self.validWord(question, "suburb", synonyms):
                    self.profile.limit["category"] = "crossover,hatchback,luxury"
                    if self.mpg == "high":
                        self.profile.limit["highway_mpg"] = "high"
                if self.validWord(question, "rur", synonyms):
                    self.profile.limit["category"] = "crossover"
                    if self.mpg == "high":
                        self.profile.limit["highway_mpg"] = "high"
            elif question == "use":
                if self.validWord(question, "grocery", synonyms):
                    self.profile.limit["category"] = "hybrid,hatchback"
                    self.profile.limit["size"] = "midsize"
                if self.validWord(question, "commut", synonyms):
                    self.profile.limit["category"] = "hybrid,luxury,hatchback"
                if self.validWord(question, "famy", synonyms):
                    self.profile.limit["category"] = "crossover,hatchback,luxury"
                    self.profile.limit["size"] = "midsize,large"
                if self.validWord(question, "sports", synonyms):
                    self.profile.limit["category"] = "crossover"
                if self.validWord(question, "work", synonyms):
                    self.profile.limit["category"] = "hybrid,hatchback"
                    self.profile.limit["size"] = "midsize,large"
                if self.validWord(question, "travel", synonyms):
                    self.profile.limit["category"] = "luxury"
                    self.profile.limit["mpg"] = "high"


    def responseIsValid(self, question, response):
        if question == "price":
            return self.obtainPriceRange(question, response)
        else:
            for token, synonyms in response.items():
                #print(token)
                #if token in self.answerBank[question]:
                #    return True
                #print(synonyms)
                #print("vs")
                #print(self.answerBank[question])

                for answer in self.answerBank[question]:
                    if self.validWord(question, answer, synonyms):
                        return True


        return False

    def nextQuestion(self, response, question):
        # give the next question
        return self.decisionTree(response, question)

        # print("Min price: ", self.profile.min_price)
        # print("Max price: ", self.profile.max_price)
        # print("Priorities: ", self.profile.priorities)
        # print("Limits: ", self.profile.limit)

        # TODO: properly recommend the next question based on the response and the question answered
        # A.K.A Do the Decision tree instead of printing all questions below

        # for q in self.answerBank:
        # if not self.answered[self.questionToKey[q]]:
        # return q

    def save_info(self, question, response):
        # TODO: use sentiment analysis to determine the priority of the response
        print()

    def askQuestions(self):
        print("\n\n\t ****** DEBUG MODE ****** \n\nWelcome to the car recommendation system!")
        print("Please answer the following questions to help us find the best car for you!")
        question = ""
        response = ""

        # question following decision tree flow chart
        while not self.end_reached:
            # ask proper question
            question = self.nextQuestion(response, question)

            if question is not None:
                print("OUT:", self.questions[question])
                response = prep.preProcessing(input("IN: "))
                print(response)

                # check if response is valid
                while not self.responseIsValid(question, response):
                    print("OUT: Sorry i didn't understand that, please try again")
                    print("")
                    print("OUT:", self.questions[question])
                    response = prep.preProcessing(input("IN: "))
                    print(response)

                self.saveAnswer(question, response)
                print("saved")
                print(self.profile.limit)

        # output car that fits the most
        print("OUT: Here is the car that fits you the best: ")
        print(self.profile.limit)
        results = self.dao.searchCarsByPriority(self.profile.limit)
        if len(results) == 0:
            print("OUT: Sorry we couldn't find a car that fits you, please try again")
            return 0
        else:
            print("OUT: Based on your answers, we recommend the following cars:")

        r = (len(results) if len(results) < 10 else 10)
        for i in range(0, r):
            # print(results[i])
            print(f"{i + 1}). The {results[i][self.dao.columns.index('year')]} {results[i][self.dao.columns.index('make')]} {results[i][self.dao.columns.index('model')]} with {results[i][self.dao.columns.index('transmission')]} transmission, its"
                  f" a {results[i][self.dao.columns.index('size')]} {' '.join(results[i][self.dao.columns.index('category')].split(';'))} {results[i][self.dao.columns.index('style')]} for ${results[i][self.dao.columns.index('price')]} with a score of {results[i][self.dao.columns.index('score_x')]} ")

        print("\nOUT: Which one interests you the most?\n")
        response = input("IN: ")
        while (not(response.isdigit()) or  int(response) > r):
            if not(response.isdigit()):
                print("OUT: Sorry i didn't understand that, please try again")
            else:
                print("OUT: Sorry that is not an option, please try again")

        #show info about car
        self.dao.showCarInfo(results[int(response)-1][self.dao.columns.index('index')])
    def decisionTree(self, response, question):
        if question == "":
            return "price"
        if question == "price":
            return "priority"
        for word,synonyms in response.items():

            if question == "priority":
                if "rely" in synonyms:
                    return "terrain"
                elif "efficy" in synonyms:
                    return "terrain"
                elif "fast" in synonyms:
                    return "environment"
                elif "fun" in synonyms:
                    return "environment"
                elif "spac" in synonyms:
                    return "area"
                elif "us" in synonyms:
                    return "use"
                elif "safety" in synonyms:
                    return "use"

            elif question == "use":
                return "environment"

            elif question == "environment":
                if "efficy" in synonyms or "friend" in synonyms or "eco" in synonyms or "bal" in synonyms:
                    return "terrain"
                elif "fast" in synonyms:
                    return "circuit"

            elif question == "terrain":
                return "area"

            elif question == "circuit":
                self.end_reached = True
                return None

            elif question == "area":
                self.end_reached = True
                return None

            else:
                return None
