# -*- coding: utf-8 -*-
import requests
import sys
import json
import pymongo
from bs4 import BeautifulSoup

key = "AIzaSyBNeMN5-449RqOvMw27ZN0xWuogMkSixRg"  # youtube api key


# mongodb initialize
uri = 'mongodb://vic010744:vic32823@ds135700.mlab.com:35700/heroku_4w25h5pt'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
db_video = db['video']


def main(argv):
    res = requests.get(
        'https://www.youtube.com/channel/UC9egiwuJsQZ0Cy2to5fvSIQ/playlists')  # get cat topic html
    soup = BeautifulSoup(res.text, "lxml")
    count = 0
    count2 = 0
    for item in soup.select(".yt-lockup-content"):
        title = item.select('a')[0].get('title')
        if(title == u'有趣的影片' or title == u'熱門影片 - 貓' or title == u'可愛的影片'):
            href = item.select('a')[0].get('href')
            playlist_id = href.split('=')[1]  # get playlist_id
            count = count + 1
            # use youtube api to get videos
            videos_json = requests.get(
                'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={}&key={}'.format(playlist_id, key))
            videos_data = json.loads(videos_json.text)
            videos = videos_data['items']
            for video in videos:
                if 'snippet' in video:
                    # get video content
                    if 'thumbnails' in video['snippet']:
                        video_url = 'https://www.youtube.com/watch?v=' + \
                            video['snippet']['resourceId']['videoId']
                        print 'get_data id = {}'.format(video['snippet']['resourceId']['videoId'])
                        if 'standard' in video['snippet']['thumbnails']:
                            thumbnails = video['snippet'][
                                'thumbnails']['standard']['url']
                        elif 'high' in video['snippet']['thumbnails']:
                            thumbnails = video['snippet'][
                                'thumbnails']['high']['url']
                        elif 'medium' in video['snippet']['thumbnails']:
                            thumbnails = video['snippet'][
                                'thumbnails']['medium']['url']
                        else:
                            thumbnails = video['snippet'][
                                'thumbnails']['default']['url']
                        title = video['snippet']['title']
                        publishedAt = video['snippet']['publishedAt']
                        description = video['snippet']['description']
                        count2 = count2 + 1

                        # upload to db
                        SEED_DATA = {
                            'url': video_url,
                            'thumbnails': thumbnails,
                            'title': title,
                            'description': description,
                            'publishedAt': publishedAt
                        }
                        db_video.insert_one(SEED_DATA)
                        print 'upload the video, url = {}'.format(video_url)

    print 'total playlist numbers = {}'.format(count)
    print 'total video numbers = {}'.format(count2)

if __name__ == '__main__':
    main(sys.argv[1:])
