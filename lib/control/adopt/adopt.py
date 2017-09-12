# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:47:55 2017
crawler 主要是兩種爬蟲引擎
@author: vicharm
"""
import requests
import json
from ...json_fb import json_message, json_template, json_mainbutton
from ...sendtofb_log import sendtofb
from bs4 import BeautifulSoup


def crawler(sender_id, searchlist):
    # http://animal-adoption.coa.gov.tw
    # this function construct a main template and start to crawler
    search = searchlist.split()
    print search
    template = json_template(sender_id)
    # start to crawler
    res = requests.get("http://animal-adoption.coa.gov.tw/index.php/animal?s_area={area}&s_kind={kind}&s_bodytype={bodytype}&num=8&s_color=CHILD&s_color=ALL&s_sex=F".format(
        area=search[0].encode('utf-8'), kind=search[1].encode('utf-8'), bodytype=search[2]))
    soup = BeautifulSoup(res.text, "lxml")
    count = 0  # count the number of animal
    for item in soup.select(".an"):
        count = count + 1
        city = item.select(".area")[0].text.encode("utf-8")
        gender = item.select(".gender")[0].text.encode("utf-8")
        shelter = item.select(".shelters")[0].text.encode("utf-8")
        item_url_desktop = item.select("a")[0].get('href')
        id_num_in_str = item_url_desktop.find('id')
        item_id = item_url_desktop[id_num_in_str + 3: id_num_in_str + 7]
        item_url = 'http://animal-adoption.coa.gov.tw/index.php/mobile/index/animal_info/?id=' + item_id
        image_url = item.select("img")[0].get('data-original')
        # find new imformation,so add this in the template
        template = add_template(template, city, gender,
                                shelter, item_url, image_url)

    if(count == 0):  # if number==0 can not find any animal
        json_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果汪汪")
        json_message(sender_id, "可以試著放寬搜尋條件，或是看看是否有人想送養喔汪汪")
        json_mainbutton(sender_id)

    else:  # finish the crawler and send data to json_template
        data = json.dumps(template)
        sendtofb(data)
        json_message(sender_id, "找到了，我很厲害吧，給我骨頭嘛(搖尾)")


def add_template(template, city, gender, shelter, item_url, image_url):
    # add new information in to the template
    bobble = {
        "title": "寵物",
        "image_url": image_url,
        "subtitle": city + '\n' + gender + '\n' + shelter,
        "buttons":
            [
                {
                    "type": "web_url",
                    "url": item_url,
                    "title": "View Website"
                }
            ]
    }
    template["message"]["attachment"]["payload"]["elements"].append(bobble)
    return template


def crawler2(sender_id, searchlist):
    # http://animal-adoption.coa.gov.tw
    # this function construct a main template and start to crawler
    print searchlist.encode('utf-8')
    search = searchlist.split()
    print search
    template = json_template(sender_id)
    # start to crawler
    res = requests.get("http://www.meetpets.org.tw/pets/{kind}?filter0={city}".format(
        city=search[2].encode('utf-8'), kind=search[0]))
    soup = BeautifulSoup(res.text, "lxml")
    count = 0  # count the number of animal
    for item in soup.select(".item-list li"):
        count = count + 1
        title = item.select("a")[0].text.encode("utf-8")
        country = item.select(
            ".view-data-node-data-field-county-field-county-value")[0].text.encode("utf-8")
        name = item.select(
            ".view-data-node-data-field-pet-name-field-pet-name-value")[0].text.encode("utf-8")
        age = item.select(
            ".view-data-node-data-field-pet-age-field-pet-age-value")[0].text.encode("utf-8")
        look = item.select(
            ".view-data-node-data-field-pet-look-field-pet-look-value")[0].text.encode("utf-8")
        item_url = "http://www.meetpets.org.tw" + \
            item.select("a")[0].get('href')
        image_url = item.select("img")[0].get('src')
        # find new imformation,so add this in the template
        template = add_template2(
            template, title, country, name, age, look, item_url, image_url)
        if count >= 7:
            break

    if(count == 0):  # if number==0 can not find any animal
        json_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果汪汪")
        json_message(sender_id, "可以試著放寬搜尋條件，或是看看是否有人想送養喔汪汪")
        json_mainbutton(sender_id)

    else:  # finish the crawler and send data to json_template
        data = json.dumps(template)
        sendtofb(data)
        json_message(sender_id, "找到了，我很厲害吧，給我骨頭嘛(搖尾)")


def add_template2(template, title, country, name, age, look, item_url, image_url):

    bobble = {
        "title": title,
        "image_url": image_url,
        "subtitle": name + '\n' + country + '\n' + age + '\n' + look,
        "buttons":
            [
                {
                    "type": "web_url",
                    "url": item_url,
                    "title": "View Website"
                }
            ]
    }
    template["message"]["attachment"]["payload"]["elements"].append(bobble)
    return template
