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
                    #寵物領養須知問答
                    #http://petbird.tw/article12019.html
                    elif((u"領養" and(u"狗" or u"貓" or u"寵物")and (u"準備" or u"條件" or u"注意" )) in message_text):
                        json_message(sender_id, "1、有獨立經濟能力，年滿二十歲以上，男需役畢，若學生想領養，必須家裡支持。\n2、必須簽一式兩份領養切結書\n3、必須同意犬貓成年後進行結紮手術\n4、同意不定期追蹤\n5、與家人同住的申請人，需得到家庭成員同意。\n6、申請人需親自選定領養動物，不能他人代勞。\n7、申請人必須按政府的規定進行晶片輸入。\n8、需到合法獸醫處注射疫苗。")
                    #照顧剛出生 幼貓
                    #http://petbird.tw/article13912.html
                    #http://petbird.tw/article14561.html
                    elif(((u"照顧" or u"養")and u"貓"and (u"幼" or u"小" or u"剛出生" )) in message_text):
                        json_message(sender_id, "適合餵食幼貓的小技巧\n1、可以使用湯匙\n2、用奶瓶來餵奶\n")
                        json_message(sender_id, "幼貓的生活注意事項\n1、衛生非常重要\n初生貓咪總是在窩裡排便，這時就需要主人特別注意窩內衛生，勤洗、勤換、勤消毒。\n2、施打預防疫苗\n貓瘟病毒對四個月以下的小貓的危害性相當的大，一定要及時打疫苗。接種疫苗的時間在小貓12周左右，一歲前共打兩次，兩次間隔20天，以後每年一次。\n3、適時補充水分\n水分補充不足容易引起貓咪便秘，此點不管是幼貓或是成貓都是一樣的。幼貓還不會自己喝水，主人要適時為牠補充。")
                    
                    #教育貓
                    #http://www.ettoday.net/news/20140824/392823.htm
                    elif((u"貓" and (u"半夜" or u"晚上") and( u"吵" or u"叫")  )in message_text):#半夜亂叫
                        json_message(sender_id,"糾正深夜擾人的貓咪方法\n1、白天增新鮮感\n很怕貓咪到了半夜就會開始擾人，所以白天要增加牠的活動量，可以和牠玩遊戲，可以在窗邊擺貓跳台讓牠觀看風景，玩具要隔幾天就做更換，保持新鮮感才不會無聊。\n\n2、不要早上餵貓\n不要在早上餵貓咪吃東西，否則當吃飯的時間一到，牠一大早的就會喵喵叫得叫你起床，可以一天內分多次餵少量食物，沒人在家可以考慮用自動計時餵食器。\n\n3、發出聲響嚇牠\n在貓咪晚上要開始玩耍時，發出聲響嚇牠一跳，當次數多了，可矯正牠的行為，但不能讓貓咪發現聲響是你製造的，否則就沒有什麼效果了。\n\n4、忽視夜間行為\n主人必須做到完全忽視貓咪的夜間行為，吵著要你起床時要堅持住不去理牠，如果吵到一半就理牠，會讓牠覺得只要堅持住就一定能達到目的。")
                    elif((u"抓" and (u"家具" or u"傢俱" or u"傢具") and u"貓")in message_text):#亂抓傢具
                        json_message(sender_id,"訓練貓咪不亂抓家具\n1、習慣同一地方\n貓咪在抓物體的時候，喜歡在同一個地方或是同一個部位抓，這是因為貓腳上富含腺體，可分泌黏稠有味的液體，在抓的過程中，這些液體就會黏附上去吸引貓咪下次再過去抓。\n\n2、訓練方法技巧\n準備一根厚實堅硬的木柱，長約70公分、寬約20公分，直立固定在貓窩附近，從幼貓開始訓練，將牠帶到木柱前引領貓咪去抓木柱，多次訓練後就會養成貓咪的習慣了。\n\n3、對有前例的貓\n對於已經有養成抓家具習慣的貓，在訓練時，要先將那些被貓抓過的地方用塑膠板或是木板蓋上，在那些地方附近擺設木柱，用相同的方式，然後每天可移動一下木柱直到貓窩附近。")
                    #一般訓練
                    elif((u"貓" and (u"訓練" or u"教")  ) in message_text):
                        
                        json_message(sender_id,"一、訓練貓咪需要注意的事項\n1、可在飯前訓練\n為了吃東西你給予牠的要求牠會加快做到，因此在飯前訓練牠們效果是不錯的。\n2、要有耐心\n3、態度必須一致\n飼主的管教方式，不能輕易的因為別人的出現或建議而改變，因為這樣會引起寵物產生模式錯亂。\n4、不要動手動腳\n貓咪做錯事或是不聽話時，千萬不要用暴力對待牠\n5、了解貓咪性格\n要訓練貓咪之前要先搞清楚貓咪的個性，要針對牠的個性來訓練才能提高效率。當貓咪是屬於比較溫順的，這樣就適合溫柔的方式。")
                        json_message(sender_id,"二、錯誤的訓練貓咪方式\n1、事後斥責貓咪\n訓練貓咪時，應在貓咪犯錯的當下就告知牠，重複幾次之後貓咪就會知道哪裡不對，但是若是等事後才把貓咪帶到犯錯的地方責怪牠，貓咪會覺得莫明奇妙。\n2、不考慮牠心情\n貓咪如果覺得緊張或是對環境感到不安，牠會用爪子去攻擊周邊的人，因此在貓咪不熟悉的地方是很難訓練貓咪的。\n3、訓練過於急躁\n多給貓咪一些空間，一次訓練一種東西就好，否則他們也會非常沮喪，失去信心，對訓練只有扣分。")
                    #貓咪吐
                    #http://petbird.tw/article13607.html
                    elif((u"貓" and u"吐") in message_text):
                        json_message(sender_id,"一、貓咪出現嘔吐的原因\n1、飲食習慣造成\n例如吃太快或吃太多\n2、食物無法消化\n貓咪看到任何東西都會去啃咬，例如：地毯、衛生紙、塑膠袋、玩偶等等。而這些東西都不是貓咪能吃的，若誤食很可能會嘔吐。\n3、貓咪食物過敏\n有可能貓咪是對吃下去的食物裡含的某種成分過敏而嘔吐。注意貓咪如果吃到牛奶、雞蛋或是魚等等的食物很可能使貓咪嘔吐。\n4、貓咪感染中毒\n有可能是感染沙門氏菌，此時記得要馬上帶去給獸醫檢查。或是寄生蟲感染，因此要定期帶去給獸醫驅蟲。另外一種可能是貓咪不小心吃到處方藥導致中毒的現象。")
                        json_message(sender_id,"二、如何預防貓咪嘔吐\n1、避免讓貓誤食\n2、物品收拾乾淨\n3、定期獸醫檢查")
                    elif((u"貓" and (u"腹瀉" or u"拉肚子"))in message_text):
                        json_message(sender_id,"一、什麼原因導致貓咪腹瀉？\n1、食用變質食品\n。貓罐頭若是打開後沒馬上食用完畢，大概過個一小時裡面的食物就變得不新鮮了。\n2、貓咪運動不足\n沒有達到一定的運動量會造成貓咪的腸胃蠕動機能有所障礙，導致食物滯留在大腸裡\n3、改變飲食習慣\n若是突然更改食物可能會導致貓咪腸胃適應不良。或是飲食中沒有補充足夠的纖維，也會導致貓咪腸胃不舒服。")
                        json_message(sender_id,"二、如何治療貓咪腹瀉？\n1、何時去看獸醫\n如果貓咪持續腹瀉超過一天，或貓咪有嘔吐、嗜睡、發燒或是食慾不振，甚至是不明原因體重下降，那麼就必須去給獸醫檢查。\n2、給予足夠水分\n3、更改貓咪飲食\n可回想看看貓咪發生腹瀉前是吃了什麼食物，或是可能對那些食物過敏，避免再次攝入那些食物。可添加一些富含纖維的食物於貓罐頭或是貓糧中混合給貓咪吃或是額外添加益生菌，將有助於緩解腸道發炎及過敏反應。")
                        json_message(sender_id,"三、該如何預防貓咪腹瀉？\n1、別讓貓喝牛奶\n2、定期幫牠驅蟲\n大約每半年到一年定期幫貓咪驅蟲。\n3、改善飲食內容\n如果貓咪常常一換飼料就會拉肚子的話，那麼就減少飼料更換的次數，若是因為一些因素必須得更換的話，就採取循序漸進的方式，將少量比例的新飼料與舊飼料混合，之後慢慢將新飼料的比例提高使貓咪腸道有足夠的時間去適應。")
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
