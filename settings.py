import os
import json


group_token = os.environ.get('GROUP_TOKEN')
confirmation_token = os.environ.get('CONFIRMATION_TOKEN')
group_id = os.environ.get('GROUP_ID')
user_token = os.environ.get('USER_TOKEN')
creator_id = os.environ.get('CREATOR_ID')
sentry_url = os.environ.get('SENTRY_URL')
DB_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://', 1)

CONVERSATION_ADDING = 2000000000
PIT_BOT = -182985865
OVERSEER_BOT = -183040898

bot_worker = True
user_bot = None


class Config:
    ENV = 'development'
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = DB_URI


with open('db/items', 'r') as f:
    items = json.loads(f.readline())
