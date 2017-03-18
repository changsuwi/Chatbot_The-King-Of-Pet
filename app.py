# coding=utf-8
import os
import sys
import json
import random
import requests
from flask import Flask, request
from bs4 import BeautifulSoup
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
                    
                    elif(message_text==u"領養資訊搜尋"):
                        json_searchbodytype(sender_id)
                        ###typingon_json(sender_id)
                        ###crawler(sender_id)
                    elif(message_text==u"迷你型" or message_text==u"小型" or message_text==u"中型" or message_text==u"大型"):
                        typingon_json(sender_id)
                        bodytype=messaging_event["message"]["quick_reply"]["payload"]
                        crawler(sender_id,bodytype)
                    else:
                        json_message(sender_id,"好的")
                        
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def typingon_json(recipient_id): 
    
    #construct typing on json 
    log("sending  typingon to {recipient}".format(recipient=recipient_id))
    data = json.dumps({
            "recipient":{
                    "id": recipient_id
                    },
            "sender_action":"typing_on"})
            
    sendtofb(data)
    
def crawler(sender_id,bodytype):
    # the animal adoption imformation is crawlered by  http://animal-adoption.coa.gov.tw
    # this function construct a main template and start to crawler
    template = {
                    "recipient": {
                    "id": sender_id
                    },
                    "message":{
                        "attachment":{
                                "type":"template",
                                "payload":{
                                            "template_type":"generic",
                                            "elements":[
                                                    ]
                                            }
                                    }
                                }
                } 
    # start to crawler
    res=requests.get("http://animal-adoption.coa.gov.tw/index.php/animal?s_area=16&s_kind=%E7%8B%97&s_bodytype={bodytype}&num=8&s_color=CHILD&s_color=ALL&s_sex=F".format(bodytype=bodytype))
    soup = BeautifulSoup(res.text,"lxml") 
    for item in soup.select(".an"):
        location=item.select(".area")[0].text.encode("utf-8")
        gender=item.select(".gender")[0].text.encode("utf-8")
        shelter=item.select(".shelters")[0].text.encode("utf-8")
        image_url=item.select("img")[0].get('data-original')
        item_url=item.select("a")[0].get('href')
        template=add_template(template,location,gender,shelter,item_url,image_url) #find new imformation,so add this in the template
    json_template(template,sender_id)
    
    
def add_template(template,location,gender,shelter,item_url,image_url):
    #add new information in to the template
    bobble={
        "title":"寵物",
        "image_url":image_url,
        "subtitle":location + '\n' + gender+ '\n' + shelter,
        "buttons":
            [
                    {
                        "type":"web_url",
                        "url":item_url,
                        "title":"View Website"
                    }
            ]    
        } 
    template["message"]["attachment"]["payload"]["elements"].append(bobble)
    return template

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
        "title":"可愛寵物影片推播",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_MOVIE"
      },
      {
        "content_type":"text",
        "title":"領養資訊搜尋",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_ADOPTION"
      }
    ]
  }
    }
    )
    sendtofb(data)
def json_searchbodytype(recipient_id):
    log("sending searchbodytype to {recipient}".format(recipient=recipient_id))
    data=json.dumps(
            {"recipient":{
    "id": recipient_id
    },
    "message":{
    "text":"請選擇欲領養寵物的體型:",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"迷你型",
        "payload":"MINI"
      },
      {
        "content_type":"text",
        "title":"小型",
        "payload":"SMALL"
      },
      {
        "content_type":"text",
        "title":"中型",
        "payload":"MEDIUM"
      },
      {
        "content_type":"text",
        "title":"大型",
        "payload":"BIG"
      }
    ]
  }
    }
    )
    sendtofb(data)        
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

def sendtofb(data): #send json to facebook
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
