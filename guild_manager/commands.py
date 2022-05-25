import guild_manager.vk_bot as vk_bot
import settings

import db.users as users
from settings import items


def command(msg):
    cmd = msg['text'].split()[0][1:]
    if cmd in globals():
        globals()[cmd](msg)
    return


def kick(msg):
    # TODO: Check role (leader, officer)
    if msg['from_id'] != int(settings.creator_id):
        u = users.get_users(msg['from_id'])
        if u == -1:
            return
        if not u['is_leader'] and not u['is_officer']:
            return

    chat = msg['peer_id']-settings.CONVERSATION_ADDING
    user = None
    if 'reply_message' in msg.keys():
        user = msg['reply_message']['from_id']
    if len(msg['fwd_messages']) == 1:
        user = msg['fwd_messages'][0]['from_id']

    if user:
        if msg['from_id'] == user:
            vk_bot.send_msg(msg['peer_id'], "Кикать самого себя? Может не стоит?",
                            reply_to=vk_bot.get_id_msg(msg['peer_id'], msg['conversation_message_id']))
            return
        vk_bot.kick(chat, user)
    else:
        vk_bot.send_msg(msg['peer_id'], "Перешлите или ответьте на сообщение пользователя, чтобы его кикнуть")

    return


def leader(msg):
    if msg['from_id'] != int(settings.creator_id):
        return

    user = None
    if 'reply_message' in msg.keys():
        user = msg['reply_message']['from_id']
    if len(msg['fwd_messages']) == 1:
        user = msg['fwd_messages'][0]['from_id']

    if user:
        if msg['from_id'] == user:
            vk_bot.send_msg(msg['peer_id'], "Cамого себя? Так не работает",
                            reply_to=vk_bot.get_id_msg(msg['peer_id'], msg['conversation_message_id']))
            return

        if type(users.get_users(user)) == int:
            vk_bot.send_msg(msg['peer_id'], f"Такой не зарегистрирован!")
            return

        if msg['text'].startswith('-'):
            users.set_val(user, is_leader=False)
            vk_bot.send_msg(msg['peer_id'], f"Теперь vk.com/id{user} больше не имеет привелегии лидера")

        if msg['text'].startswith('+'):
            users.set_val(user, is_leader=True)
            vk_bot.send_msg(msg['peer_id'], f"Теперь vk.com/id{user} имеет привелегии лидера")
    else:
        vk_bot.send_msg(msg['peer_id'], "Перешлите или ответьте на сообщение пользователя, чтобы выдать права лидера")
    return


def officer(msg):
    # TODO: give access to leader
    if msg['from_id'] == int(settings.creator_id):
        pass
    else:
        u = users.get_users(msg['from_id'])
        if u == -1:
            return
        if not u['is_leader']:
            vk_bot.send_msg(msg['peer_id'], "Только лидеры и создатель могут назначать офицеров")
            return

    user = None
    if 'reply_message' in msg.keys():
        user = msg['reply_message']['from_id']
    if len(msg['fwd_messages']) == 1:
        user = msg['fwd_messages'][0]['from_id']

    if user:
        if msg['from_id'] == user:
            vk_bot.send_msg(msg['peer_id'], "Cамого себя? Так не работает",
                            reply_to=vk_bot.get_id_msg(msg['peer_id'], msg['conversation_message_id']))
            return
        if type(users.get_users(user)) == int:
            vk_bot.send_msg(msg['peer_id'], f"Такой не зарегистрирован!")
            return

        if msg['text'].startswith('-'):
            users.set_val(user, is_officer=False)
            vk_bot.send_msg(msg['peer_id'], f"Теперь vk.com/id{user} больше не имеет привелегии офицера")

        if msg['text'].startswith('+'):
            users.set_val(user, is_officer=True)
            vk_bot.send_msg(msg['peer_id'], f"Теперь vk.com/id{user} имеет привелегии офицера")

    else:
        vk_bot.send_msg(msg['peer_id'], "Перешлите или ответьте на сообщение пользователя, чтобы выдать права офицера")
    return


def help(msg):
    # TODO: Write message
    message = "It isn't done now . . . Wait some updates"
    vk_bot.send_msg(msg['peer_id'], message)
    return
