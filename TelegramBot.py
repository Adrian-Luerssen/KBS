import Recommendation as rec
import config
import requests

from google_images_search import GoogleImagesSearch

class ChatManager:

    def __init__(self, debug=False):
        self.chats = {}
        self.debug = debug

    def newChat(self, _id, _username, _name):
        self.chats[_id] = UserChat(_id, _username, _name, self, self.debug)

    def gotMessage(self, _id, text, username=None, name=None):
        if _id not in self.chats:
            self.newChat(_id, username, name)
        if text == "/start":
            self.chats[_id].start()
            self.chats[_id].askQuestion()
        else:
            self.chats[_id].gotAnswer(text)
        # self.chats[_id].askQuestion()

    def sendMessage(self, _id, text):
        url = f'https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage'
        payload = {
            'chat_id': _id,
            'text': text
        }
        print("sending message: ", text if text is not None else "I encountered an error, please /start again 🤝")
        r = requests.post(url, json=payload)
        return r

    def sendImage(self, image_url, chat_id):
        url = f'https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendPhoto'
        payload = {
            'chat_id': chat_id,
            'photo': image_url,
            'caption': ""
        }

        r = requests.post(url, json=payload)
        return r

    def parseMessage(self, message):
        # print("message-->", message)
        try:
            if not message:
                raise ValueError("Empty message")
            username = message['message']['from']['username'] if 'username' in message['message']['from'] else None
            name = message['message']['from']['first_name'] if 'first_name' in message['message']['from'] else "User"
            chat_id = message['message']['chat']['id']
            txt = message['message']['text']
            print("chat_id-->", chat_id)
            print("txt-->", txt)
            print("username-->", username)
            print("name-->", name)

            return chat_id, txt, name, username
        except ValueError as e:
            print("NO text found-->>")
            raise e


class UserChat:

    def __init__(self, _id, _username, _name, _CM, debug=False):
        self.id = _id
        self.username = _username
        self.name = _name
        self.chatManager = _CM
        self.debug = debug
        self.q = None
        self.endReached = False
        self.searchParams = {
            'q': 'error',
            'num': 1,
            'fileType': 'jpg|gif|png',
            'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
            'safe': 'safeUndefined',
            'imgType': 'imgTypeUndefined',
            'imgSize': 'imgSizeUndefined',
            'imgDominantColor': 'imgDominantColorUndefined',
            'imgColorType': 'imgColorTypeUndefined'
        }
        self.start()

    def start(self):
        self.q = rec.questions(self.debug, self)
        self.q.prepare()
        self.endReached = False

    def askQuestion(self):
        print("Getting question..")
        question = self.q.ask()
        print("question: ", question)
        if question != "end":  # still asking
            self.chatManager.sendMessage(self.id, question)
            if self.endReached:
                self.chatManager.sendMessage(self.id, "I hope you like my recommendation!\nIf you'd like to start again, type '/start'")
        else:  # got result, send it
            # self.chatManager.sendMessage(self.id, "Here are your results:")
            result = self.q.getResult()
            if result is not None:
                self.endReached = "info"
                self.chatManager.sendMessage(self.id, result)
                self.chatManager.sendMessage(self.id, "Which one interests you the most?")
            else:
                self.noResult()

    def gotAnswer(self, answer):
        print("got answer: ", answer)

        if "bye" in answer or "exit" in answer or "quit" in answer or "stop" in answer:
            self.chatManager.sendMessage(self.id, "See you!")
            self.start()
        elif self.q.gotAnswerIsValid(answer):
            self.q.saveAnswer()
            self.askQuestion()
        else:
            self.notUnderstood(answer)

    def notUnderstood(self, answer):
        # call the sendMessage function in the ChatManager class
        self.chatManager.sendMessage(self.id, "Sorry, I didn't understand that. Please try rephrasing your answer or starting again by typing '/start'")
        with open('data/ignorance.log', 'a') as f:
            f.write(f"{answer}\n")
            f.close()

    def noResult(self):
        self.chatManager.sendMessage(self.id,
                                     "Sorry, I couldn't find a car that fits your needs. Feel free to try again :)")

    def setMakeModel(self, make_and_model):
        self.searchParams['q'] = make_and_model
        gis = GoogleImagesSearch(config.GOOGLE_KEY, config.GOOGLE_CX)
        gis.search(search_params=self.searchParams)
        self.chatManager.sendImage(gis.results()[0].url, self.id)
        self.endReached = True
