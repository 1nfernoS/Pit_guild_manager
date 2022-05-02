from traceback import format_exc
from json import JSONDecodeError

import requests
from flask import Flask, request, json, make_response

import settings

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://77f02ebae74b4a12a98f7a9596b6f03d@o1228267.ingest.sentry.io/6373973",
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>HWHelper Bot, use VK bot instead this</h2>'


@app.route('/', methods=['POST'])
def handler():
    try:
        r = request.data
        data = json.loads(r)
    except JSONDecodeError:
        return make_response("No data provided", 400)

    # confirmation don't send any other data
    try:
        type_msg = data['type']
    except KeyError:
        return make_response("Wrong key data provided", 400)
    except TypeError:
        return make_response("Wrong data provided", 402)

    if type_msg == 'confirmation':
        return make_response(settings.confirmation_token, 200)

    try:
        obj_msg = data['object']
        group_id = data['group_id']
    except KeyError:
        return make_response("Wrong data provided", 400)

    if group_id != int(settings.group_id):
        return make_response("Error: only bot have access", 403)

    if type_msg == 'message_new':
        data_msg = obj_msg['message']
        message(data_msg)

    return make_response('ok', 200)


@app.route('/check/')
def check():
    try:
        r = requests.get('https://vip3.activeusers.ru/app.php?act=user&auth_key=5153d58b92d71bda47f1dac05afc187a&viewer_id=158154503&group_id=182985865&api_id=7055214')
    except:
        return '<h2>No Access to profile</h2><h4>' + format_exc(-2) + '</h4>'
    if r.status_code == 200:
        return '<h2>Access granted</h2>'


def message(msg):
    import vk
    api = vk.API(vk.Session(), v='5.126')

    text = str(msg['text'])
    chat = int(msg['peer_id'])
    user = int(msg['from_id'])
    if text.startswith('/'):
        if user == settings.creator_id:
            if text == '/check':
                try:
                    msg = 'Test fine'
                    api.messages.send(access_token=settings.user_token,
                                      peer_id=str(chat),
                                      random_id=0,
                                      message=str(msg))
                except:
                    msg = 'Error occured, check logs'
                    api.messages.send(access_token=settings.group_token,
                                      peer_id=str(chat),
                                      random_id=0,
                                      message=str(msg))
            if text == '/ping':
                msg = 'All worked out Fine'
                api.messages.send(access_token=settings.group_token,
                                  peer_id=str(chat),
                                  random_id=0,
                                  message=str(msg))
    return


@app.errorhandler(500)
def internal_error(*args):
    """
    Send in errors chat info about exception and continue working
    Something like except: pass
    :return: response('ok', 200)
    """
    # vk_api.send(settings.errors_chat, str(format_exc(-5)))
    return make_response('ok', 200)


if __name__ == '__main__':
    app.run()
