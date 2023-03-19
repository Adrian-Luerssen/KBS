import PreProcessing as prep
import Processing as pro
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
                                       "space", "use", "speed", "safety"]
        self.answered["priority"] = False

        self.questions["environment"] = "Do you prefer a faster car or an eco-friendly one?"
        self.answerBank["environment"] = ["fast", "eco", "friendly", "efficient", "balanced"]
        self.answered["environment"] = False

        self.questions["terrain"] = "What type of terrain do you drive on?"
        self.answerBank["terrain"] = ["city", "highway", "off-road"]
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
            for i in range(len(self.answerBank[key])):
                self.answerBank[key][i] = prep.preProcessing(self.answerBank[key][i])[0]

        print(self.answerBank)

    def obtainPriceRange(self, question, response):
        lst = []
        # print(response)
        # join thousand or k to the number
        pos = 0
        while pos < len(response) - 1:
            print(response)
            if re.search("^[0-9]*$", response[pos]):
                if "thousand" == response[pos + 1]:
                    response[pos] = response[pos] + "k"
                    response = response[:pos + 1] + response[pos + 2:]
                elif "k" == response[pos + 1]:
                    response[pos] = response[pos] + "k"
                    response = response[:pos + 1] + response[pos + 2:]
            pos += 1

        # print(response)
        for tok in response:
            if re.search("[0-9]k", tok) or re.search("[0-9]thousand", tok):
                lst.append(float(tok.replace("k", "").replace("thousand", "")) * 1000)
            elif re.search("[0-9]", tok):
                lst.append(tok)

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
            self.profile.limit["price"] = self.profile.max_price
            self.profile.limit["min_price"] = self.profile.min_price
        elif question == "priority":
            if "spac" in response:
                self.profile.limit["doors"] = "4"
                self.profile.limit["size"] = "large,midsize"
            if "efficy" in response:
                self.mpg = "high"
            if "fun" in response:
                self.profile.limit["hp"] = "high"
            if "spee" in response:
                self.profile.limit["hp"] = "high"
                self.profile.limit["category"] = "exotic,factory tuner,performance"
            if "saf" in response:
                self.profile.limit["year"] = "2012"
            if "rely" in response:
                self.profile.limit["year"] = "2014"
                self.profile.limit["transmission"] = "automatic"
        elif question == "environment":
            if "fast" in response:
                self.profile.limit["hp"] = "high"
                self.profile.limit["category"] = "exotic,factory tuner,performance"
            if "eco" or "friend" or "efficy" in response:
                self.profile.limit["mpg"] = "high"
            if "balanc" in response:
                self.profile.limit["hp"] = "high"
        elif question == "terrain":
            if "city" in response:
                self.profile.limit["city_mpg"] = "high"
            if "highway" in response:
                self.profile.limit["highway_mpg"] = "high"
            if "off-road" in response:
                self.profile.limit["driven_wheels"] = "all wheel drive,four wheel drive"
        elif question == "circuit":
            if "ye" in response:
                self.profile.limit["cylinders"] = "high"
                self.profile.limit["transmission"] = "manual"
        elif question == "area":
            if "urb" in response:
                self.profile.limit["category"] = "hybrid,luxury,hatchback"
                if self.mpg == "high":
                    self.profile.limit["city_mpg"] = "high"
            if "suburb" in response:
                self.profile.limit["category"] = "crossover,hatchback,luxury"
                if self.mpg == "high":
                    self.profile.limit["highway_mpg"] = "high"
            if "rur" in response:
                self.profile.limit["category"] = "crossover"
                if self.mpg == "high":
                    self.profile.limit["highway_mpg"] = "high"
        elif question == "use":
            if "grocery" in response:
                self.profile.limit["category"] = "hybrid,hatchback"
                self.profile.limit["size"] = "midsize"
            if "commut" in response:
                self.profile.limit["category"] = "hybrid,luxury,hatchback"
            if "famy" in response:
                self.profile.limit["category"] = "crossover,hatchback,luxury"
                self.profile.limit["size"] = "midsize,large"
            if "sports" in response:
                self.profile.limit["category"] = "crossover"
            if "work" in response:
                self.profile.limit["category"] = "hybrid,hatchback"
                self.profile.limit["size"] = "midsize,large"
            if "travel" in response:
                self.profile.limit["category"] = "luxury"
                self.profile.limit["mpg"] = "high"

    def responseIsValid(self, question, response):
        if question == "price":
            return self.obtainPriceRange(question, response)
        else:
            for token in response:
                print(token, self.answerBank[question])
                if token in self.answerBank[question]:
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
        print("Welcome to the car recommendation system!")
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

        # output car that fits the most
        print("OUT: Here is the car that fits you the best: ")
        # TODO: output car that fits the most
        print(self.profile.limit)
        self.dao.searchCarsByParameters(self.profile.limit)

    def decisionTree(self, response, question):
        if question == "":
            return "price"

        elif question == "price":
            return "priority"

        elif question == "priority":
            if "rely" in response:
                return "terrain"
            elif "efficy" in response:
                return "terrain"
            elif "spee" in response:
                return "environment"
            elif "fun" in response:
                return "environment"
            elif "spac" in response:
                return "area"
            elif "us" in response:
                return "use"
            elif "safety" in response:
                return "use"

        elif question == "use":
            return "environment"

        elif question == "environment":
            if "efficy" or "friend" or "eco" or "bal" in response:
                return "terrain"
            elif "fast" in response:
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
