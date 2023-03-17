import PreProcessing as prep

class profile:
    def __int__(self):
        # define priorities
        self.min_price = 0
        self.max_price = 0
        self.priority = {}


class questions:
    def __init__(self):
        self.questions = {}
        self.answered = {}
        self.questions["what is your price range?"] = []
        self.answered["what is your price range?"] = False
        self.questions["What is your priority when buying a car?"] = ["reliability", "performance", "fuel efficiency",
                                                                      "comfort", "safety", "class", "speed"]
        self.answered["What is your priority when buying a car?"] = False
        self.questions["Do you have concerns about the environment?"] = ["Yes", "No"]
        self.answered["Do you have concerns about the environment?"] = False
        self.questions["What type of terrain do you drive on?"] = ["City", "Highway", "Off-Road"]
        self.answered["What type of terrain do you drive on?"] = False
        self.questions["Will you take the car to a circuit?"] = ["Yes", "No"]
        self.answered["Will you take the car to a circuit?"] = False
        self.questions["Where do you live?"] = ["City", "Suburb", "Rural"]
        self.answered["Where do you live?"] = False

        self.profile = profile()

    def response_is_valid(self, question,response):
        #TODO:
        if question == "what is your price range?":
            return True

        for tok in response:
            if tok in self.questions[question]:
                return True
        return False
    def nextQuestion(self, response, question):
        # give the next question
        # TODO: properly recommend the next question based on the response and the question answered
        if question == "":
            return "what is your price range?"

        if self.response_is_valid(question,response):
            self.answered[question] = True
        else:
            print("OUT: Sorry i didn't understand that, please try again")
            return question


        if not(self.answered["what is your price range?"] and self.answered["What is your priority when buying a car?"]):

            if question == "what is your price range?":
                if self.response_is_valid(question,response):
                    return "What is your priority when buying a car?"
                else:
                    self.answered[question] = True
                    return "what is your price range?"

            if question == "What is your priority when buying a car?":
                if self.response_is_valid(question,response):
                    return "What is your priority when buying a car?"
                else:
                    self.answered[question] = True

        for q in self.questions:
            if not self.answered[q]:
                return q

    def save_info(self,question, response):
        #TODO: save the info to the profile based on the questions response
        print(question + " "+ str(response))
        #TODO: use sentiment analysis to determine the priority of the response
    def ask_questions(self):
        print("Welcome to the car recommendation system!")
        print("Please answer the following questions to help us find the best car for you!")
        question = ""
        response = ""
        #go through all the questions untill all are answered
        while not all(self.answered.values()):
            # get the next question
            question = self.nextQuestion(response, question)
            print("OUT: "+question)
            response = prep.preProcessing(input("IN: "))
            print()

            self.save_info(question, response)

        

q = questions()
q.ask_questions()