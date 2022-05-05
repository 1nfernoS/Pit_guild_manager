import os
import json

group_token = os.environ.get('GROUP_TOKEN')
confirmation_token = os.environ.get('CONFIRMATION_TOKEN')
group_id = int(os.environ.get('GROUP_ID'))
user_token = os.environ.get('USER_TOKEN')
creator_id = int(os.environ.get('CREATOR_ID'))
sentry_url = os.environ.get('SENTRY_URL')

CONVERSATION_ADDING = 2000000000
PIT_BOT = -182985865
OVERSEER_BOT = -183040898
items = json.loads("items_list.json")
