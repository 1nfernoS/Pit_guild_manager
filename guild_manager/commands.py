import guild_manager.vk_bot as vk_bot
import settings


def command(msg):
    cmd = msg['text'].split()[0][1:]
    if cmd in globals():
        globals()[cmd](msg)
    return


def kick(msg):
    # TODO: Check role (leader, officer)
    if msg['from_id'] != settings.creator_id:
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

'''
def leader(msg):
    if msg['from_id'] != settings.creator_id:
        return

    user = None
    if 'reply_message' in msg.keys():
        user = msg['reply_message']['from_id']
    if len(msg['fwd_messages']) == 1:
        user = msg['fwd_messages'][0]['from_id']

    if user:
        pass
        # TODO:
        #  check is leader was set already
        #  set leader role to user
    else:
        vk_bot.send_msg(msg['peer_id'], "Перешлите или ответьте на сообщение пользователя, чтобы выдать права лидера")
    return


def officer(msg):
    # TODO: give access to leader
    if msg['from_id'] != settings.creator_id:
        return

    user = None
    if 'reply_message' in msg.keys():
        user = msg['reply_message']['from_id']
    if len(msg['fwd_messages']) == 1:
        user = msg['fwd_messages'][0]['from_id']

    if user:
        pass
        # TODO:
        #  set officer role to user
    else:
        vk_bot.send_msg(msg['peer_id'], "Перешлите или ответьте на сообщение пользователя, чтобы выдать права офицера")
    return


def help(msg):
    # TODO: Write message
    message = "It isn't done now . . . Wait some updates"
    vk_bot.send_msg(msg['peer_id'], message)
    return
'''
