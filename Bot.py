import os
from io import BytesIO

import requests
import telebot
import validators
from PIL import Image

from Base import loadingBase
from FaceWorker import findingFaceInBase, worker, findingFacesInBase
from SiteWorker import headers
from WorkWithBase import startingWork

BOT_TOKEN = '6087581116:AAF5hb54EWcxNown5zOAc9au3DsaJxWooig'

bot = telebot.TeleBot(BOT_TOKEN)
notFindingURL="Посилання не дійсне."
notCheckedURL="Не є посиланням."
imageNotWorked="Проблеми у файлі зображення."
imageInMessageText="Є зображення."
stopText="Закінчити."
beginText="Почати."
image_list={}
name_list=[]

def deletingName(name):
    global name_list
    position=0
    while position < len(name_list):
        id = name_list[position]
        if id == name:
            name_list=name_list[:position]+name_list[position+1:]
            break

def checkingImageList(msg):
    text=msg.text
    name=msg.chat.username
    if text==beginText:
        if name not in name_list:
            name_list.append(name)
        image_list[name]=[]
        return [True, []]
    elif text==stopText:
        if name in image_list.keys() and name in name_list:
            deletingName(name)
            return [True,image_list[name]]
    elif name in name_list:
        if name in image_list.keys():
            list_item=image_list[name]
            image_list[name]=list_item+workWithMessage(msg)
            return [True,[]]
    return [False, []]


def sendingPhotos(result, msg):
    for photo in result:
        bot.send_photo(msg.chat.id, photo.face.site, photo.face.name+' - '+str(photo.distance)+'.')

def sendingNames(result, msg):
    text=result[0].name
    for position in range(1, len(result)):
        text+=', '+result[position].name
    text+='.'
    bot.send_message(msg.chat.id, text)

def respondingResult(result, msg):
    bot.send_message(msg.chat.id, result[0])
    if len(result) > 1 or len(result[1]) != 0:
        sendingPhotos(result[1], msg)

def getImageFromURL(msg, text):
    try:
        image=BytesIO(requests.get(text, headers=headers).content)
        worker.loadingImageFile(image)
        return image
    except Exception as e:
        print(e)
        bot.send_message(msg.chat.id, notFindingURL)
    return None

def gettingImagesFromURL(msg,items):
    images=[item[:len(item)-1] for item in items]
    images=[getImageFromURL(msg, item) for item in images if checkingURL(item, msg)]
    images=[image for image in images if image]
    return images

def gettingImage(msg, position):
    try:
        id = msg.photo[position].file_id
        file = bot.get_file(id)
        return BytesIO(bot.download_file(file.file_path))
    except Exception as e:
        bot.send_message(msg.chat.id, str(position) + "-" + imageNotWorked)
        return None

def toGetImageFromFiles(msg):
    bot.send_message(msg.chat.id, imageInMessageText)
    images = [gettingImage(msg, 0)]
    images = [image for image in images if image]
    return images

def checkingURL(url, msg):
    if not validators.url(url):
        bot.send_message(msg.chat.id, notCheckedURL)
        return False
    return True

def workWithMessage(msg):
    downloadedFile=[]
    if msg.photo == None:
        items = msg.text.split(' ')
        downloadedFile = gettingImagesFromURL(msg, items)
    else:
        downloadedFile = [gettingImage(msg, 0)]
    return downloadedFile

@bot.message_handler(content_types=['document', 'audio', 'text', 'photo'])
def checkImage(msg):
    checkingResult=checkingImageList(msg)
    downloadedFile=[]
    if checkingResult[0]:
        downloadedFile=checkingResult[1]
    else:
        downloadedFile=workWithMessage(msg)
    if len( downloadedFile)==0:
        return
    result=findingFacesInBase(downloadedFile)
    respondingResult(result, msg)



if __name__ == 'main__':
   loadingBase()
   bot.infinity_polling()