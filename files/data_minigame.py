# Susun Huruf Bot
# Created by: Pradipta Gitaya (Diptags)
# Dipsi Lala Po Studio (Padahal saya sendiri yang membuat)

# $ Python --version 
# $ Python 3.6.4

# -------------- Mini game -------------- #
import os
import random
import sys
import json
import requests
import time

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent)

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Otorisasi gagal ! Terapkan token LINE_CHANNEL_SECRET terlebih dahulu.')
    sys.exit(1)
if channel_access_token is None:
    print('Otorisasi gagal ! Terapkan token LINE_CHANNEL_ACCESS_TOKEN terlebih dahulu.')
    sys.exit(1)

susunhurufbot = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback(): # Webhook callback function

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


#--------------------------------------------------------#


# Menyusul 
class Minigame:
    pass






# Input center



# get channel_secret and channel_access_token from your environment variable



@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    inp_raw = event.message.text
    inp = inp_raw.lower()
    inp_split = inp.split()
    profile = susunhurufbot.get_profile(event.source.user_id)

    def reply_txt(msg):
        susunhurufbot.reply_message(event.reply_token,TextSendMessage(text=msg))

    def reply_img(link):
        susunhurufbot.reply_message(event.reply_token,ImageSendMessage(original_content_url=link,preview_image_url=link))

    if inp == '/help':
        carousel_template_message = TemplateSendMessage(
            alt_text='Bantuan umum',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item1.jpg',
                        title='Susun Kata Game',
                        text='Tap salah satu',
                        actions=[
                            MessageTemplateAction(
                                label='Mulai Sekarang',
                                text='/play'
                            ),
                            MessageTemplateAction(
                                label='Aturan Main',
                                text='/rule'
                            ),
                            MessageTemplateAction(
                                label='Leaderboards',
                                text='/leaderboard')]),

                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item4.jpg',
                        title='Lain - lain',
                        text='Tap salah satu',
                        actions=[
                            MessageTemplateAction(
                                label='Tentang admin',
                                text='/admin'
                            ),
                            MessageTemplateAction(
                                label='Keluarkan aku',
                                text='/leave'
                            ),
                            URITemplateAction(
                                label='Kirim feedback',
                                uri='http://s.id/FeedbackSusunHurufBot')])
                ]
            )
        )
        susunhurufbot.reply_message(event.reply_token, carousel_template_message)

# ------------------------------------------- Lain - Lain ------------------------------------------ #
    if inp == '/admin':
        about_button = TemplateSendMessage(
            alt_text='Info Admin',
            template=ButtonsTemplate(
                thumbnail_image_url='https://dl.dropboxusercontent.com/s/xjgb1az7tt7p7h3/admin_logo.png',
                title='Admin Susun Huruf Bot',
                text= 'Pradipta Gitaya (21 Tahun)',
                actions=[
                    MessageTemplateAction(
                        label='Hubungi Admin',
                        text= '/contactadmin' ),
                    MessageTemplateAction(
                        label='Catatan Admin',
                        text= '/adminnotes' ),]))

        susunhurufbot.reply_message(event.reply_token, about_button)

    elif inp == '/adminnotes':
        reply_txt(admin_note_msg)
    elif inp == '/contactadmin':
        reply_txt(about_msg)

    elif inp == '/leave':

        def kick():
            confirm_template = ConfirmTemplate(text='Keluarkan bot dari obrolan?', actions=[
                MessageTemplateAction(label='Iya', text='Pergi sana!'),
                MessageTemplateAction(label='Tidak', text='Jangan keluarkan!'),])
            template_message = TemplateSendMessage(alt_text='Konfirmasi kick', template=confirm_template)
            return susunhurufbot.reply_message(event.reply_token, template_message)
            
        if isinstance(event.source, SourceGroup):
            kick()
        
        elif isinstance(event.source, SourceRoom):
            kick()

        else:
            reply_txt('Ini chat 1:1 , gimana caranya aku bisa keluar dari sini coba :(')

    elif inp == ('Pergi sana!'.lower()): # Bot kick confirmation
        reply_txt('Sampai jumpa ~')

        if isinstance(event.source, SourceGroup):
            susunhurufbot.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            susunhurufbot.leave_room(event.source.room_id)

    elif inp == ('Jangan keluarkan!'.lower()): # Bot kick confirmation
        return 'OK'










status = True

while status:




