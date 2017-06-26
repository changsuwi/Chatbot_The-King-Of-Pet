# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:50:20 2017
json_fb 此模組主要存放通用的json格式與打包
例如使用者輸入json ，template打包 ， main button 的json ，message的打包
@author: vicharm
"""
from sendtofb_log import sendtofb, log
import json


def typingon_json(recipient_id):
    #  construct typing on json
    log("sending  typingon to {recipient}".format(recipient=recipient_id))
    data = json.dumps({"recipient": {"id": recipient_id},
                       "sender_action": "typing_on"})
    sendtofb(data)


def json_template(recipient_id):
    template = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                    ]
                }
            }
        }
    }
    return template


def json_mainbutton(recipient_id):
    log("sending mainbutton to {recipient}".format(recipient=recipient_id))
    data = json.dumps(
        {
            "recipient":
            {
                "id": recipient_id
            },
            "message":
            {
                "text": "汪汪，我是聊天機器狗汪汪，我很聰明的，我可以做很多事:",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "聊天",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_CHAT"
                    },
                    {
                        "content_type": "text",
                        "title": "交換明信片",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_POSTCARD"
                    },
                    {
                        "content_type": "text",
                        "title": "可愛寵物影片推播",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_MOVIE"
                    },
                    {
                        "content_type": "text",
                        "title": "領養資訊搜尋",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_ADOPTION"
                    },
                    {
                        "content_type": "text",
                        "title": "民間送養資訊搜尋",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_ADOPTION"
                    }
                ]
            }
        }
    )
    sendtofb(data)


def json_photo(recipient_id, url):
    log("sending photo to {recipient}".format(recipient=recipient_id))
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": url
                }
            }
        }
    })
    sendtofb(data)


def json_message(recipient_id, message_text):  # construct message json

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    sendtofb(data)


def json_subscription(recipient_id):
    log("sending  json_subscription to {recipient}".format(
        recipient=recipient_id))
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": u"請問您是否要訂閱呢？ 訂閱可以在每天的固定時間接收新的可愛寵物影片呦",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": u"是",
                            "payload": "subscription_yes"
                        },
                        {
                            "type": "postback",
                            "title": u"否",
                            "payload": "subscription_no"
                        }
                    ]
                }
            }
        }
    })
    sendtofb(data)
