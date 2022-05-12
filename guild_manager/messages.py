import guild_manager.profile_api as profile
from guild_manager.forwards import forward
from guild_manager.commands import command
from guild_manager.payloads import payload

# from db.tables import User, Item

import settings

# TODO:
#  1. Initialize item list (DB or smth)
#  2. Check logs (Overseer, gold, shatters)
#  3. DB for users (id, url profile, etc) and buffers (id, type, token, chat_id, etc)
#  4. Pricing items?
#  5. CM functions (kick, punishments, announcements)
#  6. Notes and stuff
#  7. In-game assist (books, walk, questions, road cross, etc)


def message(msg):
    # TODO: store prefix somewhere else, and add opportunity to change it
    prefix = '-'

    text = str(msg['text'])
    chat = int(msg['peer_id'])
    user = int(msg['from_id'])

    # ignore bot's messages
    if user < 0:
        return

    if chat < settings.CONVERSATION_ADDING:
        # profile parse
        if 'https://vip3.activeusers.ru/app.php?' in text:
            inv = profile.inv(text)
            # TODO: Save equipment

    if 'payload' in msg.keys():
        payload(msg)
        # payload grants that there is no reply or command
        return

    if len(msg['fwd_messages']) == 1:
        if msg['fwd_messages'][0]['from_id'] in [settings.PIT_BOT, settings.OVERSEER_BOT]:
            forward(msg)
        pass

    if text.startswith(prefix):
        command(msg)
        pass

    return
