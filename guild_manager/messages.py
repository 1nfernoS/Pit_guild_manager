import guild_manager.profile_api as profile
from guild_manager.forwards import forward
from guild_manager.commands import command
from guild_manager.payloads import payload

from guild_manager import vk_bot

# import db.users as users

# from db.instance import DB
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
    prefix = ['-', '+']

    text = str(msg['text'])
    chat = int(msg['peer_id'])
    user = int(msg['from_id'])

    # ignore bot's messages
    if user < 0:
        return

    # vk_bot.send_msg(chat, 'Сообщение получени, не от бота')

    if chat < settings.CONVERSATION_ADDING:

        # vk_bot.send_msg(chat, 'Сообщение в лс')
        # profile parse
        if len(msg['attachments']) != 0:
            at = msg['attachments'][0]
            if at['type'] == 'link':
                if text == "":
                    text = at['link']['url']
        if 'https://vip3.activeusers.ru/app.php?' in text:
            # vk_bot.send_msg(chat, 'Сообщение с профилем')

            s = text[text.find('act='):text.find('&group_id')]
            auth = s[s.find('auth_key') + 9:s.find('auth_key') + 41]
            inv = profile.inv(text)
            passives = profile.passive(auth, user)
            actives = profile.active(auth, user)
            class_id = inv[0] if inv[0] != '14108' else inv[1]

            #                       ['user_id', 'auth_token', 'build', 'class_id', 'is_leader', 'is_officer']
            # u = User(user, auth, str(inv), int(class_id))
            # DB.session.add(u)
            # DB.session.commit()
            # users.write_users(user, {'user_id': user, 'auth_token': auth, 'build': inv, 'class_id': class_id, 'is_leader': False, 'is_officer': False})

            answer = ''
            answer += 'Регистрация успешна!\n'
            answer += f'Класс: {settings.items[class_id]}\n'
            answer += 'Экипировка:\n\n'
            answer += '\n'.join([settings.items[i] for i in inv if
                                 settings.items[i].startswith('(А)')
                                 or settings.items[i].startswith('(П)')
                                 or 'Адмов' in settings.items[i]])
            vk_bot.send_msg(chat, answer)

            answer = ''
            answer += 'Активные умения:\n\n'
            answer += '\n'.join([f'{i[0]} {i[1]} ({i[2]}%)' for i in actives])
            vk_bot.send_msg(chat, answer)

            answer = ''
            answer += 'Пассивные умения:\n\n'
            answer += '\n'.join([f'{i[0]} {i[1]} ({i[2]}%)' for i in passives])
            vk_bot.send_msg(chat, answer)

            # TODO: Save equipment

    if 'payload' in msg.keys():
        payload(msg)
        # payload grants that there is no reply or command
        return

    if len(msg['fwd_messages']) == 1:
        if msg['fwd_messages'][0]['from_id'] in [settings.PIT_BOT, settings.OVERSEER_BOT]:
            forward(msg)
        return

    if len(text) == 0:
        return

    if 1 == 2 \
            or text.startswith('+') \
            or text.startswith('-') \
            or text.startswith('/') \
            :
        command(msg)
        pass

    return
