from json import JSONDecodeError
from flask import Flask, request, json, make_response

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

import settings
from guild_manager.messages import message

sentry_sdk.init(
    dsn=settings.sentry_url,
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Pit-guild-manager Bot, use VK bot instead this</h2>'


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

    if group_id != settings.group_id:
        # raise Exception(f'{group_id} != {settings.group_id}')
        return make_response("Error: only bot have access", 403)

    if type_msg == 'message_new':
        data_msg = obj_msg['message']
        message(data_msg)

    return make_response('ok', 200)


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


@app.route('/idk/how/do/you/get/there/aboba')
def get_vars():
    return dir(settings)


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
