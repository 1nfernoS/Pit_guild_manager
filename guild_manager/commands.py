import guild_manager.vk_bot as vk_bot
import settings


def command(msg):
    cmd = msg['text'].split()[0][1:]
    if cmd in globals():
        globals()[cmd](msg)
    return


def kick(msg):
    # TODO: Check role
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
