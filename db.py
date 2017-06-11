# -*- coding: utf-8 -*-


import pymongo
import random

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
    if(Postcard.count(query) == 0):
        SEED_DATA = {
            'url': url,
            'ID': sender_id
        }
        print Postcard.insert_one(SEED_DATA)
    else:
        Postcard.update(query, {'$set': {'url': url}})


def upload_db_intro(text, sender_id):
    Postcard = db['postcard']
    query = {'ID': sender_id}
    Postcard.update(
        query, {'$set': {'intro': text, 'match': '0', 'match_id': "None"}})
    client.close()


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

