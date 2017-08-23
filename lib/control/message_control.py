# coding=utf-8

from ..json_fb import typingon_json, json_message, json_photo
from ..json_fb import json_subscription
from chat import chat
from adopt.adopt import crawler, crawler2
from adopt.search1 import json_city, json_searchdogcat, json_searchbodytype
from adopt.search1 import json_location
from adopt.search2 import json_location2, json_city2, json_choosedogcat2
from db import upload_db_photo_url, upload_db_intro, upload_db_nickname, match
from db import get_flag, get_reci_id, get_nickname
from db import upload_flag, first_use, get_video
from video import deal_video
from imgur import upload_photo


def message_control(messaging_event, sender_id):
    if("text" in messaging_event["message"]):
        message_text = messaging_event["message"][
            "text"]  # the message's text
        print(sender_id)  # test
        if message_text == u'聊天':
            upload_flag(1, sender_id)
            json_message(
                sender_id, "我懂很多寵物知識喔\n你可以問我有關寵物領養 寵物健康 寵物食品的各種問題~")
        elif message_text == u'交換新明信片':
            upload_flag(20, sender_id)
            json_message(
                sender_id, "這是交換寵物明信片的小遊戲，藉由本汪這個郵差，讓您可以藉由明信片認識愛寵物的新朋友")
            json_message(sender_id, "返回上一頁，點擊傳送訊息，然後傳送一張照片")
        elif message_text == u'可愛寵物影片推播':
            upload_flag(3, sender_id)
            videos = get_video()
            deal_video(sender_id, videos)
            if first_use(sender_id, 3) == 1:
                json_subscription(sender_id)
        elif message_text == u'領養資訊搜尋':
            upload_flag(4, sender_id)
            json_location(sender_id)
        elif message_text == u'民間送養資訊搜尋':
            upload_flag(5, sender_id)
            json_choosedogcat2(sender_id)
        elif(get_flag(sender_id) == 1):
            chat(sender_id, message_text)
        elif(get_flag(sender_id) == 21):
            upload_flag(22, sender_id)
            upload_db_intro(message_text, sender_id)
            json_message(sender_id, "已收到，請輸入暱稱")
        elif(get_flag(sender_id) == 22):
            upload_db_nickname(message_text, sender_id)
            json_message(sender_id, "已完成，請耐心等待神秘的明信片")
            upload_flag(0, sender_id)
            match(sender_id)
        elif(get_flag(sender_id) == 4 or
             get_flag(sender_id) == 5):
            '''
        use payload to save the data which user send
        領養資訊搜尋：location->city->kind->body->start crawler
        民間送養資訊：kind->location->city-> start crawler
            '''
            if(message_text == u"北部地區" or message_text == u"中部地區" or message_text == u"南部地區" or message_text == u"東部地區"):
                payload = messaging_event["message"][
                    "quick_reply"]["payload"]
                print "payload={a}".format(a=payload)
                if(payload == "1" or payload == "2" or payload == "3" or payload == "4"):
                    json_city(sender_id, payload)
                else:
                    json_city2(sender_id, payload)
            elif(u"縣" in message_text or u"市" in message_text or message_text == u"北北基宜全部" or message_text == u"桃竹苗全部" or message_text == u"中彰投全部" or message_text == u"雲嘉南全部" or message_text == u"高屏全部" or message_text == u"花東全部"):
                payload = messaging_event["message"][
                    "quick_reply"]["payload"]
                if(len(payload) <= 5):
                    json_searchdogcat(sender_id, payload)
                else:
                    typingon_json(sender_id)
                    crawler2(sender_id, payload)
            elif(message_text == u"全部種類" or message_text == u"狗" or message_text == u"貓"):
                payload = messaging_event["message"][
                    "quick_reply"]["payload"]
                if(payload == "dog " or payload == "cat "):
                    json_location2(sender_id, payload)
                else:
                    json_searchbodytype(sender_id, payload)
            elif message_text == u"全部體型" or message_text == u"迷你型" or message_text == u"小型" or message_text == u"中型" or message_text == u"大型":
                typingon_json(sender_id)
                searchlist = messaging_event[
                    "message"]["quick_reply"]["payload"]
                crawler(sender_id, searchlist)

        elif get_flag(sender_id) == 6:
            reci_id = get_reci_id(sender_id)
            if reci_id == 'None':
                json_message(sender_id, '目前沒有配對到的好友喔，若要交朋友，請按功能表的交換新明信片')
            else:
                nickname = get_nickname(sender_id)
                message_text = nickname + ':' + message_text
                json_message(reci_id, message_text.encode('utf-8'))

    elif "attachments" in messaging_event["message"]:
        if get_flag(sender_id) == 20:
            for attachment in messaging_event["message"]["attachments"]:
                url = attachment["payload"]["url"]
            url = upload_photo(url)
            upload_db_photo_url(url, sender_id)
            upload_flag(21, sender_id)
            json_message(sender_id, "已收到圖片")
            json_message(sender_id, "請輸入簡單的明信片內容，給未知的寵物愛好者吧\n 例如")
            json_message(sender_id, "這是我家的可愛小狗，叫作蛋黃，他的尾巴超可愛的 對吧~")
            # 待補
        elif get_flag(sender_id) == 6:
            for attachment in messaging_event["message"]["attachments"]:
                url = attachment["payload"]["url"]
            url = upload_photo(url)
            reci_id = get_reci_id(sender_id)
            if get_flag(reci_id) == 6:
                json_photo(reci_id, url)
            else:
                json_photo(reci_id, url)
                message_text = 'by postcard'
                json_message(reci_id, message_text.encode('utf-8'))
