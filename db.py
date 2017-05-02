# -*- coding: utf-8 -*-


import pymongo


### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

uri = 'mongodb://vic010744:vic32823@ds023455.mlab.com:23455/heroku_xfc3zss3' 

###############################################################################
# main
###############################################################################



def upload_db_photo_url(url,sender_id):

    client = pymongo.MongoClient(uri)

    db = client.get_default_database()
    
    # First we'll add a few songs. Nothing is required to create the songs 
    # collection; it is created automatically when we insert.

    Postcard = db['Postcard']

    # Note that the insert method can take either an array or a single dict.
    SEED_DATA={
            'url': url,
            'ID': sender_id
            }
    Postcard.insert_one(SEED_DATA)

    # Then we need to give Boyz II Men credit for their contribution to
    # the hit "One Sweet Day".

    #query = {'song': 'One Sweet Day'}

    #songs.update(query, {'$set': {'artist': 'Mariah Carey ft. Boyz II Men'}})

    # Finally we run a query which returns all the hits that spent 10 or
    # more weeks at number 1.

    #cursor = songs.find({'weeksAtOne': {'$gte': 10}}).sort('decade', 1)

    #for doc in cursor:
     #   print ('In the %s, %s by %s topped the charts for %d straight weeks.' %
      #         (doc['decade'], doc['song'], doc['artist'], doc['weeksAtOne']))
    
    ### Since this is an example, we'll clean up after ourselves.

    ###db.drop_collection('songs')

    ### Only close the connection when your app is terminating

    client.close()