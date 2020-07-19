import sys, time, os
from pytube import YouTube
from pyupload.uploader import *
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

token = 'bot_token'
path = r"C:\Users\Administrator\Desktop\dwld"
bot = telegram.Bot(token)
updater = Updater(token,  request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000},use_context=True)
dispatcher = updater.dispatcher
dim = ""

def youtube(vid_url,update,context):
    yt = YouTube(vid_url)
    title = yt.title
    title = title.replace("#",'')
    title = title.replace(".",'')
    print(title)
    yt = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
    yt.download(path)
    if '360' in qual:
        context.bot.send_message(chat_id=update.effective_chat.id, text="OwO Downloaded\nsending...")
        #bot.send_video(chat_id=update.message.chat_id, video=open(f'{path}\\{title}.mp4', 'rb'), support_str=True)
        try:
            upld = upload(f'{path}\\{title}.mp4')
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{upld}') 
        except:
            try:
                title = title.replace('"','')
                upld = upload(f'{path}\\{title}.mp4')
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'{upld}')
            except:
                try:
                    #title = title.replace('"','')
                    title = title.replace("'",'')
                    upld = upload(f'{path}\\{title}.mp4')
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{upld}')
                except:
                    try:
                        #title = title.replace('"','')
                        #title = title.replace("'",'')
                        title = title.replace(",",'')
                        upld = upload(f'{path}\\{title}.mp4')
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f'{upld}')
                    except:
                        #title = title.replace('"','')
                        #title = title.replace("'",'')
                        #title = title.replace(",",'')
                        title = title.replace(".",'')
                        upld = upload(f'{path}\\{title}.mp4')
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f'{upld}')
        bot.send_video(chat_id=update.message.chat_id, video=open(f'{path}\\{title}.mp4', 'rb'), support_str=True)
    
    if '360' not in qual:
        yt2 = YouTube(vid_url)
        yt2 = yt2.streams.filter(adaptive=True).order_by('resolution').desc().first()
        yt2.download(path)
        convert(title,qual,update,context)

def convert(title,qual,update,context):
    if '1080' in qual:
        dim = "1920x1080"
    else:
        dim = "640x360"
    mkvmg(title,dim,update,context)

def mkvmg(title,dim,update,context):
    try:
        cmd = f'mkvmerge.exe --output "{path}\\{title}.mkv" --no-video --language 1:eng  "{path}\\{title}.mp4" --language 0:eng --default-track 0:yes --display-dimensions 0:{dim} "{path}\\{title}.webm" --track-order 0:1,1:0'
        os.system(cmd)
        upld = upload(f'{path}\\{title}.mkv')
    except:
        try:
            title = title.replace('"','')
            try:
                title = title.replace("'",'')
                try:
                    title = title.replace(",",'')
                except:
                    title = title.replace("'",'')
            except:
                title = title.replace(",",'')
        except:
            title = title.replace("'",'')
        title = title.replace(".",'')
        cmd = f'mkvmerge.exe --output "{path}\\{title}.mkv" --no-video --language 1:eng  "{path}\\{title}.mp4" --language 0:eng --default-track 0:yes --display-dimensions 0:{dim} "{path}\\{title}.webm" --track-order 0:1,1:0'
        os.system(cmd)
        context.bot.send_message(chat_id=update.effective_chat.id, text="uploading...")
        upld = upload(f'{path}\\{title}.mkv')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{upld}')
    bot.send_document(chat_id=update.message.chat_id, document=open(f'{path}\\{title}.mkv', 'rb'))

def upload(name):
    uploader_class = CatboxUploader
    uploader_instance = uploader_class(name)
    result = uploader_instance.execute()
    return result

def condcheck(link):
    substr = 'www.youtube.com/watch?v='
    if substr in link:
        return True
    else:
        return False

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ara ara you want to use me *kawaii*\n tap on /help to let me show you how to work with me")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Pretty simple funtionality\n use /dl <youtube-link> <360/1080> to download the videos\nBy default i will download the videos in 1080p format")

def dl(update,context):
    global link
    global qual
    link = update.message.text
    qual = link[-4:]
    link = link[4:]
    link = link.replace(qual,'')
    print(link)
    print(qual)
    link = link.replace('youtu.be/','www.youtube.com/watch?v=')
    if condcheck(link):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Downloading...")
        youtube(link,update,context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="duh! you need to send a valid link too\nThis is the format /dl <youtube-link> <quality>")

start_handler = CommandHandler('start', start)
yt_handler = CommandHandler('dl', dl)
help_handler = CommandHandler('help',help)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(yt_handler)
updater.start_polling()