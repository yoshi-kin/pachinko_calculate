from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
    )
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
    )
from linebot.models import (
    StickerSendMessage, FollowEvent, PostbackEvent, MessageEvent,TextMessage, TextSendMessage, TemplateSendMessage, PostbackAction, ButtonsTemplate, MessageAction, URIAction, CarouselColumn, ImageComponent, FlexSendMessage, CarouselTemplate, BubbleContainer, QuickReply, QuickReplyButton, RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, MessageAction, URIAction, ImageCarouselTemplate, ImageCarouselColumn,
    ConfirmTemplate, BubbleContainer, ImageComponent, BoxComponent, TextComponent, SpacerComponent, IconComponent, ButtonComponent, SeparatorComponent
    )
from argparse import ArgumentParser
import os, sys, logging, re
import config
from machines import kamen, singaro
from module import is_int, is_float, regular_int, regular_float
from model import User


app = Flask(__name__)

# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.INFO)

line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)

users = {}
    
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(FollowEvent)
def on_follow(event):
    message = TextSendMessage(text='フォローありがとうございます。\
            こちらは「遊タイム期待値」を計算するボットになります。\
            「遊タイム期待値」とは、現在の回転数から「大当たりを引く」あるいは「遊タイム終了」まで打った場合の期待値です。\
                以降、打ち続ける場合は期待値が変わるので注意してください。\
            それではまず、機種を選んでみましょう。')
    
    line_bot_api.reply_message(
        event.reply_token,
        message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'おは':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='必須項目',
                text='タップして選択してください',
                actions=[
                    PostbackAction(
                        label='機種を選ぶ',
                        data = 'machine'
                    ),
                    PostbackAction(
                        label='現在回転数/回転率',
                        data = 'count_rate'
                    )
                ]
            )
        )
    elif regular_int(event.message.text) is not None:
        count = regular_int(event.message.text).group()
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text=f'現在の回転数は{count}ですね?',
                actions=[
                    PostbackAction(
                        label='はい',
                        data=count
                    ),
                    PostbackAction(
                        label='やり直す',
                        data='count_rate'
                    )
                ]
            )
        )
    elif regular_float(event.message.text) is not None:
        rate = regular_float(event.message.text).group()
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text=f'回転率は{rate}ですね?',
                actions=[
                    PostbackAction(
                        label='はい',
                        data=rate
                    ),
                    PostbackAction(
                        label='やり直す',
                        data='count_rate'
                    )
                ]
            )
        )
    else:
        message = TextSendMessage(text='入力が正しくありません。')

    line_bot_api.reply_message(
        event.reply_token,      
        message
    )

@handler.add(PostbackEvent)
def postback(event):
    userId = event.source.user_id
    if not userId in users:
        users[userId] = User(id=userId)
    
    if event.postback.data == 'machine':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='機種一覧',
                text='タップして選択してください',
                actions=[
                    PostbackAction(
                        label='Pぱちんこ仮面ライダー轟音M2',
                        data='Pぱちんこ仮面ライダー轟音M2'
                    ),
                    PostbackAction(
                        label='P真・牙狼',
                        data ='P真・牙狼'
                    ),
                ]
            )
        )
    elif event.postback.data == 'count_rate':
        if users[userId].machine == []:
            message = TextSendMessage(text='機種を設定してください。')
        else:
            message = TextSendMessage(
                text='「確変を除いた現在回転数」または「回転率」を入力して      い    ます。\
                        \
                       整数値を入力すると回転数、小数値を入力すると回転率を設定します。\
                        \
                       入力例）\
                       現在回転数が450の場合「450」\
                       回転率が18の場合「18.0」'
                    )
    elif 'P' in event.postback.data:
        users[userId].push_machine(event.postback.data)
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text=f'機種を設定しました。他の項目も設定しますか?',
                actions=[
                    PostbackAction(
                        label='はい',
                        data='count_rate'
                    ),
                    PostbackAction(
                        label='やり直す',
                        data='machine'
                    )
                ]
            )
        )
    elif is_int(event.postback.data):
        users[userId].push_count(event.postback.data)
        if users[userId].rate == []:
            message = TextSendMessage(text='続いて回転率を入力してください。')
        else:
            message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text=f"{users[userId].machine[-1]}、現在の回転数{users[userId].count[-1]}、回転率{users[userId].rate[-1]}。この条件で期待値を計算しますか？",
                actions=[
                    PostbackAction(
                        label='はい',
                        data='calculation'
                    ),
                    PostbackAction(
                        label='やり直す',
                        data='machine'
                    )
                ]
            )
        )
    elif is_float(event.postback.data):
        users[userId].push_rate(event.postback.data)
        if users[userId].count == []:
            message = TextSendMessage(text='続いて現在の回転数を入力してください。')
        else:
            message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text=f"{users[userId].machine[-1]}、現在の回転数{users[userId].count[-1]}、回転率{users[userId].rate[-1]}。この条件で期待値を計算しますか？",
                actions=[
                    PostbackAction(
                        label='はい',
                        data='calculation'
                    ),
                    PostbackAction(
                        label='やり直す',
                        data='machine'
                    )
                ]
            )
        )
    elif event.postback.data == 'calculation':
        if users[userId].machine[-1] == 'Pぱちんこ仮面ライダー轟音M2':
            func = kamen
        elif users[userId].machine[-1] == 'P真・牙狼':
            func = singaro
        message = TextSendMessage(text=f'期待値は{users[userId].calculate(func)}円です。')

    line_bot_api.reply_message(
            event.reply_token,      
            message
        )

if __name__ == '__main__':
    app.run()