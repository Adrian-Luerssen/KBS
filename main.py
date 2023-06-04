# import Recommendation as rec
#
# import PreProcessing as pre
#
#
# q = rec.questions(debug=True)
# q.askQuestions()

from flask import Flask
from flask import request
from flask import Response
from google_images_search import GoogleImagesSearch
import requests
import config
import TelegramBot as telegramBot

app = Flask(__name__)
gis = GoogleImagesSearch(config.GOOGLE_KEY, config.GOOGLE_CX)

import PreProcessing as pre
import Recommendation as rec

#q = rec.questions(debug=False)
#q.askQuestions()


#def updateSearchParams(search_target):
#    _search_params['q'] = search_target


# gis.search(search_params=_search_params)
# print("total pics: ", len(gis.results()))


chatManager = telegramBot.ChatManager(debug=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
        chat_id, txt, name, username = chatManager.parseMessage(msg)
        txt = txt.lower()
        #print("FLUSHING")
        #return Response('ok', status=200)
        if txt in {"hi", "hello", "howdy", "hola", "hey"}:
            # tel_send_message(chat_id, "Hello, world!")
            chatManager.sendImage(config.BOT_LOGO, chat_id)
        elif txt == "image":
            chatManager.sendImage(gis.results()[0].url, chat_id)
        elif txt == "/start":
            chatManager.sendMessage(chat_id, "Hello! I'm the Car Recommender Bot!\n\nPlease answer the following questions to help me find the best car for you!")
            chatManager.gotMessage(chat_id, txt, name, username)
        else:
            chatManager.gotMessage(chat_id, txt)

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>" \
               "<h2>This is a Car Recommendation Telegram bot, if you want to use it " \
               "<a href='https://t.me/car_recommender_bot'>click here.</a></h2>" \
               "<img src='https://lumiere-a.akamaihd.net/v1/images/open-uri20150422-20810-uyvay5_788a7d61.jpeg'/>"


if __name__ == '__main__':
    app.run(threaded=True, port=5002)
