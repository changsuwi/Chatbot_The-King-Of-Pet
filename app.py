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
                    print(sender_id)
                    if(message_text=="Hello" or message_text=="Hi" or message_text==u"嗨" or message_text==u"妳好" or message_text==u"你好" or message_text=="hello" or message_text=="hi"):
                        send_message(sender_id, "汪汪")
                    elif(message_text==u"幹" or message_text==u"靠杯" or message_text==u"靠北" or message_text==u"87"):
                        number=random.randint(0, 3)
                        if(number==0):
                            send_message(sender_id, "不給骨頭就咬你")
                        elif(number==1):
                            send_message(sender_id, "咬你喔")
                        elif(number==2):
                            send_message(sender_id,"嗚嗚")
                        elif(number==3):
                            send_message(sender_id,"87人類")
                    else:
                        res=requests.get("http://animal-adoption.coa.gov.tw/index.php/animal")
                        soup = BeautifulSoup(res.text,"lxml") 
                        send_message(sender_id, "1111")
                        for item in soup.select(".an"):
                             location=item.select(".area")[0].text.encode("utf-8")
                             gender=item.select(".gender")[0].text.encode("utf-8")
                             shelter=item.select(".shelters")[0].text.encode("utf-8")
                             image_url=item.select(".img")[0].get('data-original')
                             item_url="https://petersfancybrownhats.com"
                             send_template(sender_id,location,gender,shelter,item_url,image_url)
                             
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def send_template(recipient_id,location,gender,shelter,item_url,image_url):
    log("sending  to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                "template_type":"generic",
                "elements":[
                     {
                    "title":"寵物",
                    "item_url":"https://petersfancybrownhats.com",
                    "image_url":image_url,
                    "subtitle":location + '\n' + gender + '\n' + shelter,
                    "buttons":[
                         {
                        "type":"web_url",
                        "url":"https://petersfancybrownhats.com",
                        "title":"View Website"
                         },
                         {
                            "type":"postback",
                            "title":"Start Chatting",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                          }              
                        ]
                      }
                    ]
                  }
                }
              }
            }
        )
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        
def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
