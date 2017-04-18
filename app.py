# coding=utf-8
from sendtofb_log import log
from json_fb import typingon_json,json_mainbutton,json_video,json_message
from crawler import crawler,crawler2
from search1 import json_location,json_city,json_searchdogcat,json_searchbodytype
from search2 import json_choosedogcat2,json_location2,json_city2
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
                    message_text = messaging_event["message"]["text"]  # the message's text
                    print(sender_id) #test
                    if(message_text=="Hello" or message_text=="Hi" or message_text==u"嗨" or message_text==u"妳好" or message_text==u"你好" or message_text=="hello" or message_text=="hi"):
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
                        json_message(sender_id, "我懂很多寵物知識喔\n你可以問我有關寵物領養 寵物健康 寵物食品的各種問題~")
                    
                    #http://petbird.tw/article12019.html
                    elif((u"領養" and(u"狗" or u"貓" or u"寵物")and (u"準備" or u"條件" or u"注意" )) in message_text):
                        json_message(sender_id, "1、有獨立經濟能力，年滿二十歲以上，男需役畢，若學生想領養，必須家裡支持。\n2、必須簽一式兩份領養切結書\n3、必須同意犬貓成年後進行結紮手術\n4、同意不定期追蹤\n5、與家人同住的申請人，需得到家庭成員同意。\n6、申請人需親自選定領養動物，不能他人代勞。\n7、申請人必須按政府的規定進行晶片輸入。\n8、需到合法獸醫處注射疫苗。")
                    
                    #http://petbird.tw/article13912.html
                    #http://petbird.tw/article14561.html
                    elif((u"照顧" and u"貓"and (u"幼" or u"小" or u"剛出生" )) in message_text):
                        json_message(sender_id, "適合餵食幼貓的小技巧\n1、可以使用湯匙\n2、用奶瓶來餵奶\n幼貓的生活注意事項\n")
                        json_message(sender_id, "1、衛生非常重要\n初生貓咪總是在窩裡排便，這時就需要主人特別注意窩內衛生，勤洗、勤換、勤消毒，保證貓窩的乾淨，以促進貓咪的健康成長。\n2、施打預防疫苗\n貓瘟病毒對四個月以下的小貓的危害性相當的大，一定要及時打疫苗，做好預防。接種疫苗的時間在小貓12周左右，一歲前共打兩次，兩次間隔20天，以後每年一次。\n3、適時補充水分\n不論是何種動物，水都是非常重要的，若是水分補充不足的話容易引起貓咪便秘，此點不管是幼貓或是成貓都是一樣的。幼貓還不會自己喝水，主人要適時為牠補充。")
                    
                    elif(message_text==u"可愛寵物影片推播"):
                        json_video(sender_id)
                    elif(message_text==u"領養資訊搜尋"):
                        json_location(sender_id)
                    elif(message_text==u"民間送養資訊搜尋"):
                        json_choosedogcat2(sender_id)
                    ###use payload to save the data which user send
                    ###領養資訊搜尋：location---> city ---> kind ---> body ---> start crawler
                    ###民間送養資訊：kind---> location---> city---> start crawler
                    elif(message_text==u"北部地區" or message_text==u"中部地區" or message_text==u"南部地區" or message_text==u"東部地區"):
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
                        
                    elif(message_text==u"全部體型" or message_text==u"迷你型" or message_text==u"小型" or message_text==u"中型" or message_text==u"大型"):
                        typingon_json(sender_id) 
                        searchlist=messaging_event["message"]["quick_reply"]["payload"] ###get payload
                        crawler(sender_id,searchlist)
                    else:
                        json_message(sender_id,"好的")
                        
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200




if __name__ == '__main__':
    app.run(debug=True)
