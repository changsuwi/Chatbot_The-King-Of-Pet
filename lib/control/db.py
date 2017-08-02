# -*- coding: utf-8 -*-


import pymongo
import random
from ..json_fb import json_match
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
        Postcard.update(
            query, {'$set': {'match_id': 'None', match: '0'}})
        target_id = get_reci_id(sender_id)
        query = {'ID': target_id}
        # 未來可能新增提示訊息給使用者，讓使用者知道已無配對
        Postcard.update(
            query, {'$set': {'match_id': 'None', match: '0'}})


def upload_db_intro(text, sender_id):
    Postcard = db['postcard']
    query = {'ID': sender_id}
    Postcard.update(
        query, {'$set': {'intro': text}})
    client.close()


def match(sender_id):
    Postcard = db['postcard']
    target = Postcard.find({'match': '0'})
    for item in target:
        if(item['ID'] != sender_id):
            query = {'ID': item['ID']}
            Postcard.update(
                query, {'$set':
                        {'match': '1', 'match_id': sender_id}})
            json_match(item['ID'])
            query = {'ID': sender_id}
            Postcard.update(
                query, {'$set':
                        {'match': '1', 'match_id': item['ID']}})
            json_match(sender_id)


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
    Postcard.update({'ID': target_id}, {
                    '$set': {'match': '0', 'match_id': 'None'}})
    Postcard.update({'ID': sender_id}, {
                    '$set': {'match': '0', 'match_id': 'None'}})
