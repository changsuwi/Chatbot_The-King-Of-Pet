# coding=utf-8
from sendtofb_log import log
from json_fb import typingon_json,json_mainbutton,json_video,json_message,get_start
from chat import chat
from crawler import crawler,crawler2
from search1 import json_location,json_city,json_searchdogcat,json_searchbodytype
from search2 import json_choosedogcat2,json_location2,json_city2
from imgur import upload_photo 
from db import upload_db_photo_url,upload_db_intro,upload_flag,get_flag
import os


import random

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])

def setup():
    get_start()

            
def webhook():
    
    
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    if(messaging_event["message"].has_key("text")):
                        message_text = messaging_event["message"]["text"]  # the message's text
                        print(sender_id) #test
                        if(message_text=="Hello" or message_text=="Hi" or message_text==u"嗨" or message_text==u"妳好" or message_text==u"你好" or message_text=="hello" or message_text=="hi" or message_text==u"哈囉"):
                            json_message(sender_id, "汪汪")
                            json_mainbutton(sender_id)
                        elif(message_text==u"幹" or message_text==u"靠杯" or message_text==u"靠北" or message_text==u"87"):
                            number=random.randint(0, 3)
                            if(number==0):
                                json_message(sender_id, "不給骨頭就咬你")
                            elif(number==1):
                                json_message(sender_id, "咬你喔")
                            elif(number==2):
                                json_message(sender_id,"嗚嗚")
                            elif(number==3):
                                json_message(sender_id,"87人類")
                        elif(message_text==u"聊天"):
                            upload_flag(1,sender_id)
                            json_message(sender_id, "我懂很多寵物知識喔\n你可以問我有關寵物領養 寵物健康 寵物食品的各種問題~")
                        
                        elif(message_text==u"交換明信片"):
                            upload_flag(2,sender_id)
                            json_message(sender_id,"請先傳送一張寵物的可愛照吧~")    
                        elif(message_text==u"可愛寵物影片推播"):
                            upload_flag(3,sender_id)
                            json_video(sender_id)
                        elif(message_text==u"領養資訊搜尋"):
                            upload_flag(4,sender_id)
                            json_location(sender_id)
                        elif(message_text==u"民間送養資訊搜尋"):
                            upload_flag(5,sender_id)
                            json_choosedogcat2(sender_id)
                        else:
                            if(get_flag(sender_id)==1):
                                chat(sender_id,message_text)
                            elif(get_flag(sender_id)==2):
                                upload_db_intro(message_text,sender_id)
                                json_message(sender_id,"已完成，請耐心等待神秘的明信片")
                            elif(get_flag(sender_id)==4 or get_flag(sender_id)==5):
                                ###use payload to save the data which user send
                                ###領養資訊搜尋：location---> city ---> kind ---> body ---> start crawler
                                ###民間送養資訊：kind---> location---> city---> start crawler
                                if(message_text==u"北部地區" or message_text==u"中部地區" or message_text==u"南部地區" or message_text==u"東部地區"):
                                    payload=messaging_event["message"]["quick_reply"]["payload"]
                                    print "payload={a}".format(a=payload)
                                    if(payload=="1" or payload=="2" or payload=="3" or payload=="4" ):
                                        json_city(sender_id,payload)
                                    else:
                                        json_city2(sender_id,payload)
                                    
                                elif(u"縣" in message_text or u"市" in message_text or message_text==u"北北基宜全部" or message_text==u"桃竹苗全部" or message_text==u"中彰投全部" or message_text==u"雲嘉南全部" or message_text==u"高屏全部" or message_text==u"花東全部"): 
                                    payload=messaging_event["message"]["quick_reply"]["payload"]
                                    if(len(payload)<=5):
                                        json_searchdogcat(sender_id,payload)
                                    else:
                                        typingon_json(sender_id) 
                                        crawler2(sender_id,payload)
                                elif(message_text==u"全部種類" or message_text==u"狗" or message_text==u"貓"): 
                                    payload=messaging_event["message"]["quick_reply"]["payload"]
                                    if(payload=="dog " or payload=="cat "):
                                        json_location2(sender_id,payload)
                                    else:
                                        json_searchbodytype(sender_id,payload)
                                    
                                elif(message_text==u"全部體型" or message_text==u"迷你型"  or message_text==u"中型" or message_text==u"大型"):
                                    typingon_json(sender_id) 
                                    searchlist=messaging_event["message"]["quick_reply"]["payload"] ###get payload
                                    crawler(sender_id,searchlist)
                
                        
                    elif(messaging_event["message"].has_key("attachments") and get_flag(sender_id)==2):
                        for attachment in messaging_event["message"]["attachments"]:
                            url=attachment["payload"]["url"]
                        url=upload_photo(url)
                        upload_db_photo_url(url,sender_id)
                        json_message(sender_id,"已收到圖片")
                        json_message(sender_id,"請輸入簡單的明信片內容，給未知的寵物愛好者吧\n 例如")
                        json_message(sender_id,"這是我家的可愛小狗，叫作蛋黃，他的尾巴超可愛的 對吧~")
                        # 待補
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200




if __name__ == '__main__':
    app.run(debug=True)
