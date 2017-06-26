from ..json_fb import json_template
import json
from ..sendtofb_log import sendtofb


def deal_video(recipient_id, videos):
    template = json_template(recipient_id)
    for x in range(0, 7):
        title = videos[x]['title']
        url = videos[x]['url']
        thumbnails = videos[x]['thumbnails']
        description = videos[x]['description']
        template = add_video(template, title, url, thumbnails, description)
    data = json.dumps(template)
    sendtofb(data)


def add_video(template, title, url, thumbnails, description):
    bobble = {
        "title": title,
        "image_url": thumbnails,
        "subtitle": description,
        "buttons":
            [
                {
                    "type": "web_url",
                    "url": url,
                    "title": "watch video"
                }
            ]
    }
    template["message"]["attachment"]["payload"]["elements"].append(bobble)
    return template
