# coding=utf-8

from ..json_fb import json_mainbutton, json_message, json_photo
from ..json_fb import json_subscription, json_ask_reply_mail, json_del_friend
from adopt.search1 import json_location
from adopt.search2 import json_choosedogcat2
from video import deal_video
from db import upload_flag, get_mail
from db import deal_subscription, get_video, first_use
from db import del_friend, get_reci_id


def postback_control(messaging_event, sender_id):
    if messaging_event["postback"]["payload"] == 'GET_STARTED_PAYLOAD':
        upload_flag(0, sender_id)
        json_message(sender_id, "汪汪，我是聊天機器狗～～我會做很多事喔")
        json_message(sender_id, "寵物顧問：可以問我寵物問題，我會給你解答的～")
        json_message(sender_id, "交換明信片：用明信片來認識愛寵物的新朋友吧～")
        json_message(sender_id, "寵物影片推播：幫你找可愛的寵物影片")
        json_message(sender_id, "領養資訊搜尋：找收容所的領養資訊")
        json_message(sender_id, "送養資訊搜尋：找民間送養的資訊")
        json_mainbutton(sender_id)
    elif messaging_event["postback"]["payload"] == 'main_button1':
        upload_flag(1, sender_id)
        json_message(
            sender_id, "我懂很多寵物知識喔\n你可以問我有關寵物領養 寵物健康 寵物食品的各種問題~")
        json_message(
            sender_id, "若不需要再詢問寵物知識，可點選右下角功能表選擇別的功能喔汪汪～")
    elif messaging_event["postback"]["payload"] == 'main_button2':
        upload_flag(2, sender_id)
        json_message(sender_id, "這是交換寵物明信片的小遊戲，藉由本汪這個郵差，讓您可以藉由明信片認識愛寵物的新朋友")
        json_message(sender_id, "點擊傳送訊息，然後傳送一張照片")
    elif messaging_event["postback"]["payload"] == 'main_button3':
        upload_flag(3, sender_id)
        videos = get_video()
        deal_video(sender_id, videos)
        if first_use(sender_id, 3) == 1:
            json_subscription(sender_id)
        json_message(
            sender_id, "若要使用其他功能，可點選右下角功能表選擇別的功能喔汪汪～")
    elif messaging_event["postback"]["payload"] == 'main_button4':
        upload_flag(4, sender_id)
        json_location(sender_id)
    elif messaging_event["postback"]["payload"] == 'main_button5':
        upload_flag(5, sender_id)
        json_choosedogcat2(sender_id)
    elif messaging_event["postback"]["payload"] == 'main_button6':
        reci_id = get_reci_id(sender_id)
        if reci_id == 'None':
            json_message(sender_id, '目前沒有配對到的好友喔，若要交朋友，請按功能表的交換新明信片')
        else:
            upload_flag(6, sender_id)
            json_message(sender_id, "返回功能表上一頁，點選傳送訊息，輸入想說的話或圖片，本汪就會幫你寄過去的呦")
    elif messaging_event["postback"]["payload"] == 'main_button7':
        '''
        還需新增一個狀況 若沒使用過交換明信片的功能，就點擊刪除好友，會有bug
        '''
        if get_reci_id(sender_id) == 'None':
            json_message(sender_id, "目前無可刪除的明信片好友")
        else:
            upload_flag(7, sender_id)
            json_message(sender_id, "若刪除明信片好友，未來將無法與該位好友取得聯繫")
            json_del_friend(sender_id)
    elif messaging_event["postback"]["payload"] == 'main_button8':
        json_subscription(sender_id)

    elif messaging_event['postback']['payload'] == 'get_match_mail':
        user_mail = get_mail(sender_id)
        friend_mail = get_mail(user_mail['match_id'])
        intro = friend_mail['intro']
        img_url = friend_mail['url']
        json_photo(sender_id, img_url)
        json_message(sender_id, intro.encode('utf-8'))
        json_ask_reply_mail(sender_id)
    elif messaging_event['postback']['payload'] == 'subscription_yes':
        deal_subscription(sender_id, 1)
        json_message(sender_id, "訂閱完成，固定推播寵物影片時間為每晚八點")
    elif messaging_event['postback']['payload'] == 'subscription_no':
        deal_subscription(sender_id, 0)
        json_message(
            sender_id, "好的，若未來有需要訂閱，點選功能表->\n寵物影片/領養資訊\n影片訂閱/取消訂閱")
    # elif messaging_event['postback']['payload'] == 'reply_yes':
    #     json_message(
    #         sender_id, "未來只要點選\n功能表-->\n與明信片朋友聊天\n就可以傳送訊息給明信片朋友喔")
    #     json_message(
    #         sender_id, "若不想與對方聊天了，點選斷絕往來即可，了解了嗎？")
    #     json_message(
    #         sender_id, "那麼本汪已準備好，幫你寄信拉～ 現在只要輸入想說的話，都會傳送到對方那喔")
    # elif messaging_event['postback']['payload'] == 'reply_no':
    #     json_message(
    #         sender_id, "好的，若未來想要聊天時，只要點選\n功能表-->\n與明信片朋友聊天\n就可以傳送訊息給明信片朋友喔")
    #     upload_flag(0, sender_id)

    elif messaging_event['postback']['payload'] == 'del_yes':
        del_friend(sender_id)
        json_message(sender_id, "已刪除，若想交換新明信片認識好友，請再點選\n功能表->交換明信片->交換明信片")
    elif messaging_event['postback']['payload'] == 'del_no':
        del_friend(sender_id)
        json_message(sender_id, "好的，若未來想刪除，請再點選功能表->\n刪除明信片好友")
