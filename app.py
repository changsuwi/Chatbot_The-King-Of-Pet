# coding=utf-8
from lib.sendtofb_log import log
from lib.control.message_control import message_control
from lib.control.postback_control import postback_control
import os
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if (request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge")):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                if messaging_event.get("message"):  # someone sent us a message
                    # the facebook ID of the person sending you the message
                    message_control(messaging_event, sender_id)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    postback_control(messaging_event, sender_id)

    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True)
