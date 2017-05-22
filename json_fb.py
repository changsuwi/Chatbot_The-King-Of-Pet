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


def json_template(template, recipient_id):
    log("sending  template to {recipient}".format(recipient=recipient_id))
    data = json.dumps(template)
    sendtofb(data)


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


def json_video(recipient_id):
    log("sending video to {recipient}".format(recipient=recipient_id))
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "video",
                "payload": {
                    "url": "https://r6---sn-u5oxu-uooe.googlevideo.com/videoplayback?lmt=1492925516230696&ip=140.116.1.136&pl=19&dur=527.046&mv=m&source=youtube&ms=au&ei=20wiWbWNGomz4gLKhY-oBw&mn=sn-u5oxu-uooe&mm=31&id=o-AKDAHfT410h3N80zSZuM9lqMOAVRhtonRN5oUiyQh-Bo&signature=D6AF22F97BC4855FFF93B207F5A37AF2E4BA6202.0AE794100DF50BB1CA89E75E206A565D5A3D0EF8&requiressl=yes&mt=1495420041&itag=22&ratebypass=yes&ipbits=0&initcwndbps=5277500&mime=video%2Fmp4&key=yt6&sparams=dur%2Cei%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&expire=1495441723&upn=0Qky2oY2CYk"
                }
            }
        }
    }
    json_template(data, recipient_id)


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
