# -*- coding: utf-8 -*-
"""
Created on Tue May 02 22:16:19 2017

@author: vic
"""

from imgurpython import ImgurClient


def upload_photo(image_url):
    client_id = '9efb779cd512a75'
    client_secret = 'f0c60f6d82e3b9b2d33a7f81318ac950ee424aa4'
    access_token = '3827abdb987541f4e5d7831cfa91f64b838d6fcf'
    refresh_token = '1df2672c250d33d5823ddf7d7a1d34ffbca0b2fc'
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    album = None # You can also enter an album ID here
    config = {
		'album': album,
	}

    print("Uploading image... ")
    image = client.upload_from_url(image_url, config=config, anon=False)
    print("Done")    
    return image['link']


