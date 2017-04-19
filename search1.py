# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:57:45 2017
search engine1 存放與領養資訊相關的json與打包
@author: vicharm
"""
from sendtofb_log import sendtofb
import json

def json_location(recipient_id):
    print("sending location to {recipient}".format(recipient=recipient_id))
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

def json_city(recipient_id,count):
    print("sending city to {recipient}".format(recipient=recipient_id))
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
    print("sending searchdogact to {recipient}".format(recipient=recipient_id))
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
    print("sending searchbodytype to {recipient}".format(recipient=recipient_id))
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
