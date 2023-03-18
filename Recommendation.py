import PreProcessing as prep
import Processing as pro
import re


class profile:
    min_price = 0
    max_price = 0
    priorities = []
    limit = {}

    def __int__(self):
        # define priorities
        self.min_price = 0
        self.max_price = 0
        self.priorities = []  # the priorities from the decision tree will move
        self.limit = {}  # the limitations of the recomendations, key is the limited factor : values are what we will be limiting by


class questions:
    def __init__(self):
        self.profile = profile()
        self.questionToKey = {}
        self.questions = {}
        self.answered = {}
        self.questions["what is your price range?"] = []
        self.questionToKey["what is your price range?"] = "price"
        self.answered["price"] = False

        self.questions["What is your priority when buying a car?"] = ["reliability", "efficiency", "fun",
                                                                      "space", "use", "class", "speed"]
        self.questionToKey["What is your priority when buying a car?"] = "priority"
        self.answered["priority"] = False

        self.questions["Do you have concerns about the environment?"] = ["yes", "no"]
        self.questionToKey["Do you have concerns about the environment?"] = "environment"
        self.answered["environment"] = False

        self.questions["What type of terrain do you drive on?"] = ["city", "highway", "off-road"]
        self.questionToKey["What type of terrain do you drive on?"] = "terrain"
        self.answered["terrain"] = False

        self.questions["Will you take the car to a circuit?"] = ["yes", "no"]
        self.questionToKey["Will you take the car to a circuit?"] = "circuit"
        self.answered["circuit"] = False

        self.questions["Where do you live?"] = ["city", "suburb", "rural"]
        self.questionToKey["Where do you live?"] = "live"
        self.answered["live"] = False

    def obtainPriceRange(self, question, response):
        lst = []
        for tok in response:
            if re.search("[0-9]", tok):
                lst.append(tok)

        if (len(lst)) == 0:
            self.answered[self.questionToKey[question]] = False
            return False
        else:
            self.answered[self.questionToKey[question]] = True
            if (len(lst) == 1):
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
        self.answered[self.questionToKey[question]] = True
        for tok in response:
            if tok in self.questions[question]:

                if question == "What is your priority when buying a car?":
                    self.profile.priorities.append(tok)
                else:
                    if self.questionToKey[question] not in self.profile.limit:
                        self.profile.limit[self.questionToKey[question]] = []
                    self.profile.limit[self.questionToKey[question]].append(tok)

    def response_is_valid(self, question, response):
        if question == "what is your price range?":
            return self.obtainPriceRange(question, response)

        for tok in response:
            if tok in self.questions[question]:
                return True
        return False

    def nextQuestion(self, response, question):
        # give the next question
        if question == "":
            return "what is your price range?"

        if self.response_is_valid(question, response):
            self.getResponse(question, response)
        else:
            print("OUT: Sorry i didn't understand that, please try again")
            return question

        print("Min price: ", self.profile.min_price)
        print("Max price: ", self.profile.max_price)
        print("Priorities: ", self.profile.priorities)
        print("Limits: ", self.profile.limit)

        # TODO: properly recommend the next question based on the response and the question answered
        # A.K.A Do the Decision tree instead of printing all questions below

        for q in self.questions:
            if not self.answered[self.questionToKey[q]]:
                return q

    def save_info(self, question, response):
        # TODO: use sentiment analysis to determine the priority of the response
        print()

    def ask_questions(self):
        print("Welcome to the car recommendation system!")
        print("Please answer the following questions to help us find the best car for you!")
        question = ""
        response = ""
        # go through all the questions untill all are answered
        while not all(self.answered.values()):
            # get the next question
            question = self.nextQuestion(response, question)
            if question is not None:
                print("\nOUT: " + question)
                response = prep.preProcessing(input("IN: "))

        # TODO Recommend system


q = questions()
q.ask_questions()
