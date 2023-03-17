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
        self.answered["what is your price range?"] = True
        self.questions["What is your priority when buying a car?"] = ["Reliability", "Performance", "Fuel Efficiency",
                                                                      "Comfort", "Safety", "Class", "Speed"]
        self.answered["What is your priority when buying a car?"] = True
        self.questions["Do you have concerns about the environment?"] = ["Yes", "No"]
        self.answered["Do you have concerns about the environment?"] = False
        self.questions["What type of terrain do you drive on?"] = ["City", "Highway", "Off-Road"]
        self.answered["What type of terrain do you drive on?"] = False
        self.questions["Will you take the car to a circuit?"] = ["Yes", "No"]
        self.answered["Will you take the car to a circuit?"] = False
        self.questions["Where do you live?"] = ["City", "Suburb", "Rural"]
        self.answered["Where do you live?"] = False

        self.profile = profile()


    def nextQuestion(self, response, question):
        # give the next question
        # TODO: properly recommend the next question based on the response and the question answered
        for question in self.questions:
            if not self.answered[question]:
                self.answered[question] = True
                print(question)
                return question
    def save_info(self,question, response):
        #TODO: save the info to the profile based on the questions response
        print(question + " "+ str(response))
        #TODO: use sentiment analysis to determine the priority of the response
    def ask_questions(self):
        print("Welcome to the car recommendation system!")
        print("Please answer the following questions to help us find the best car for you!")
        question = "what is your price range?"
        print(question)
        response = prep.preProcessing(input())
        self.save_info(question, response)
        question = "what is your priority when buying a car?"
        print(question)
        response = prep.preProcessing(input())
        self.save_info(question, response)
        question = "What is your priority when buying a car?"

        #go through all the questions untill all are answered
        while not all(self.answered.values()):
            # get the next question
            question = self.nextQuestion(response, question)
            response = prep.preProcessing(input())

            self.save_info(question, response)

        

q = questions()
q.ask_questions()