# LINE Messaging API SDK for Python
# https://github.com/line/line-bot-sdk-python
#
import os
import Menu_tool
import Text_analysis
# sudo pip install flask/**-
from flask import Flask, request, abort
# sudo pip install line-bot-sdk
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction, PostbackEvent, Postback
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'J2xZ4vuq5g9lOU5lOz4n+Fkvskqo6A6AOqiHbdFjS8e/ZWO3qSD0ZWzjiVR5K4BdC+qyeR8zzYMNjJdZak/IBL//aMqW4MZAMWhvM/CiXrCA+0+CmVZT6se1XuaxKLhsE6Myg6fiaqekfM7EU7qziQdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '84630545053bcbab5fd772a5cc521c21'
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print 'request body' info 
    app.logger.info("Request body: " + body)
    print("Request body: %s" % body)
    # handle webhook body
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        Text_analysis.select_tool(event.message.text))
        
        



@handler.add(PostbackEvent)
def handle_postback(event):
        line_bot_api.reply_message(
        event.reply_token,
        Text_analysis.select_postback(event.postback.data))

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080))) 