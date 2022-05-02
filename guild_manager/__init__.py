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


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


@app.route('/')
def index():
    return '<h2>HWHelper Bot, use VK bot instead this</h2>'


@app.route('/logs')
def check_logs():
    try:
        with open('log.txt', 'r') as f:
            s = ''
            for i in f.readlines():
                s += i
            return s
    except FileNotFoundError:
        return 'No logs for now'


@app.route('/', methods=['POST'])
def handler():
    try:
        r = request.data
        # print(r)
        data = json.loads(r)
    except JSONDecodeError:
        return make_response("No data provided", 400)
    try:
        with open('log.txt', 'a') as f:
            f.write(str(type(data)))
            f.write(': ')
            f.write(str(data))
            f.write('\n')
    except FileNotFoundError:
        with open('log.txt', 'x') as f:
            f.write(str(type(data)))
            f.write(': ')
            f.write(str(data))
            f.write('\n')

        # confirmation don't send any other data
    try:
        type_msg = data['type']
    except KeyError:
        return make_response("Wrong key data provided", 400)
    except TypeError:
        # print(type(data), data, sep='\t - \t')
        # print(format_exc(-2))
        return make_response("Wrong data provided", 402)

    if type_msg == 'confirmation':
        return make_response(settings.confirmation_token, 200)

    try:
        obj_msg = data['object']
        group_id = data['group_id']
    except KeyError:
        return make_response("Wrong data provided", 400)

    if group_id != settings.group_id:
        return make_response("Error: only bot have access", 403)

    if type_msg == 'message_new':
        data_msg = obj_msg['message']
        # print(20 * '=' + '\ngoing to message\n' + 20 * '=')
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
