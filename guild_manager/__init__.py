from traceback import format_exc
from json import JSONDecodeError

import requests
from flask import Flask, request, json, make_response

import settings

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>HWHelper Bot, use VK bot instead this</h2>'


@app.route('/', methods=['POST'])
def handler():
    """
    Start point for pre-processing request from vk
    :return: response('ok', 200) / confirmation token
    """
    try:
        r = request.data
        data = json.loads(str(r))
    except JSONDecodeError:
        return make_response("No data provided", 400)

    print(r)

    # confirmation don't send any other data
    try:
        type_msg = data['type']
        group_id = data['group_id']
    except KeyError:
        return make_response("Wrong data provided", 400)
    except TypeError:
        return make_response("Wrong data provided", 400)

    if type_msg == 'confirmation' and group_id == settings.group_id:
        return settings.confirmation_token

    try:
        obj_msg = data['object']
        group_id = data['group_id']
    except KeyError:
        return make_response("Wrong data provided", 400)

    if group_id != settings.group_id:
        return make_response("Error: only bot have access", 403)

    if type_msg == 'message_new':
        data_msg = obj_msg['message']
        check()
        # message(data_msg)

    return make_response('ok', 200)


@app.route('/check/')
def check():
    try:
        r = requests.get('https://vip3.activeusers.ru/app.php?act=user&auth_key=5153d58b92d71bda47f1dac05afc187a&viewer_id=158154503&group_id=182985865&api_id=7055214')
    except:
        return '<h2>No Access to profile</h2><h4>' + format_exc(-2) + '</h4>'
    if r.status_code == 200:
        return '<h2>Access granted</h2>'


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
