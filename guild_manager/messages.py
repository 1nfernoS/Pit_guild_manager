def message(msg):
    text = str(msg['text'])
    chat = int(msg['peer_id'])
    user = int(msg['from_id'])
    # TODO:
    #  1. Initialize item list (DB or smth)
    #  2. Check logs (Overseer, gold, shatters)
    #  3. DB for users (id, url profile, etc) and buffers (id, type, token, chat_id, etc)
    #  4. Pricing items?
    #  5. CM functions (kick, punishments, announcements)
    #  6. Notes and stuff
    #  7. In-game assist (books, walk, questions, road cross, etc)
    '''
    if text.startswith('/'):
        if user == settings.creator_id:
            if text == '/check':
                msg = 'Test fine'
                # TODO: get chat_id
                api.messages.send(access_token=settings.user_token,
                                  chat_id=str(266),
                                  random_id=0,
                                  message=str(msg))
            if text == '/ping':
                msg = 'All worked out Fine'
                api.messages.send(access_token=settings.group_token,
                                  peer_id=str(chat),
                                  random_id=0,
                                  message=str(msg))
    '''
    return
