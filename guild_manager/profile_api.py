from bs4 import BeautifulSoup
import requests
import json


# TODO: Add using for this

def id_tag(tag, search, skip=0):
    for j in range(len(tag.find_all('div'))):
        if search in tag.find_all('div')[j]['class']:
            if skip > 0:
                skip -= 1
            else:
                return j


def active(auth_key, user_id):
    url = f'https://vip3.activeusers.ru/app.php?act=pages&id=620&auth_key={auth_key}&viewer_id={user_id}&group_id=182985865&api_id=7055214'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    t1 = soup.body
    t2 = t1.find_all('div')[id_tag(t1, 'app_pages')]
    t3 = t2.div.div.div.div
    res_list = list()

    for i in t3.find_all('li'):
        z = list()
        for j in i.text.split():
            if j.endswith(':'):
                z.append(' '.join(i.text.split()[:i.text.split().index(j) + 1]))
            if j.isdigit():
                z.append(int(j))
                z.append((round((int(j) / 10) ** 0.5 * 10) + 100) / 100)
        res_list.append(z)
    return res_list


def passive(auth_key, user_id):
    url = f'https://vip3.activeusers.ru/app.php?act=pages&id=622&auth_key={auth_key}&viewer_id={user_id}&group_id=182985865&api_id=7055214'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    t1 = soup.body
    t2 = t1.find_all('div')[id_tag(t1, 'app_pages')]
    t3 = t2.div.div.div.div
    res_list = list()

    for i in t3.find_all('li'):
        z = list()
        for j in i.text.split():
            if j.endswith(':'):
                z.append(' '.join(i.text.split()[:i.text.split().index(j) + 1]))
            if j.isdigit():
                z.append(int(j))
                z.append((round((int(j) / 10) ** 0.5 * 10) + 100) / 100)
        res_list.append(z)
    return res_list


def price(item):
    url = f'https://vip3.activeusers.ru/app.php?act=item&id={item}&auth_key=5153d58b92d71bda47f1dac05afc187a&viewer_id=158154503&group_id=182985865&api_id=7055214'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    t1 = soup.body
    t2 = t1.find_all('div')[id_tag(t1, 'app_item')]
    t3 = t2.div.div
    t4 = t3.find_all('div')[id_tag(t3, 'section')]
    t5 = t4.find_all('div')[id_tag(t4, 'portlet')]
    t6 = t5.find_all('div')[id_tag(t5, 'row', 1)]
    t7 = t6.div.div.div.find_all('script')[1]
    t8 = str(t7)[str(t7).find('window.graph_data'):]
    t9 = json.loads(t8[20:t8.find(';')])
    price_list = list()
    for i in t9:
        price_list.append(i[1])
    return round(sum(price_list) / 20)


def stats(url_profile):
    if 'act=user' not in url_profile:
        return

    soup = BeautifulSoup(requests.get(url_profile).content, 'html.parser')
    t1 = soup.body
    t2 = t1.find_all('div')[id_tag(t1, 'profile-content')]
    t3 = t2.div.div.div.div
    t4 = t3.find_all('div')[id_tag(t3, 'portlet-body')]
    t5 = t4.find_all('span')
    stat = []
    for i in range(0, len(t5), 2):
        stat.append(int(t5[i].text))
    res = {'level': stat[0], 'attack': stat[1], 'defence': stat[2],
           'strength': stat[3], 'agility': stat[4], 'endurance': stat[5],
           'luck': stat[6], 'accuracy': stat[7], 'concentration': stat[8]}
    return res


def inv(url_profile):
    if 'act=user' not in url_profile:
        return

    soup = BeautifulSoup(requests.get(url_profile).content, 'html.parser')
    t1 = soup.body
    t2 = t1.find_all('div')[id_tag(t1, 'app_user')]
    t3 = t2.div.div
    t4 = t3.find_all('div')[id_tag(t3, 'progress-box')]
    t5 = t4.find_all('div')[2].div
    res_list = list()
    for i in t5.find_all('a'):
        res_list.append(i['href'][i['href'].find('id=') + 3:i['href'].find('id=') + 8])
    return res_list
