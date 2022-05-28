import re
from settings import items
from guild_manager.profile_api import price
import guild_manager.vk_bot as vk_bot


def forward(msg):
    # TODO: forwards parse
    fwd_msg = msg['fwd_messages'][0]
    if 'Цена: ' in fwd_msg['text']:
        auction_price(fwd_msg, msg['peer_id'])
    pass


def auction_price(fwd, peer):
    import traceback
    try:
        s = fwd['text'].split('\n')
        item_id = list(items.keys())[list(items.values()).index(s[0][s[0].find('1*')+2:])]
        avg_price = price(item_id)
        vk_bot.send_msg(peer, avg_price)
        merc_price = int(re.findall(r'\d+', s[1])[1])  # 1 - emoji, 2  - price
        vk_bot.send_msg(peer, merc_price)
    except:
        vk_bot.send_msg(peer, traceback.format_exc(-2))
        item_id = 'NULL'
        avg_price = 'NULL'
        merc_price = 'NULL'
    msg = f'Товар: {items[item_id]}:\nЦена на аукционе: &#127765; {avg_price} (&#127765; {round(avg_price * 0.9)} чистыми)\nЦена торговца: {merc_price}'
    vk_bot.send_msg(peer, msg)
    return
