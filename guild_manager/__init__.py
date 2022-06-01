from json import JSONDecodeError
from flask import request, json, make_response
from flask import Flask

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

import settings
from guild_manager.messages import message
import guild_manager.profile_api as profile
from db.instance import DB


def init_app():
    """Create DB file instance"""
    try:
        with open('db/user_list', 'x') as f:
            f.write(json.dumps(list()))
    except FileExistsError:
        pass
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('settings.Config')  # configure app using the Config class defined in settings.py

    # DB.init_app(app)  # initialise the database for the app
    # DB.create_all(app=app)
    with app.app_context():
        # this import allows us to create the table if it does not exist
        from db.tables import User, Item
        DB.create_all()

        #  Other stuff if needed
        #  from src.users.routes import bp as users_bp
        #  app.register_blueprint(users_bp)

        sentry_sdk.init(
            dsn=settings.sentry_url,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )

        return app


app = init_app()


@app.route('/')
def index():
    return '<h2>Pit-guild-manager Bot, use VK bot instead this</h2>'


@app.route('/api', methods=['POST'])
def api_access():
    try:
        data = json.loads(json.loads(request.data))
    except JSONDecodeError:
        return make_response("No data provided", 400)
    print(type(data))
    print(data)
    try:
        act = data['action']
    except KeyError:
        return make_response("Wrong key data provided", 400)
    except TypeError:
        return make_response("Wrong data provided", 402)

    if act == 'profile':
        try:
            key = data['user_key']
        except (KeyError, TypeError):
            return make_response("Wrong key data provided", 400)

        try:
            user_id = data['user_id']
        except (KeyError, TypeError):
            return make_response("Wrong key data provided", 400)
        res = dict()
        res['items'] = profile.inv(f'https://vip3.activeusers.ru/app.php?act=user&auth_key={key}&viewer_id={user_id}&group_id=182985865&api_id=7055214')
        return json.dumps(res)

    return make_response('Complete', 200)


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

    if int(group_id) != int(settings.group_id):
        # raise Exception(f'{group_id} != {settings.group_id}')
        return make_response("Error: only bot have access", 403)

    if type_msg == 'message_new':
        data_msg = obj_msg['message']
        message(data_msg)

    return make_response('ok', 200)


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


@app.route('/some-query')
def first_user():
    from db.tables import User
    user = request.args.get('id', default=0, type=int)
    res = User.query.filter_by(vk_id=user).first()
    return str(res)


'''
@app.route('/bot_worker')
def threads():
    # from threading import Thread
    print('\t\t\t', settings.user_bot)
    try:
        get_state = int(request.args.get('state', None))
    except (ValueError, TypeError):
        get_state = None
    if get_state is not None:
        settings.bot_worker = bool(get_state)

    if settings.bot_worker:
        from user_buy_bot import work as script

        import threading

        class StoppableThread(threading.Thread):
            """Thread class with a stop() method. The thread itself has to check
            regularly for the stopped() condition."""

            def __init__(self, *args, **kwargs):
                super(StoppableThread, self).__init__(*args, **kwargs)
                self._stop_event = threading.Event()

            def stop(self):
                self._stop_event.set()

            def stopped(self):
                return self._stop_event.is_set()

        settings.user_bot = StoppableThread(target=script)
        settings.user_bot.start()
        pass
    else:
        pass
    print('\t\t', settings.user_bot)

    return make_response('Bot status is ' + str(settings.bot_worker), 200)
'''


@app.route('/idk/how/do/you/get/there/aboba')
def get_vars():
    res = {}
    for i in dir(settings):
        if i == 'items' or i.startswith('__'):
            continue
        res[i] = getattr(settings, i, None)
    return str(res)


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
