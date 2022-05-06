from vk import Session, API
from vk.exceptions import VkAPIError

from settings import group_token, CONVERSATION_ADDING

api = API(Session(), v='5.131')


def get_id_msg(peer, conv_id):
    return api.messages.getByConversationMessageId(
        access_token=group_token,
        peer_id=peer,
        conversation_message_ids=[conv_id]
    )['items'][0]['id']


def send_msg(peer, msg, key=group_token, **kwargs):
    token = key
    return api.messages.send(
        access_token=token,
        peer_id=str(peer),
        random_id=0,
        message=str(msg),
        disable_mentions=True,
        **kwargs
        )


def pin_msg(peer, msg, key=group_token):
    token = key
    api.messages.pin(
        access_token=token,
        peer_id=str(peer),
        message_id=send_msg(peer, msg, token)
    )
    return


def kick(chat, user):
    token = group_token
    try:
        api.messages.removeChatUser(
            access_token=token,
            chat_id=chat,
            user_id=user
        )
        send_msg(chat+CONVERSATION_ADDING, f"Пользоваель @id{user} успешно кикнут")
    except VkAPIError:
        send_msg(chat+CONVERSATION_ADDING, "Ошибка при удалении пользователя")
    return

