from vk import Session, API

from settings import group_token

api = API(Session(), v='5.131')


def send_msg(peer, msg, key=group_token):
    token = key
    return api.messages.send(
        access_token=token,
        peer_id=str(peer),
        random_id=0,
        message=str(msg)
        )


def pin_msg(peer, msg, key=group_token):
    token = key
    api.messages.pin(
        access_token=token,
        peer_id=str(peer),
        message_id=send_msg(peer, msg, token)
    )
    return
