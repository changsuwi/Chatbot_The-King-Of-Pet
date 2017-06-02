# coding=utf-8
import pymongo
import random
#  Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

uri = 'mongodb://vic010744:vic32823@ds135700.mlab.com:35700/heroku_4w25h5pt'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
Video = db['video']
videos = Video.find()
count = videos.count()
for x in range(0, 3):
    video = videos[random.randint(0, count - 1)]
    print video['title'].encode('utf-8')
