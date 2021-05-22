# https://www.github.com/theostrich/IG-2-Directlink-Bot
# https://t.me/theostrich
# https://bit.ly/feedbackOstrich
import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import json
from telegram import MessageEntity

TOKEN = os.getenv("TOKEN")
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


# Start
def start(update, context):
    username = update.message.chat.username
    print(username)
    keyboard = [
        [
            telegram.InlineKeyboardButton("Support Channel 🌱",
                                          url="t.me/theostrich"),
            telegram.InlineKeyboardButton("Support Group 🦸‍♂", url="t.me/ostrichdiscussion"),
        ],
        [
            telegram.InlineKeyboardButton("Developer 🧑‍💻",
                                          url="https://github.com/nooneluvme"),
        ]
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    message = f'''
<b>Hey @{username} 👋

I am @Ig2DirectLinkBot Bot 👾 

Can Give You Download link 🔗
Of Public Post 📷
Instagram🤞

/help to how to use me 

Made By <a href=\"https://t.me/theostrich\"> Ostrich </a> ❤️
</b>
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='html',
                             reply_markup=reply_markup, disable_web_page_preview=True)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# help
def help(update, context):
    username = update.message.chat.username
    print("Help :", username)
    keyboard = [
        [
            telegram.InlineKeyboardButton("Support Group 🦸‍♂", url="t.me/ostrichdiscussion"),
        ],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    message = '''
Send a Instagram Post Link 🥱
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='html',
                             reply_markup=reply_markup, disable_web_page_preview=True)


help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


def web2pdf(update, context):
    url = update.message.text
    try:
        if "instagram" in url:
            splited_url = url.split("?")
            url = splited_url[0] + "?__a=1" if splited_url[0][-1] == "/" else splited_url[0] + "/?__a=1"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/83.0.4103.97 Safari/537.36"}
            r = requests.get(url=url, headers=headers)
            print(url)
            if r.status_code == 200:
                # Working With Json
                jsonresponds = r.text
                print(jsonresponds)
                jsonpy = json.loads(jsonresponds)
                instadata = jsonpy["graphql"]["shortcode_media"]
                download_link = ""
                if instadata["__typename"] == "GraphVideo":
                    download_link += instadata["video_url"]
                elif instadata["__typename"] == "GraphImage":
                    download_link += instadata["display_url"]
                keyboard = [
                    [
                        telegram.InlineKeyboardButton("⚡️ Download Link ⚡️",
                                                      url=download_link),
                    ]
                ]
                reply_markup = telegram.InlineKeyboardMarkup(keyboard)
                message = f'''
<a href=\"{download_link}\">🔥 Download Link 🔥</a>
            '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='html'
                                         , reply_markup=reply_markup, disable_web_page_preview=False)
        else:
            message = '''
<b>Only Instagram Links are allowed 📷</b>
            '''
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='html',
                                     disable_web_page_preview=True
                                     )
    except:
        massage = '''
<b>I am not Hacker To Get Download link of a private Account 🖖</b>
                    '''
        context.bot.send_message(chat_id=update.effective_chat.id, text=massage, parse_mode='html',
                                 disable_web_page_preview=True)


web2pdf_handler = MessageHandler(Filters.text & Filters.entity(MessageEntity.URL), web2pdf)
dispatcher.add_handler(web2pdf_handler)

updater.start_polling()
