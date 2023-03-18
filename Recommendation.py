import PreProcessing as prep
import Processing as pro
import re

class profile:
    min_price = 0
    max_price = 0
    priorities = []

    def __int__(self):
        # define priorities
        self.min_price = 0
        self.max_price = 0
        self.priorities = []            #the priorities from the decision tree will move
        self.limit = []                 #the limitations of the recomendations


class questions:
    def __init__(self):
        self.profile = profile()
        self.questions = {}
        self.answered = {}
        self.questions["what is your price range?"] = []
        self.answered["what is your price range?"] = False
        self.questions["What is your priority when buying a car?"] = ["reliability", "efficiency", "fun",
                                                                      "space", "use", "class", "speed"]
        self.answered["What is your priority when buying a car?"] = False
        self.questions["Do you have concerns about the environment?"] = ["yes", "no"]
        self.answered["Do you have concerns about the environment?"] = False
        self.questions["What type of terrain do you drive on?"] = ["city", "highway", "off-road"]
        self.answered["What type of terrain do you drive on?"] = False
        self.questions["Will you take the car to a circuit?"] = ["yes", "no"]
        self.answered["Will you take the car to a circuit?"] = False
        self.questions["Where do you live?"] = ["city", "suburb", "rural"]
        self.answered["Where do you live?"] = False


    def obtainPriceRange(self, question,response):
        lst = []
        for tok in response:
            if re.search("[0-9]", tok):
                lst.append(tok)

        if (len(lst)) == 0:
            self.answered[question] = False
            return False
        else: 
            self.answered[question] = True
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
        self.answered[question] = True
        for tok in response:
            if tok in self.questions[question]:
                if questions == "What is your priority when buying a car?":
                    self.profile.priorities.append(tok)
                else:
                    self.profile.limit.append(tok)

    def response_is_valid(self, question,response):
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

        if self.response_is_valid(question,response):
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
            if not self.answered[q]:
                return q

    def save_info(self,question, response):
        #TODO: use sentiment analysis to determine the priority of the response
        print()

    def ask_questions(self):
        print("Welcome to the car recommendation system!")
        print("Please answer the following questions to help us find the best car for you!")
        question = ""
        response = ""
        #go through all the questions untill all are answered
        while not all(self.answered.values()):
            # get the next question
            question = self.nextQuestion(response, question)
            if question is not None:
                print("\nOUT: "+question)
            response = prep.preProcessing(input("IN: "))
        
        #TODO Recommend system


        

q = questions()
q.ask_questions()