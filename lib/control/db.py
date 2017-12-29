# -*- coding: utf-8 -*-


import pymongo
import random
from ..json_fb import json_message, json_photo
#  Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

uri = 'mongodb://vic010744:vic32823@ds135700.mlab.com:35700/heroku_4w25h5pt'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
###############################################################################
# main
###############################################################################


def upload_flag(flag, sender_id):
    Category = db['flag']
    query = {'ID': sender_id}
    if(Category.count(query) == 0):
        Category.insert_one({'ID': sender_id, 'flag': flag})
    else:
        query = {'ID': sender_id}
        Category.update(query, {'$set': {'flag': flag}})


def get_flag(sender_id):
    Category = db['flag']
    dat = Category.find_one({'ID': sender_id})
    return dat['flag']


def upload_db_photo_url(url, sender_id):
    Postcard = db['postcard']
    query = {'ID': sender_id}
    # first use
    if(Postcard.count(query) == 0):
        SEED_DATA = {
            'url': url,
            'ID': sender_id,
            'intro': 'None',
            'match': '0',
            'match_id': "None"
        }
        print Postcard.insert_one(SEED_DATA)
    # user has used
    # 未來新增選項讓使用者選擇是否要用新明信片 或是沿用舊的
    # new postcard
    else:
        target_id = get_reci_id(sender_id)
        if target_id is not 'None':
            json_message(target_id, '不好意思，您的明信片好友已離開，若需要交換新明信片，請點選功能表內的交換新明信片')
            Postcard.update({'ID': target_id},
                            {'$set': {'match_id': 'None', 'match': '-1'}})
        Postcard.update(query, {
            '$set': {'url': url, 'match': '0', 'match_id': 'None'}})


def upload_db_intro(text, sender_id):
    Postcard = db['postcard']
    query = {'ID': sender_id}
    Postcard.update(
        query, {'$set': {'intro': text}})
    client.close()


def upload_db_nickname(text, sender_id):
    Postcard = db['postcard']
    query = {'ID': sender_id}
    Postcard.update(
        query, {'$set': {'nickname': text}})
    client.close()


def get_nickname(sender_id):
    Postcard = db['postcard']
    dat = Postcard.find_one({'ID': sender_id})
    return dat['nickname']


def json_match(recipient_id, sender_nickname):
    upload_flag(6, recipient_id)
    json_message(recipient_id, '本汪咬到一封明信片\n寄信人：{sender}\n內容如下'.format(
        sender=sender_nickname.encode('UTF-8')))
    user_mail = get_mail(recipient_id)
    friend_mail = get_mail(user_mail['match_id'])
    intro = sender_nickname + ':' + '\n' + friend_mail['intro']
    img_url = friend_mail['url']
    json_photo(recipient_id, img_url)
    json_message(recipient_id, intro.encode('utf-8'))
    json_message(
        recipient_id, "現在只要傳送訊息，都會傳送到對方那喔")
    json_message(
        recipient_id, "若不想與對方聊天了\n點開功能表->\n交換明信片->\n刪除明信片好友即可")


def match(sender_id):
    Postcard = db['postcard']
    target = Postcard.find({'match': '0'})
    for item in target:
        if(item['ID'] != sender_id):
            query = {'ID': item['ID']}
            Postcard.update(
                query, {'$set':
                        {'match': '1', 'match_id': sender_id}})
            query = {'ID': sender_id}
            sender_data = Postcard.find_one(query)
            sender_nickname = sender_data['nickname']
            Postcard.update(
                query, {'$set':
                        {'match': '1', 'match_id': item['ID']}})
            json_match(item['ID'], sender_nickname)
            json_match(sender_id, item['nickname'])


def get_mail(sender_id):
    Postcard = db['postcard']
    query = {'ID': sender_id}
    data = Postcard.find_one(query)
    return data


def get_video():
    Video = db['video']
    videos = Video.find()
    count = videos.count()
    video_list = []
    for x in range(0, 7):
        video = videos[random.randint(0, count - 1)]
        video_list.append(video)
    return video_list


def first_use(sender_id, mode):
    query = {'ID': sender_id}
    if mode == 3:
        Subscription = db['subscription']
        if Subscription.count(query) == 0:
            return 1
        else:
            return 0


def deal_subscription(sender_id, mode):
    Subscription = db['subscription']
    query = {'ID': sender_id}
    if mode == 0:
        if Subscription.count(query) == 0:
            SEED_DATA = {
                'ID': sender_id,
                'subscription': 0
            }
            Subscription.insert_one(SEED_DATA)
        else:
            Subscription.update(query, {'$set': {'subscription': 0}})

    else:
        if Subscription.count(query) == 0:
            SEED_DATA = {
                'ID': sender_id,
                'subscription': 1
            }
            Subscription.insert_one(SEED_DATA)
        else:
            Subscription.update(query, {'$set': {'subscription': 1}})


def get_reci_id(sender_id):
    Postcard = db['postcard']
    query = {'ID': sender_id}
    data = Postcard.find_one(query)
    return data['match_id']


def del_friend(sender_id):
    Postcard = db['postcard']
    target_id = get_reci_id(sender_id)
    json_message(target_id, '不好意思，您的明信片好友已離開，若需要交換新明信片，請點選功能表內的交換新明信片')
    Postcard.update({'ID': target_id}, {
                    '$set': {'match': '-1', 'match_id': 'None'}})
    Postcard.update({'ID': sender_id}, {
                    '$set': {'match': '-1', 'match_id': 'None'}})
