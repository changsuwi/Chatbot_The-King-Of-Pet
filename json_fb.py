# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:50:20 2017
json_fb 此模組主要存放通用的json格式與打包 例如使用者輸入json ，template打包 ， main button 的json ，message的打包
@author: vicharm
"""
from sendtofb_log import sendtofb,log
import pymongo
import pprint
import json

def typingon_json(recipient_id): 
    
    #construct typing on json 
    log("sending  typingon to {recipient}".format(recipient=recipient_id))
    data = json.dumps({
            "recipient":{
                    "id": recipient_id
                    },
            "sender_action":"typing_on"})
            
    sendtofb(data)
def json_template(template,recipient_id): #construct template json
    log("sending  template to {recipient}".format(recipient=recipient_id))
    data = json.dumps(template)
    sendtofb(data)
        
def json_mainbutton(recipient_id): #construct mainbutton json
    log("sending mainbutton to {recipient}".format(recipient=recipient_id))
    data=json.dumps(
            {"recipient":{
    "id": recipient_id
    },
    "message":{
    "text":"汪汪，我是聊天機器狗汪汪，我很聰明的，我可以做很多事:",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"聊天",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_CHAT"
      },
      {
        "content_type":"text",
        "title":"交換明信片",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_POSTCARD"
      },
      {
        "content_type":"text",
        "title":"可愛寵物影片推播",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_MOVIE"
      },
      {
        "content_type":"text",
        "title":"領養資訊搜尋",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_ADOPTION"
      },
      {
        "content_type":"text",
        "title":"民間送養資訊搜尋",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_ADOPTION"
      }
    ]
  }
    }
    )
    sendtofb(data)
def json_postcard_name(recipient_id):
    log("sending postcard_name to {recipient}".format(recipient=recipient_id))
    json_message(recipient_id,"請輸入姓名\n格式為:\n姓名:寵物名稱\nEX:\n姓名:蛋黃哥")
def json_postcard_context(recipient_id):
    log("sending postcard_context to {recipient}".format(recipient=recipient_id))
    json_message(recipient_id,"輸入一小段話來認識新朋友吧\n格式為:\n內容:文字\nEX:\n內容:這是我家的小母狗蛋黃，很可愛吧")
def json_postcard_photo(recipient_id):
    log("sending postcard_photo to {recipient}".format(recipient=recipient_id))
    json_message(recipient_id,"傳送一張寵物的可愛照吧~")
def json_video(recipient_id):
    log("sending video to {recipient}".format(recipient=recipient_id))
    uri = 'mongodb://vic010744:vic32823@ds135700.mlab.com:35700/heroku_4w25h5pt'
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection= db['video']
    #for item in collection.find():
    data={
            "recipient":{
            "id":recipient_id
            },
            "message":{
                    "attachment":{
                            "type":"video",
                            "payload":{
                                    "url":"https://video-tpe1-1.xx.fbcdn.net/v/t42.1790-2/17781300_1460293247338531_344435082691346432_n.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InN2ZV9zZCJ9&oh=cd9acf5c3d78947d569af31741e97527&oe=58EA01A8"
                                    }
                            }
                    }
                }
    json_template(data,recipient_id)
        #break
        
def json_message(recipient_id, message_text): #construct message json

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    sendtofb(data)
