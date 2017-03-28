# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:25:14 2017
search engine two 存放與送養資訊相關的json 與 打包
@author: vicharm
"""
from sendtofb_log import sendtofb,log
import json
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
    
def json_location2(recipient_id,payload):
    log("sending location2 to {recipient}".format(recipient=recipient_id))
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
def json_city2(recipient_id,payload):
    log("sending city2 to {recipient}".format(recipient=recipient_id))
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