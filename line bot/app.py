import configparser
from flask import Flask, request, abort
import requests
from datetime import datetime,timedelta

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction,TemplateSendMessage,URITemplateAction,
)

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')


app = Flask(__name__)

line_bot_api = LineBotApi(config['LINE']['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['LINE']['CHANNEL_SECRET'])


def receive_data():
    try:
        data = requests.get('https://pm25.lass-net.org/data/last.php?device_id=1001000').json()['feeds'][0]['LASS']
    except:
        return "微型測站異常，修復中~拍謝"
    datetime_object = datetime.strptime(data['timestamp'].replace('T'," ").replace('Z',""), '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
    date_str = datetime_object.strftime('%Y{Y}%m{m}%d{d}%H{H}%M{M}%S{S}').format(Y='年',m='月',d='日',H='時',M='分',S=' 秒')
    if datetime.now() - datetime_object > timedelta(hours=1):
        return "微型測站離線中~請耐心等候QQ"
    else:
        return '''觀測時間：{}\nPM2.5: {}\nPM10: {}\nPM1.0: {}\n濕度: {}\n溫度: {}
                    '''.format(date_str,data['s_d0'],data['s_d1'],data['s_d2'],data['s_h0'],data['s_t0'])

try:
    line_bot_api.push_message('<to>', TextSendMessage(text=receive_data()+" 安安"))
except LineBotApiError as e:
    pass

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "天氣":

        content = receive_data()

        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
    if event.message.text:

        button_template_message =ButtonsTemplate(
                            actions=[
                                PostbackTemplateAction(
                                    label='查詢現在天氣吧',
                                    text='天氣',
                                    data=receive_data()
                                ),
                            ]
                        )

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="別錯過天氣即時資訊！",
                template=button_template_message,
            )
        )

'''

'''






if __name__ == "__main__":
    app.run()
