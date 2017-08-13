# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:50:20 2017
json_fb 此模組主要存放通用的json格式與打包
例如使用者輸入json ，template打包 ， main button 的json ，message的打包
@author: vicharm
"""
from sendtofb_log import sendtofb, log
import json
from lib.control.db import get_mail


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
                "text": "你要選擇哪個呢？",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "聊天",
                        "payload": "main_button1"
                    },
                    {
                        "content_type": "text",
                        "title": "交換明信片",
                        "payload": "main_button2"
                    },
                    {
                        "content_type": "text",
                        "title": "可愛寵物影片推播",
                        "payload": "main_button3"
                    },
                    {
                        "content_type": "text",
                        "title": "領養資訊搜尋",
                        "payload": "main_button4"
                    },
                    {
                        "content_type": "text",
                        "title": "民間送養資訊搜尋",
                        "payload": "main_button5"
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


def json_match(recipient_id):
    log("sending  match mail to {recipient}".format(recipient=recipient_id))
    json_message(recipient_id, '本汪咬到一封明信片')
    user_mail = get_mail(recipient_id)
    friend_mail = get_mail(user_mail['match_id'])
    intro = friend_mail['intro']
    img_url = friend_mail['url']
    json_photo(recipient_id, img_url)
    json_message(recipient_id, intro.encode('utf-8'))
    '''
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": u"主人，本汪剛剛在門口咬到一封明信片XDD",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": u"前往查看",
                            "payload": "get_match_mail"
                        }
                    ]
                }
            }
        }
    })
    sendtofb(data)'''


def json_ask_reply_mail(recipient_id):
    log("sending  json_ask_reply_mail to {recipient}".format(
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
                    "text": u"請問您要回信嗎？",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": u"是",
                            "payload": "reply_yes"
                        },
                        {
                            "type": "postback",
                            "title": u"否",
                            "payload": "reply_no"
                        }
                    ]
                }
            }
        }
    })
    sendtofb(data)


def json_del_friend(recipient_id):
    log("sending  json_del_friend to {recipient}".format(
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
                    "text": u"請問您要刪除明信片好友嗎？",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": u"是",
                            "payload": "del_yes"
                        },
                        {
                            "type": "postback",
                            "title": u"否",
                            "payload": "del_no"
                        }
                    ]
                }
            }
        }
    })
    sendtofb(data)
