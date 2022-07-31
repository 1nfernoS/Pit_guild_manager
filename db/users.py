"""
import json


def get_users(user_id=None):
    with open('db/user_list', 'r') as f:
        users = json.loads(f.readline())

    if user_id is not None:
        for i in users:
            if i['user_id'] == user_id:
                return i
        return -1

    return users


def set_val(user_id, **kwargs):
    u = get_users(user_id)
    if u != -1:
        for i in kwargs:
            if i in u.keys():
                u[i] = kwargs[i]
        write_users(user_id, u)


def write_users(user_id, data):
    users = get_users()
    if all(p in data.keys() for p in ['user_id', 'auth_token', 'build', 'class_id', 'is_leader', 'is_officer']):
        index = -1
        for i in users:
            if i['user_id'] == user_id:
                index = users.index(i)
                break
        if index < 0:
            users.append(data)
        else:
            users[index] = data

        with open('db/user_list', 'w') as f:
            f.write(json.dumps(users))


def del_user(user_id):
    users = get_users()
    if get_users(user_id) != -1:
        users.pop(users.index(get_users(user_id)))

    with open('db/user_list', 'w') as f:
        f.write(json.dumps(users))


'''

class User:
    _user_id = 0
    _auth_token = ''
    _build = list()
    _class_id = 0
    _is_leader = False
    _is_officer = False

    def __init__(self, user_id: int = 0, auth_token: str = '', build: list = None, class_id: int = 0, leader: bool = False, officer: bool = False):
        self._user_id = user_id
        self._auth_token = auth_token
        self._build = build if build is not None else list()
        self._class_id = class_id
        self._is_leader = leader
        self._is_officer = officer
        return

    def data(self):
        res = dict()
        res['user_id'] = self._user_id
        res['auth_token'] = self._auth_token
        res['build'] = self._build
        res['class_id'] = self._class_id
        res['is_leader'] = self._is_leader
        res['is_officer'] = self._is_officer
        return res

    def set_leader(self):
        # TODO: Checks
        self._is_leader = True

    def del_leader(self):
        self._is_leader = False

    def is_leader(self):
        return self._is_leader

    def set_officer(self):
        self._is_officer = True

    def del_officer(self):
        self._is_officer = False

    def is_officer(self):
        return self._is_officer

    def get_build(self):
        return self._build

    def set_build(self, build: list):
        # TODO: Checks
        self._build = build

'''
"""