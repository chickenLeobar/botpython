from collections import deque

from flask import Flask, request

from messenger import Messenger

from bot.initialize import chat_bot

import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

from utils import resolver_payload, env

ACCESS_TOKEN = env('ACCESS_TOKEN', default=None)
VERIFY_TOKEN = env("VERIFY_TOKEN", default=None)

bot_messenge = Messenger(ACCESS_TOKEN)

app = Flask(__name__)

app.debug = True


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':

        logging.warning("hello i am working , GET")
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        else:
            return "Invalid verification token"
    if request.method == 'POST':
        output = request.get_json(force=True)
        bot_messenge.handle(output)

        return "Success"


if __name__ == "__main__":
    app.run()

# while True:
#     try:
#         user_input = input()
#
#         bot_response = chat_bot.get_response(user_input)
#
#         print(bot_response)
#
#     # Press ctrl-c or ctrl-d on the keyboard to exit
#     except (KeyboardInterrupt, EOFError, SystemExit):
#         break
