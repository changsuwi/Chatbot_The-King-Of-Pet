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
                        json_searchlocation(sender_id)
                    elif(message_text==u"民間送養資訊搜尋"):
                        json_choosedogcat2(sender_id)
                    ###use payload to save the data which user send
                    ###location---> city ---> kind ---> body ---> start crawler
                    elif(message_text==u"北部地區" or message_text==u"中部地區" or message_text==u"南部地區" or message_text==u"東部地區"):
                        payload=messaging_event["message"]["quick_reply"]["payload"]
                        print "payload={a}".format(a=payload)
                        if(payload=="1" or payload=="2" or payload=="3" or payload=="4" ):
                            json_chooselocation(sender_id,payload)
                        else:
                            json_chooselocation2(sender_id,payload)
                        
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
                            json_searchlocation2(sender_id,payload)
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

def typingon_json(recipient_id): 
    
    #construct typing on json 
    log("sending  typingon to {recipient}".format(recipient=recipient_id))
    data = json.dumps({
            "recipient":{
                    "id": recipient_id
                    },
            "sender_action":"typing_on"})
            
    sendtofb(data)
        
def crawler(sender_id,searchlist):
    # the animal adoption imformation is crawlered by  http://animal-adoption.coa.gov.tw
    # this function construct a main template and start to crawler
    search=searchlist.split()
    print search
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
    res=requests.get("http://animal-adoption.coa.gov.tw/index.php/animal?s_area={area}&s_kind={kind}&s_bodytype={bodytype}&num=8&s_color=CHILD&s_color=ALL&s_sex=F".format(area=search[0].encode('utf-8'),kind=search[1].encode('utf-8'),bodytype=search[2]))
    soup = BeautifulSoup(res.text,"lxml") 
    count=0 #count the number of animal 
    for item in soup.select(".an"):
        count=count+1;
        location=item.select(".area")[0].text.encode("utf-8")
        gender=item.select(".gender")[0].text.encode("utf-8")
        shelter=item.select(".shelters")[0].text.encode("utf-8")
        item_url=item.select("a")[0].get('href')
        res2=requests.get(item_url)
        soup2 = BeautifulSoup(res2.text,"lxml") 
        for item2 in soup2.select(".carousel-inner"):
            image_url = item2.select("img")[0].get('src')
        template=add_template(template,location,gender,shelter,item_url,image_url) #find new imformation,so add this in the template
    
    if(count==0): #if number==0 can not find any animal
        json_message(sender_id,"嗚嗚嗚不好意思，找不到相對應的結果汪汪")
        json_message(sender_id,"可以試著放寬搜尋條件，或是看看是否有人想送養喔汪汪")
        json_mainbutton(sender_id)
    
    else: #finish the crawler and send data to json_template
        json_template(template,sender_id)
        json_message(sender_id,"找到了，我很厲害吧，給我骨頭嘛(搖尾)")
    
    
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
    
def json_searchlocation(recipient_id):
    log("sending searchlocation to {recipient}".format(recipient=recipient_id))
    data=json.dumps(
            {"recipient":{
    "id": recipient_id
    },
    "message":{
    "text":"請選擇地區:",
    "quick_replies":[
            {
                    "content_type":"text",
                    "title":"北部地區",
                    "payload":"1"
            },
            {
                    "content_type":"text",
                    "title":"中部地區",
                    "payload":"2"
            },
            {
                    "content_type":"text",
                    "title":"南部地區",
                    "payload":"3"
            },
            {
                    "content_type":"text",
                    "title":"東部地區",
                    "payload":"4"
            }
        ]
    
    }
    }
    )
    sendtofb(data)

def json_chooselocation(recipient_id,count):
    log("sending chooselocation to {recipient}".format(recipient=recipient_id))
    print "count={a}".format(a=count)
    if(count=="1"):
        data=json.dumps(
            {"recipient":{
                    "id": recipient_id
                    },
                "message":{
                        "text":"請選擇縣市:",
                        "quick_replies":[
                          {
                            "content_type":"text",
                            "title":"北北基宜全部",
                            "payload":u"北北基宜 "
                          },
                          {
                            "content_type":"text",
                            "title":"桃竹苗全部",
                            "payload":u"桃竹苗 "
                          },
                          {
                            "content_type":"text",
                            "title":"台北市",
                            "payload":"2 "
                          },
                          {
                            "content_type":"text",
                            "title":"新北市",
                            "payload":"3 "
                          },
                          {
                            "content_type":"text",
                            "title":"基隆市",
                            "payload":"4 "
                          },
                          {
                            "content_type":"text",
                            "title":"桃園市",
                            "payload":"6 "
                          },
                          {
                            "content_type":"text",
                            "title":"新竹縣",
                            "payload":"7 "
                          },
                          {
                            "content_type":"text",
                            "title":"新竹市",
                            "payload":"8 "
                          },
                          {
                            "content_type":"text",
                            "title":"苗栗縣",
                            "payload":"9 "
                          }
                           ]
                        }
                }
            )
    elif(count=="2"):
       data=json.dumps(
            {"recipient":{
                    "id": recipient_id
                    },
                "message":{
                        "text":"請選擇縣市:",
                        "quick_replies":[
                        {
                            "content_type":"text",
                            "title":"中彰投全部",
                            "payload":u"中彰投 "
                          },
                        {
                            "content_type":"text",
                            "title":"台中市",
                            "payload":"10 "
                          },
                          {
                            "content_type":"text",
                            "title":"彰化縣",
                            "payload":"11 "
                          },
                          {
                            "content_type":"text",
                            "title":"南投縣",
                            "payload":"12 "
                          },
                          {
                            "content_type":"text",
                            "title":"雲林縣",
                            "payload":"13 "
                          }
                                  ]
                        }
                    }
                )
    elif(count=="3"):
       data=json.dumps(
            {"recipient":{
                    "id": recipient_id
                    },
                "message":{
                        "text":"請選擇縣市:",
                        "quick_replies":[
                        {
                            "content_type":"text",
                            "title":"雲嘉南全部",
                            "payload":u"雲嘉南 "
                          },
                          {
                            "content_type":"text",
                            "title":"高屏全部",
                            "payload":u"高屏 "
                          },
                          {
                            "content_type":"text",
                            "title":"嘉義縣",
                            "payload":"14 "
                          },
                          {
                            "content_type":"text",
                            "title":"嘉義市",
                            "payload":"15 "
                          },
                          {
                            "content_type":"text",
                            "title":"台南市",
                            "payload":"16 "
                          },
                          {
                            "content_type":"text",
                            "title":"高雄市",
                            "payload":"17 "
                          },
                          {
                            "content_type":"text",
                            "title":"屏東縣",
                            "payload":"18 "
                          }
                                  ]
                        }
                    }
                )
    else:
        data=json.dumps(
            {"recipient":{
                    "id": recipient_id
                    },
                "message":{
                        "text":"請選擇縣市:",
                        "quick_replies":[
                           {
                            "content_type":"text",
                            "title":"北北基宜全部",
                            "payload":u"北北基宜 "
                          },
                          {
                            "content_type":"text",
                            "title":"花東全部",
                            "payload":u"花東 "
                          },
                          {
                            "content_type":"text",
                            "title":"宜蘭縣",
                            "payload":"5 "
                          },
                          {
                            "content_type":"text",
                            "title":"宜蘭縣",
                            "payload":"5 "
                          },
                          {
                            "content_type":"text",
                            "title":"花蓮縣",
                            "payload":"19 "
                          },
                          {
                            "content_type":"text",
                            "title":"台東縣",
                            "payload":"20 "
                          }
                                  ]
                        }
                    }
                )
    sendtofb(data)
    
def json_searchdogcat(recipient_id,payload):
    log("sending searchdogact to {recipient}".format(recipient=recipient_id))
    data=json.dumps(
            {"recipient":{
    "id": recipient_id
    },
    "message":{
    "text":"請選擇欲領養寵物的類型:",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"全部種類",
        "payload":payload + "ALL "
      },
      {
        "content_type":"text",
        "title":"狗",
        "payload":payload + u"狗 "
      },
      {
        "content_type":"text",
        "title":"貓",
        "payload":payload + u"貓 "
      },
      {
        "content_type":"text",
        "title":"其他 ",
        "payload":payload + u"其他 "
      }
    ]
  }
    }
    )
    sendtofb(data)

def json_searchbodytype(recipient_id,payload):
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
        "title":"全部體型",
        "payload":payload+"ALL "
      },
      {
        "content_type":"text",
        "title":"迷你型",
        "payload":payload+"MINI "
      },
      {
        "content_type":"text",
        "title":"小型",
        "payload":payload+"SMALL "
      },
      {
        "content_type":"text",
        "title":"中型",
        "payload":payload+"MEDIUM "
      },
      {
        "content_type":"text",
        "title":"大型",
        "payload":payload+"BIG "
      }
    ]
  }
    }
    )
    sendtofb(data)  
def json_choosedogcat2(recipient_id):
    log("sending searchdogact2 to {recipient}".format(recipient=recipient_id))
    data=json.dumps(
            {"recipient":{
    "id": recipient_id
    },
    "message":{
    "text":"請選擇欲領養寵物的類型:",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"狗",
        "payload":"dog "
      },
      {
        "content_type":"text",
        "title":"貓",
        "payload":"cat "
      }
    ]
  }
    }
    )
    sendtofb(data)
    
def json_searchlocation2(recipient_id,payload):
    log("sending searchlocation2 to {recipient}".format(recipient=recipient_id))
    data=json.dumps(
            {"recipient":{
    "id": recipient_id
    },
    "message":{
    "text":"請選擇地區:",
    "quick_replies":[
            {
                    "content_type":"text",
                    "title":"北部地區",
                    "payload":payload+"1 "
            },
            {
                    "content_type":"text",
                    "title":"中部地區",
                    "payload":payload+"2 "
            },
            {
                    "content_type":"text",
                    "title":"南部地區",
                    "payload":payload+"3 "
            },
            {
                    "content_type":"text",
                    "title":"東部地區",
                    "payload":payload+"4 "
            }
        ]
    
    }
    }
    )
    sendtofb(data)
def json_chooselocation2(recipient_id,payload):
    log("sending chooselocation2 to {recipient}".format(recipient=recipient_id))
    print "count={a}".format(a=payload[4])
    if(payload[4]=="1"):
        data=json.dumps(
            {"recipient":{
                    "id": recipient_id
                    },
                "message":{
                        "text":"請選擇縣市:",
                        "quick_replies":[
                          {
                            "content_type":"text",
                            "title":"台北市",
                            "payload":payload + u"台北市 "
                          },
                          {
                            "content_type":"text",
                            "title":"新北市",
                            "payload":payload + u"新北市 "
                          },
                          {
                            "content_type":"text",
                            "title":"基隆市",
                            "payload":payload + u"基隆市 "
                          },
                          {
                            "content_type":"text",
                            "title":"桃園市",
                            "payload":payload + u"桃園市 "
                          },
                          {
                            "content_type":"text",
                            "title":"新竹縣",
                            "payload":payload + u"新竹縣 "
                          },
                          {
                            "content_type":"text",
                            "title":"新竹市",
                            "payload":payload + u"新竹市 "
                          },
                          {
                            "content_type":"text",
                            "title":"苗栗縣",
                            "payload":payload + u"苗栗縣 "
                          }
                           ]
                        }
                }
            )
    elif(payload[4]=="2"):
       data=json.dumps(
            {"recipient":{
                    "id": recipient_id
                    },
                "message":{
                        "text":"請選擇縣市:",
                        "quick_replies":[
                        {
                            "content_type":"text",
                            "title":"台中市",
                            "payload":payload + u"台中市 "
                          },
                          {
                            "content_type":"text",
                            "title":"彰化縣",
                            "payload":payload + u"彰化縣 "
                          },
                          {
                            "content_type":"text",
                            "title":"南投縣",
                            "payload":payload + u"南投縣 "
                          },
                          {
                            "content_type":"text",
                            "title":"雲林縣",
                            "payload":payload + u"雲林縣 "
                          }
                                  ]
                        }
                    }
                )
    elif(payload[4]=="3"):
       data=json.dumps(
            {"recipient":{
                    "id": recipient_id
                    },
                "message":{
                        "text":"請選擇縣市:",
                        "quick_replies":[
                          {
                            "content_type":"text",
                            "title":"嘉義縣",
                            "payload":payload + u"嘉義縣 "
                          },
                          {
                            "content_type":"text",
                            "title":"嘉義市",
                            "payload":payload + u"嘉義市 "
                          },
                          {
                            "content_type":"text",
                            "title":"台南市",
                            "payload":payload + u"台南市 "
                          },
                          {
                            "content_type":"text",
                            "title":"高雄市",
                            "payload":payload + u"高雄市 "
                          },
                          {
                            "content_type":"text",
                            "title":"屏東縣",
                            "payload":payload + u"屏東縣 "
                          }
                                  ]
                        }
                    }
                )
    else:
        data=json.dumps(
            {"recipient":{
                    "id": recipient_id
                    },
                "message":{
                        "text":"請選擇縣市:",
                        "quick_replies":[
                          {
                            "content_type":"text",
                            "title":"宜蘭縣",
                            "payload":payload + u"宜蘭縣 "
                          },
                          {
                            "content_type":"text",
                            "title":"花蓮縣",
                            "payload":payload + u"花蓮縣 "
                          },
                          {
                            "content_type":"text",
                            "title":"台東縣",
                            "payload":payload + u"台東縣 "
                          }
                                  ]
                        }
                    }
                )
    sendtofb(data)
    
def crawler2(sender_id,searchlist):
    # the animal adoption imformation is crawlered by  http://animal-adoption.coa.gov.tw
    # this function construct a main template and start to crawler
    print searchlist.encode('utf-8')
    search=searchlist.split()
    print search
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
    res=requests.get("http://www.meetpets.org.tw/pets/{kind}?filter0={location}".format(location=search[2].encode('utf-8'),kind=search[0]))
    soup = BeautifulSoup(res.text,"lxml") 
    count=0 #count the number of animal 
    for item in soup.select(".item-list li"):
        count=count+1;
        title = item.select("a")[0].text.encode("utf-8")
        country = item.select(".view-data-node-data-field-county-field-county-value")[0].text.encode("utf-8")
        name = item.select(".view-data-node-data-field-pet-name-field-pet-name-value")[0].text.encode("utf-8")
        age = item.select(".view-data-node-data-field-pet-age-field-pet-age-value")[0].text.encode("utf-8")
        look = item.select(".view-data-node-data-field-pet-look-field-pet-look-value")[0].text.encode("utf-8")
        item_url="http://www.meetpets.org.tw"+item.select("a")[0].get('href')
        image_url=item.select("img")[0].get('src')
        template=add_template2(template,title,country,name,age,look,item_url,image_url) #find new imformation,so add this in the template

    if(count==0): #if number==0 can not find any animal
        json_message(sender_id,"嗚嗚嗚不好意思，找不到相對應的結果汪汪")
        json_message(sender_id,"可以試著放寬搜尋條件，或是看看是否有人想送養喔汪汪")
        json_mainbutton(sender_id)
    
    else: #finish the crawler and send data to json_template
        json_template(template,sender_id)
        json_message(sender_id,"找到了，我很厲害吧，給我骨頭嘛(搖尾)")
        
def add_template2(template,title,country,name,age,look,item_url,image_url):

    bobble={
        "title":title,
        "image_url":image_url,
        "subtitle":name + '\n' + country + '\n' + age + '\n' + look ,
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
