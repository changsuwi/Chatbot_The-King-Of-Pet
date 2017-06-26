# coding=utf-8

from ..json_fb import json_mainbutton, json_message, json_photo
from ..json_fb import json_subscription, json_ask_reply_mail
from adopt.search1 import json_location
from adopt.search2 import json_choosedogcat2
from video import deal_video
from db import upload_flag, get_mail, get_video, first_use, deal_subscription


def postback_control(messaging_event, sender_id):
    if messaging_event["postback"]["payload"] == 'GET_STARTED_PAYLOAD':
        upload_flag(0, sender_id)
        json_message(sender_id, "汪汪")
        json_mainbutton(sender_id)
    elif messaging_event["postback"]["payload"] == 'main_button1':
        upload_flag(1, sender_id)
        json_message(
            sender_id, "我懂很多寵物知識喔\n你可以問我有關寵物領養 寵物健康 寵物食品的各種問題~")
    elif messaging_event["postback"]["payload"] == 'main_button2':
        upload_flag(2, sender_id)
        json_message(sender_id, "請先傳送一張寵物的可愛照吧~")
    elif messaging_event["postback"]["payload"] == 'main_button3':
        upload_flag(3, sender_id)
        videos = get_video()
        deal_video(sender_id, videos)
        if first_use(sender_id, 3) == 1:
            json_subscription(sender_id)
    elif messaging_event["postback"]["payload"] == 'main_button4':
        upload_flag(4, sender_id)
        json_location(sender_id)
    elif messaging_event["postback"]["payload"] == 'main_button5':
        upload_flag(5, sender_id)
        json_choosedogcat2(sender_id)
    elif messaging_event['postback']['payload'] == 'get_match_mail':
        mail = get_mail(sender_id)
        intro = mail['intro']
        img_url = mail['url']
        json_photo(sender_id, img_url)
        json_message(sender_id, intro.encode('utf-8'))
        json_ask_reply_mail(sender_id)
    elif messaging_event['postback']['payload'] == 'subscription_yes':
        deal_subscription(sender_id, 1)
        json_message(sender_id, "訂閱完成")
    elif messaging_event['postback']['payload'] == 'subscription_no':
        deal_subscription(sender_id, 0)
        json_message(
            sender_id, "好的，若未來有需要訂閱，點選\n工作列->\n可愛動物影片推播->\n訂閱功能")
    elif messaging_event['postback']['payload'] == 'reply_yes':
        json_message(
            sender_id, "本汪已準備好，幫你寄信拉～ 不管是文字 圖片 音訊 都交給本汪吧")
        upload_flag(6, sender_id)
