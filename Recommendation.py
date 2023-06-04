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
    def __init__(self, debug=False, UserChat=None):
        self.UserChat = UserChat
        self.results = None
        self.profile = profile()
        self.debug = debug
        self.dao = DAO.DAO("data/data.csv")

        self.question = ""
        self.response = {}

        for parameter in self.dao.columns:
            self.profile.limit[parameter] = "any"

        self.questionToKey = {}
        self.questions = {}
        self.answerBank = {}
        self.answered = {}
        self.end_reached = False
        self.mpg = ""

        self.questions["price"] = "What is your price range? 💰"
        self.answerBank["price"] = []
        self.answered["price"] = False

        self.questions["priority"] = "What is your priority when buying a car?"
        self.answerBank["priority"] = ["reliability", "efficiency", "fun",
                                       "space", "use", "fast", "speed", "safety"]
        self.answered["priority"] = False

        self.questions["environment"] = "Do you prefer a faster car 🏎️ or an eco-friendly one 🌱?  "
        self.answerBank["environment"] = ["fast", "eco", "friendly", "efficient", "balanced"]
        self.answered["environment"] = False

        self.questions["terrain"] = "What type of terrain do you drive on? 🏙️⛰️"
        self.answerBank["terrain"] = ["city", "highway", "offroad"]
        self.answered["terrain"] = False

        self.questions["circuit"] = "Will you take the car to a circuit? 🏎️ 🏁"
        self.answerBank["circuit"] = ["yes", "no"]
        self.answered["circuit"] = False

        self.questions["area"] = "Where do you live? 🏘️🏢🏡"
        self.answerBank["area"] = ["urban", "suburb",
                                   "rural"]  # can assume suburb takes highway often and rural takes off-road often
        self.answered["area"] = False

        self.questions["use"] = "What are you going to use the car for?"
        self.answerBank["use"] = ["groceries", "commute", "family", "sports", "work", "travel"]
        # can assume groceries and commute are city and suburb, family is suburb, sports is off-road, luxury is highway, work is city, travel is highway
        self.answered["use"] = False


        for key in self.answerBank:
            a = self.answerBank[key]
            self.answerBank[key] = {}
            for i in range(len(a)):
                new = prep.preProcessing(a[i])
                self.answerBank[key][list(new.keys())[0]] = list(new.values())[0]

        if self.debug: print(self.answerBank)

    def validWord(self, question, known_word, input):
        known_synonyms = self.answerBank[question][known_word]
        # Check if any of the input synonyms coincide with the known synonyms
        common_synonyms = [value for value in known_synonyms if value in input]
        # if self.debug:print(input)
        # if self.debug:print(known_synonyms)
        if common_synonyms:
            # if self.debug:print( f"The input word is a synonym of the known word '{known_word}' through the following synonyms: {common_synonyms}")
            return True

        return False

    def obtainPriceRange(self, question, response):
        lst = []
        # if self.debug:print(response)
        # join thousand or k to the number
        # get all tokens as list
        response = list(response.keys())
        pos = 0
        while pos < len(response) - 1:
            # if self.debug:print(response)
            if re.search("^[0-9]*$", response[pos]):
                if "thousand" == response[pos + 1] or "k" == response[pos + 1]:
                    response[pos] = response[pos] + "k"
                    response = response[:pos + 1] + response[pos + 2:]
                elif "m" == response[pos + 1] or "million" == response[pos + 1]:
                    response[pos] = response[pos] + "m"
                    response = response[:pos + 1] + response[pos + 2:]
            pos += 1

        if self.debug: print(response)
        for tok in response:
            if re.search("[0-9]k", tok) or re.search("[0-9]thousand", tok):
                lst.append(float(tok.replace("k", "").replace("thousand", "")) * 1000)
            elif re.search("[0-9]m", tok) or re.search("[0-9]million", tok):
                lst.append(float(tok.replace("mil", "").replace("m", "")) * 1000000)
            elif re.search("[0-9]", tok):
                lst.append(float(tok))
        if self.debug: print(lst)
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
        if self.debug: print(response)
        for token in response:
            if token in self.answerBank[question]:
                if question == "priority":
                    self.profile.priorities.append(token)
                else:
                    if question not in self.profile.limit:
                        self.profile.limit[question] = []
                    self.profile.limit[question].append(
                        token)  # TODO: change to set values, if cares about fuel -> electric or low mpg, choose

    def saveAnswer(self):

        if self.question == "info":
            #self.dao.saveCarInfo(self.results[int(self.response) - 1][self.dao.columns.index('index')], self.profile.limit)
            return
        elif self.question == "end":
            self.dao.saveCarInfo(self.results[int(list(self.response.keys())[0]) - 1][self.dao.columns.index('index')],
                                 self.profile.limit)
            return
        elif self.question == "price":
            self.profile.limit["price"] = str(self.profile.max_price)
            self.profile.limit["price_min"] = str(self.profile.min_price)
            return

        for word, synonyms in self.response.items():
            if self.debug: print(synonyms)
            if self.question == "priority":
                # if self.debug:print(self.validWord(question, "", synonyms))
                if self.validWord(self.question, "spac", synonyms):
                    self.profile.limit["doors"] = "4"
                    self.profile.limit["size"] = "large,midsize"
                if self.validWord(self.question, "efficy", synonyms):
                    self.mpg = "high"
                if self.validWord(self.question, "fun", synonyms):
                    self.profile.limit["hp"] = "high"
                if self.validWord(self.question, "fast", synonyms) or self.validWord(self.question, "spee",
                                                                                     synonyms):
                    self.profile.limit["hp"] = "high"
                    self.profile.limit["category"] = "exotic,factory tuner,performance,high-performance"
                if self.validWord(self.question, "saf", synonyms):
                    self.profile.limit["year"] = "2012"
                if self.validWord(self.question, "rely", synonyms):
                    self.profile.limit["year"] = "2014"
                    self.profile.limit["transmission"] = "automatic"
            elif self.question == "environment":
                if self.validWord(self.question, "fast", synonyms):
                    self.profile.limit["hp"] = "high"
                    self.profile.limit["category"] = "exotic,factory tuner,performance"
                if self.validWord(self.question, "eco", synonyms) or self.validWord(self.question, "friend",
                                                                                    synonyms) or self.validWord(
                    self.question, "efficy", synonyms):
                    self.profile.limit["mpg"] = "high"
                    self.profile.limit["fuel_type"] = "electric"
                if self.validWord(self.question, "bal", synonyms):
                    self.profile.limit["hp"] = "high"
            elif self.question == "terrain":
                if self.validWord(self.question, "city", synonyms):
                    self.profile.limit["city_mpg"] = "high"
                if self.validWord(self.question, "highway", synonyms):
                    self.profile.limit["highway_mpg"] = "high"
                if self.validWord(self.question, "offroad", synonyms):
                    self.profile.limit["driven_wheels"] = "all wheel drive,four wheel drive"
            elif self.question == "circuit":
                if self.validWord(self.question, "ye", synonyms):
                    self.profile.limit["cylinders"] = "high"
                    # self.profile.limit["transmission"] = "manual"
            elif self.question == "area":
                if self.validWord(self.question, "urb", synonyms):
                    self.profile.limit["category"] = "hybrid,luxury,hatchback"
                    if self.mpg == "high":
                        self.profile.limit["city_mpg"] = "high"
                if self.validWord(self.question, "suburb", synonyms):
                    self.profile.limit["category"] = "crossover,hatchback,luxury"
                    if self.mpg == "high":
                        self.profile.limit["highway_mpg"] = "high"
                if self.validWord(self.question, "rur", synonyms):
                    self.profile.limit["category"] = "crossover"
                    if self.mpg == "high":
                        self.profile.limit["highway_mpg"] = "high"
            elif self.question == "use":
                if self.validWord(self.question, "grocery", synonyms):
                    self.profile.limit["category"] = "hybrid,hatchback"
                    self.profile.limit["size"] = "midsize"
                if self.validWord(self.question, "commut", synonyms):
                    self.profile.limit["category"] = "hybrid,luxury,hatchback"
                if self.validWord(self.question, "famy", synonyms):
                    self.profile.limit["category"] = "crossover,hatchback,luxury"
                    self.profile.limit["size"] = "midsize,large"
                if self.validWord(self.question, "sports", synonyms):
                    self.profile.limit["category"] = "crossover"
                if self.validWord(self.question, "work", synonyms):
                    self.profile.limit["category"] = "hybrid,hatchback"
                    self.profile.limit["size"] = "midsize,large"
                if self.validWord(self.question, "travel", synonyms):
                    self.profile.limit["category"] = "luxury"
                    self.profile.limit["mpg"] = "high"

    def responseIsValid(self, question, response) -> bool:
        if question == "":
            return False
        elif question == "info":
            return True
        elif question == "end":
            print(list(response.keys())[0])
            if int(list(self.response.keys())[0]) > (len(self.results) if len(self.results) < 8 else 8):
                return False
            if not (list(self.response.keys())[0].isdigit()):
                return False
            return True
        elif question == "price":
            return self.obtainPriceRange(question, response)
        else:
            for token, synonyms in response.items():
                # if self.debug:print(token)
                # if token in self.answerBank[question]:
                #    return True
                # if self.debug:print(synonyms)
                # if self.debug:print("vs")
                # if self.debug:print(self.answerBank[question])
                if self.debug: print("| question: ", question)
                #if self.debug:print("| answerBank", self.answerBank[question])
                if self.debug:print("| response: ", response)
                #if self.debug:print("| token: ", token)
                if self.debug:print("| synonyms: ", synonyms)
                for answer in self.answerBank[question]:
                    if self.validWord(question, answer, synonyms):
                        return True

        return False

    def nextQuestion(self, response, question):
        # give the next question
        return self.decisionTree(response, question)

        # if self.debug:print("Min price: ", self.profile.min_price)
        # if self.debug:print("Max price: ", self.profile.max_price)
        # if self.debug:print("Priorities: ", self.profile.priorities)
        # if self.debug:print("Limits: ", self.profile.limit)

        # TODO: properly recommend the next question based on the response and the question answered
        # A.K.A Do the Decision tree instead of if self.debug:printing all questions below

        # for q in self.answerBank:
        # if not self.answered[self.questionToKey[q]]:
        # return q

    def save_info(self, question, response):
        # TODO: use sentiment analysis to determine the priority of the response
        if self.debug: print()

    def prepare(self):
        self.question = ""
        self.response = ""

    def ask(self) -> str:
        self.question = self.nextQuestion(self.response, self.question)

        if self.question == "end":
            return self.getResult()
        if self.question == "info":
            if self.UserChat is not None:
                self.UserChat.setMakeModel(self.results[int(list(self.response.keys())[0]) - 1][self.dao.columns.index('make')] + " " +
                self.results[int(list(self.response.keys())[0]) - 1][self.dao.columns.index('model')])
            return self.dao.showCarInfo(self.results[int(list(self.response.keys())[0]) - 1][self.dao.columns.index('index')])
        if self.question == "bye":
            return ""
        if self.question is not None:
            return self.questions[self.question]
            # print("OUT:", self.questions[self.question])

    def gotAnswerIsValid(self, answer) -> bool:
        # self.response = prep.preProcessing(input("IN: "))
        self.response = prep.preProcessing(answer)
        if self.debug: print("prepd: ", self.response)
        return self.responseIsValid(self.question, self.response)

        # print("OUT: Sorry I didn't understand that, please try again")
        # print("")
        # print("OUT:", self.questions[self.question])
        # self.response = prep.preProcessing(input("IN: "))
        # if self.debug: print(self.response)

    def getResult(self):
        self.results = self.dao.searchCarsByPriority(self.profile.limit)
        if len(self.results) == 0:
            return None
        else:
            r = (len(self.results) if len(self.results) < 8 else 8)
            recommended_cars = "Based on your answers, I think you would like the following cars:\n\n"
            for i in range(0, r):
                print("results: ", self.results[i])
                print("" + self.results[i][self.dao.columns.index('category')])
                #print(
                #    f"{i + 1}). The {results[i][self.dao.columns.index('year')]} {results[i][self.dao.columns.index('make')]} {results[i][self.dao.columns.index('model')]} with {results[i][self.dao.columns.index('transmission')]} transmission, its"
                #    f" a {results[i][self.dao.columns.index('size')]} {aux.join(results[i][self.dao.columns.index('category')].split(';'))} {results[i][self.dao.columns.index('style')]} for ${results[i][self.dao.columns.index('price')]}"
                #    #f" with a score of {results[i][self.dao.columns.index('score_x')]} "
                # )
                formatted_car_info = "{0}). The {1} {2} {3} with {4} transmission, it's a {5} {6} {7} for ${8}\n\n".format(
                    i + 1,
                    self.results[i][self.dao.columns.index('year')],
                    self.results[i][self.dao.columns.index('make')],
                    self.results[i][self.dao.columns.index('model')],
                    self.results[i][self.dao.columns.index('transmission')],
                    self.results[i][self.dao.columns.index('size')],
                    " ".join(self.results[i][self.dao.columns.index('category')].split(';')),
                    self.results[i][self.dao.columns.index('style')],
                    self.results[i][self.dao.columns.index('price')]
                )
                recommended_cars += formatted_car_info

            return recommended_cars + "\nWhich one interests you the most? Please type just the number 🙏"

    def askQuestions(self):
        if self.debug: print("\n\n\t ****** DEBUG MODE ****** \n\n")
        print(
            "Welcome to the car recommendation system!\n\nPlease answer the following questions to help us find the best car for you!")
        self.question = ""
        self.response = ""

        # question following decision tree flow chart
        while not self.end_reached:
            # ask proper question
            self.question = self.nextQuestion(self.response, self.question)

            if self.question is not None:
                print("OUT:", self.questions[self.question])
                self.response = prep.preProcessing(input("IN: "))
                if self.debug: print(self.response)

                # check if response is valid
                while not self.responseIsValid(self.question, self.response):
                    print("OUT: Sorry, I didn't understand that. Please try rephrasing your answer")
                    print("")
                    print("OUT:", self.questions[self.question])
                    self.response = prep.preProcessing(input("IN: "))
                    if self.debug: print(self.response)

                self.saveAnswer()  # (answer, question)
                if self.debug: print("saved")
                if self.debug: print(self.profile.limit)

        # output car that fits the most
        # print("OUT: Here is the car that fits you the best: ")
        if self.debug: print(self.profile.limit)
        self.results = self.dao.searchCarsByPriority(self.profile.limit)
        if len(self.results) == 0:
            print("OUT: Sorry we couldn't find a car that fits you, please try again")
            return 0
        else:
            print("OUT: Based on your answers, we recommend the following cars:")

        r = (len(self.results) if len(self.results) < 10 else 10)
        recommended_cars = "Based on your answers, we recommend the following cars:\n"
        for i in range(0, r):
            # print(results[i])
            #print("category: ", "" + results[i][self.dao.columns.index('category')])
            #print("category try: ", results[i][self.dao.columns.index('category')] )
            # print(
            #    f"{i + 1}). The {results[i][self.dao.columns.index('year')]} {results[i][self.dao.columns.index('make')]} {results[i][self.dao.columns.index('model')]} with {results[i][self.dao.columns.index('transmission')]} transmission, its"
            #    f" a {results[i][self.dao.columns.index('size')]} {' '.join(results[i][self.dao.columns.index('category')].split(';'))} {results[i][self.dao.columns.index('style')]} for ${results[i][self.dao.columns.index('price')]}"
            #    #f" with a score of {results[i][self.dao.columns.index('score_x')]} "
            # )
            formatted_car_info = "{0}). The {1} {2} {3} with {4} transmission, it's a {5} {6} {7} for ${8}\n".format(
                i + 1,
                self.results[i][self.dao.columns.index('year')],
                self.results[i][self.dao.columns.index('make')],
                self.results[i][self.dao.columns.index('model')],
                self.results[i][self.dao.columns.index('transmission')],
                self.results[i][self.dao.columns.index('size')],
                ' '.join(self.results[i][self.dao.columns.index('category')].split(';')),
                self.results[i][self.dao.columns.index('style')],
                self.results[i][self.dao.columns.index('price')]
            )
            recommended_cars += formatted_car_info

        #print(recommended_cars)
        # return recommended_cars
        print("\nOUT: Which one interests you the most?\n")
        self.response = input("IN: ")
        while not ((self.response.isdigit()) and not (int(self.response) > r)):
            if not (self.response.isdigit()):
                print("OUT: Sorry i didn't understand that, please try again")
            else:
                print("OUT: Sorry that is not an option, please try again")

        # show info about car
        self.dao.showCarInfo(self.results[int(self.response) - 1][self.dao.columns.index('index')])
        self.dao.saveCarInfo(self.results[int(self.response) - 1][self.dao.columns.index('index')], self.profile.limit)

    def decisionTree(self, response, question):
        if question == "":
            return "price"
        if question == "price":
            return "priority"
        for word, synonyms in response.items():

            if question == "priority":
                if self.validWord(question, "rely", synonyms):
                    return "terrain"
                elif self.validWord(question, "efficy", synonyms):
                    return "terrain"
                elif self.validWord(question, "fast", synonyms) or self.validWord(question, "spee", synonyms):
                    return "environment"
                elif self.validWord(question, "fun", synonyms):
                    return "environment"
                elif self.validWord(question, "spac", synonyms):
                    return "area"
                elif self.validWord(question, "us", synonyms):
                    return "use"
                elif self.validWord(question, "rely", synonyms):
                    return "use"

            elif question == "use":
                return "environment"

            elif question == "environment":
                if self.validWord(question, "eco", synonyms) or self.validWord(question, "friend",
                                                                               synonyms) or self.validWord(question,
                                                                                                           "efficy",
                                                                                                           synonyms):
                    return "terrain"
                elif self.validWord(question, "fast", synonyms):
                    return "circuit"

            elif question == "terrain":
                return "area"

            elif question == "circuit":
                self.end_reached = True
                return "end"

            elif question == "area":
                self.end_reached = True
                return "end"

            elif question == "end":
                return "info"

            elif question == "info":
                return None

            else:
                return None
