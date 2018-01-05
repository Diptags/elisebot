# Elisé (Chat Bot)
# Created by: Pradipta Gitaya (Diptags)
# Dipsi Lala Po Studio (Padahal saya sendiri yang membuat)

# $ Python --version 
# $ Python 3.6.4

import os
import random
import sys
import json
import goslate
import requests

from files.data_foodcorner import * # Import file eksternal
from files.data_longmsg import * # Import file eksternal
from time import sleep
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

# get channel_secret and channel_access_token from your environment variable

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Otorisasi gagal ! Terapkan token LINE_CHANNEL_SECRET terlebih dahulu.')
    sys.exit(1)
if channel_access_token is None:
    print('Otorisasi gagal ! Terapkan token LINE_CHANNEL_ACCESS_TOKEN terlebih dahulu.')
    sys.exit(1)

elisebot = LineBotApi(channel_access_token)
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


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    inp_raw = event.message.text
    inp = inp_raw.lower()
    inp_split = inp.split()
    profile = elisebot.get_profile(event.source.user_id)

    def reply_txt(msg):
        elisebot.reply_message(event.reply_token,TextSendMessage(text=msg))

    def reply_img(link):
        elisebot.reply_message(event.reply_token,ImageSendMessage(original_content_url=link,preview_image_url=link))

# ---------------------- Program Execution ---------------------- #

    keyword = ['/newprofile','/bantuan','/help','/keyword','/leave','/myprofile','/sleep','/quotes','/weather','/translate','/movie','/admin','/adminnotes','/contactadmin','/lifehacks','/foodcorner','/weather']

    if inp == '/help':
        carousel_template_message = TemplateSendMessage(
            alt_text='Bantuan umum',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item1.jpg',
                        title='Keseharian hidup',
                        text='Tap salah satu',
                        actions=[
                            MessageTemplateAction(
                                label='Mini game',
                                text='/minigame'
                            ),
                            MessageTemplateAction(
                                label='Kumpulan quotes',
                                text='/quotes'
                            ),
                            MessageTemplateAction(
                                label='Resep hidangan',
                                text='/foodcorner')]),

                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item2.jpg',
                        title='Utilitas & Kegiatan',
                        text='Tap salah satu',
                        actions=[
                            MessageTemplateAction(
                                label='Kalkulator',
                                text='/calculator'
                            ),
                            MessageTemplateAction(
                                label='Info cuaca',
                                text='/weather'
                            ),
                            MessageTemplateAction(
                                label='Terjemahan bahasa',
                                text='/translate')]),

                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item3.jpg',
                        title='Hiburan Seru',
                        text='Tap salah satu',
                        actions=[
                            MessageTemplateAction(
                                label='Film terbaru',
                                text='/movies'
                            ),
                            MessageTemplateAction(
                                label='Mode kerang ajaib',
                                text='/kerang'
                            ),
                            MessageTemplateAction(
                                label='Kumpulan meme',
                                text='/meme')]),

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
                                uri='http://s.id/FeedbackBot')])
                ]
            )
        )
        elisebot.reply_message(event.reply_token, carousel_template_message)

    elif inp == '/keyword': # Menampilkan help untuk device yang tidak support button dan carousel
        reply_txt(help_msg)

# ------------------------------------------------------------------------------- #
    elif inp == '/minigame':
        reply_txt("Elisé masih belajar bermain kak, ditunggu aja ya ^.^")

    elif inp == '/myprofile':

        myprofile_msg = '''Profil kakak nih~
Nama: {}
Status: {}'''.format(profile.display_name,profile.status_message)

        if isinstance(event.source, SourceUser):
            reply_txt(myprofile_msg)
        else:
            reply_txt("Adek hanya bisa menampilkan via PM")
        
    elif inp == '/quotes':
        file_path = 'files/'

        with open(os.path.join(os.path.dirname(__file__),file_path,\
            'kata_mutiara.txt'),'r') as data:
            lst_quotes_raw = data.readlines()
        lst_quotes = [x.strip() for x in lst_quotes_raw]
        reply_txt(random.choice(lst_quotes))

    elif inp == '/translate':
            reply_txt(trans_msg)

    elif inp_split[0] == 'terjemahkan':

        supported_lang = ['id','en']
        supported_lang_dict = {'id':'indonesia','en':'inggris'}
    
        if (len(inp_split)) > 2 and inp_split[1] in supported_lang:
            trans = goslate.Goslate()
            msg = (' '.join(inp_split[2:]))

            final_msg = trans.translate(msg,inp_split[1])
            reply_txt(final_msg)

        elif (len(inp_split)) > 2 and inp_split[1] not in supported_lang:
            reply_txt("Maaf kak, aku nggak tahu :(")
        
        else:
            reply_txt('''Ada yang salah kak, ini formatnya:
terjemahkan <spasi> bahasa tujuan <spasi> Kalimat yang mau diterjemahkan
''')
# ------------------------------------------------------------------------------- #
    elif inp == '/kerang':
        reply_txt(kerang_msg)

    elif inp_split[0] == 'apakah' or inp_split[0] == 'apa':
        reply_txt(random.choice(kerang_jawab))
# ------------------------------------------------------------------------------- #
    elif inp == '/foodcorner':
        if isinstance(event.source, SourceUser):
            recipe_button = TemplateSendMessage(
                alt_text='Kumpulan resep hidangan',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://dl.dropboxusercontent.com/s/nbgcfzvob2z6xt4/FoodCorner.png',
                    title='Kumpulan resep hidangan',
                    text= 'Cocok untuk kakak jika sedang lapar dan bingung',
                    actions=[
                        MessageTemplateAction(
                            label='Makanan ala anak kos',
                            text= '/kosrecipe'),
                        MessageTemplateAction(
                            label='Kue & camilan',
                            text= '/cakerecipe' ),
                        MessageTemplateAction(
                            label='Hidangan lainnya',
                            text= '/otherrecipe')]))

            elisebot.reply_message(event.reply_token, recipe_button)
        else:
            reply_txt("Fitur ini cuma bisa lewat PM, kak. Coba lagi ya")

    elif inp == '/kosrecipe':
        if isinstance(event.source, SourceUser):
            carousel_template_message = TemplateSendMessage(
                alt_text='Resep Ala anak kos',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://dl.dropboxusercontent.com/s/srfm9l8ucimj594/hidangan_logo.jpg.png',
                            title='Resep Ala anak kos 1',
                            text='Tap salah satu di bawah',
                            actions=[
                                MessageTemplateAction(
                                    label='Omelet telur',
                                    text='elise mau makanan a1'),
                                MessageTemplateAction(
                                    label='Sup sayur',
                                    text='elise mau makanan a2'),
                                MessageTemplateAction(
                                    label='Pangsit sosis telur',
                                    text='elise mau makanan a3')]),
                        CarouselColumn(
                            thumbnail_image_url='https://dl.dropboxusercontent.com/s/srfm9l8ucimj594/hidangan_logo.jpg.png',
                            title='Resep Ala anak kos 2',
                            text='Tap salah satu di bawah',
                            actions=[
                                MessageTemplateAction(
                                    label='Roti telur lunak',
                                    text='elise mau makanan a4'),
                                MessageTemplateAction(
                                    label='Nasi goreng',
                                    text='elise mau makanan a5'),
                                MessageTemplateAction(
                                    label='Roti maryam/canai',
                                    text='elise mau makanan a6')])]))
                                    
            elisebot.reply_message(event.reply_token, carousel_template_message)
        else:
            reply_txt("Fitur ini cuma bisa lewat PM, kak. Coba lagi ya")

    elif inp == '/cakerecipe':
        if isinstance(event.source, SourceUser):
            carousel_template_message = TemplateSendMessage(
                alt_text='Resep Kue & Camilan',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://dl.dropboxusercontent.com/s/srfm9l8ucimj594/hidangan_logo.jpg.png',
                            title='Resep kue & camilan 1',
                            text='Tap salah satu di bawah',
                            actions=[
                                MessageTemplateAction(
                                    label='Oreo cake',
                                    text='elise mau makanan b1'),
                                MessageTemplateAction(
                                    label='Nugget pisang',
                                    text='elise mau makanan b2'),
                                MessageTemplateAction(
                                    label='Bolu kukus',
                                    text='elise mau makanan b3')]),
                        CarouselColumn(
                            thumbnail_image_url='https://dl.dropboxusercontent.com/s/srfm9l8ucimj594/hidangan_logo.jpg.png',
                            title='Resep kue & camilan 2',
                            text='Tap salah satu di bawah',
                            actions=[
                                MessageTemplateAction(
                                    label='Rainbow cake',
                                    text='elise mau makanan b4'),
                                MessageTemplateAction(
                                    label='Bakwan jamur',
                                    text='elise mau makanan b5'),
                                MessageTemplateAction(
                                    label='Roti maryam/canai',
                                    text='elise mau makanan b6')])]))
                                    
            elisebot.reply_message(event.reply_token, carousel_template_message)
        else:
            reply_txt("Fitur ini cuma bisa lewat PM, kak. Coba lagi ya")

    elif inp == '/otherrecipe':
        if isinstance(event.source, SourceUser):
            carousel_template_message = TemplateSendMessage(
                alt_text='Hidangan lainnya',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://dl.dropboxusercontent.com/s/srfm9l8ucimj594/hidangan_logo.jpg.png',
                            title='Resep lainnya 1',
                            text='Tap salah satu di bawah',
                            actions=[
                                MessageTemplateAction(
                                    label='Mango thai/juice',
                                    text='elise mau makanan c1'),
                                MessageTemplateAction(
                                    label='Macaroni Schotel',
                                    text='elise mau makanan c2'),
                                MessageTemplateAction(
                                    label='Seblak pedas',
                                    text='elise mau makanan c3')]),
                        CarouselColumn(
                            thumbnail_image_url='https://dl.dropboxusercontent.com/s/srfm9l8ucimj594/hidangan_logo.jpg.png',
                            title='Resep lainnya 2',
                            text='Tap salah satu di bawah',
                            actions=[
                                MessageTemplateAction(
                                    label='Mocktail blue & red',
                                    text='elise mau makanan c4'),
                                MessageTemplateAction(
                                    label='Matcha latte',
                                    text='elise mau makanan c5'),
                                MessageTemplateAction(
                                    label='Sate taichan',
                                    text='elise mau makanan c6')])]))
                                    
            elisebot.reply_message(event.reply_token, carousel_template_message)
        else:
            reply_txt("Fitur ini cuma bisa lewat PM, kak. Coba lagi ya")

    elif inp_split[0:3] == ['elise', 'mau', 'makanan']:           
        if isinstance(event.source, SourceUser):
            food_var = inp_split[3]

            if food_var in food_dict:
                reply_txt(food_dict[food_var])
            else:
                reply_txt("Maaf kak belum ada resepnya :(")
        else:
            reply_txt("Fitur ini cuma bisa lewat PM, kak. Coba lagi ya")
# ------------------------------------------------------------------------------- #
    elif inp == '/calculator':
        reply_txt(calc_msg)
    
    elif inp_split[0:2] == ['hitung','dong']:
        menghitung = inp[12:]
        try:
            reply_txt("Hasilnya: {}".format(eval(menghitung)))
        except ZeroDivisionError:
            reply_txt("Adek nggak bisa kak")
        except:
            reply_txt("Formatnya salah kak, coba lagi ya")

    elif inp == '/movies':
        reply_txt('Fitur ini menyusul ya kak~ ^.^')

    elif inp == '/weather':
        reply_txt('Fitur ini menyusul ya kak~ ^.^')

    elif inp == '/meme':
        reply_txt('Fitur ini menyusul ya kak~ ^.^')

# ------------------------------------------------------------------------------- #
    elif inp == 'tes' or inp == 'testing' or inp == 'test' or inp == 'tess' or inp == 'tes saja' or inp == 'tes aja':
        reply_txt('Aku udah aktif kak.. 1.. 2.. 3..')
# --------------------------------------------------------------- #
    elif inp == '/leave':

        def kick():
            confirm_template = ConfirmTemplate(text='Keluarkan Elisé dari obrolan?', actions=[
                MessageTemplateAction(label='Iya', text='Pergi sana!'),
                MessageTemplateAction(label='Tidak', text='Jangan keluarkan!'),])
            template_message = TemplateSendMessage(alt_text='Konfirmasi kick', template=confirm_template)
            return elisebot.reply_message(event.reply_token, template_message)
            
        if isinstance(event.source, SourceGroup):
            kick()
        
        elif isinstance(event.source, SourceRoom):
            kick()

        else:
            reply_txt('Kakak nggak bisa usir adek :P kakak aja yang pergi ya (^.^)/')

    elif inp == ('Pergi sana!'.lower()): # Bot kick confirmation
        reply_txt('Kakak jahat :( ,nanti undang lagi ya :)')

        if isinstance(event.source, SourceGroup):
            elisebot.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            elisebot.leave_room(event.source.room_id)

    elif inp == ('jangan keluarkan!'.lower()): # Bot kick confirmation
        reply_txt('Terima kasih kak :)')
# --------------------------------------------------------------- #

    elif inp == '/admin':
        about_button = TemplateSendMessage(
            alt_text='Info Admin',
            template=ButtonsTemplate(
                thumbnail_image_url='https://dl.dropboxusercontent.com/s/xjgb1az7tt7p7h3/admin_logo.png',
                title='Admin Elisé (Chat bot)',
                text= 'Pradipta Gitaya (21 Tahun)',
                actions=[
                    MessageTemplateAction(
                        label='Hubungi Admin',
                        text= '/contactadmin' ),
                    MessageTemplateAction(
                        label='Catatan Admin',
                        text= '/adminnotes' ),]))

        elisebot.reply_message(event.reply_token, about_button)

    elif inp == '/adminnotes':
        reply_txt(admin_note_msg)
    elif inp == '/contactadmin':
        reply_txt(about_msg)
# ----------------------------------------------------------------- #

    elif inp not in keyword:

        if inp == "halo" or inp == "hallo" or inp == "hello" or inp == "hi" or inp == "hai" or inp == 'hey' or inp == 'hoi':
            reply_txt("Halo kak, kita ngobrol yuk~ (^.^)//")

        elif inp == "ampas" or inp == "no ssr" or inp == "tergarami" or inp == "zonk" or inp == "gacha ampas" or inp == "gachanya ampas" or inp == "tidak hoki" or inp == "nggak hoki":
            reply_txt("Coba lagi kak ! Siapa tau lebih zonk \(>.<)/")

        elif inp == "gas" or inp == "kuy" or inp == "jalan jalan" or inp == "cabut" or inp == "cabs" or inp ==  "let's go" or inp == "yuk" or inp == "pergi":
            reply_txt("Kuy kemana kak? Sebentar, adek mau dandan dulu")

        elif inp == "dasar wibu" or inp == "kamu wibu" or inp == "dih wibu" or inp == "lu wibu" or inp == "wibu lu" or inp == "wibu dasar" or inp == "wibu kamu":
            reply_txt("Adek mau jadi wibu juga (>..<)/")
        
        elif inp == "enak" or inp == "ena ena":
            reply_txt("Dasar kakak, maunya ena ena terus ngilang gitu aja")

        elif inp == "gas" or inp == "kuy" or inp == "jalan jalan" or inp == "cabut" or inp == "cabs" or inp == "let's go" or inp == "yuk" or inp == "pergi":
            reply_txt("Kuy kemana kak? Sebentar, adek mau dandan dulu")

        elif inp == "jelek":
            reply_txt("Wah, kakak ngaku kalo kakak jelek, adek salut ^.^")

        elif inp == "elise jelek":
            reply_txt("Elise lucu kok kak, sekitar 9/10 lah")
    
        elif inp == "referensi anime":
            reply_txt("Coba buka ini: https://anidb.net")
        
        elif inp == '...':
            reply_txt("krik...krik...krik...")

        else:
            return "OK"
            
    else:
        return "OK"
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
