import os
import pickle
import shutil

import FaceWorker
import SiteWorker
from main import Face

faceRecognitionFolder='C:\\BaseFolder'
baseFolder='C:\\BaseFolder'
deepFaceBaseFolder='C:\\Deep_face_base'
baseFolder=faceRecognitionFolder
fileClass='.item'

readAttribute='rb'
writeAttribute='wb'

baseLoadedText="База завантажена"
baseUpdatedText="База оновлена"
baseRemovedText="База видалена"
baseCreatedText="База створена"
notLoadedRecordText="Не вдалося завнтажити файл запису - "

def savingFile(item, path):
    file=open(path, writeAttribute)
    pickle.dump(item, file)
    file.close()

def openingFile(path):
    file=open(path, readAttribute)
    result = pickle.load(file)
    file.close()
    return result

def creatingBase():

    FaceWorker.find_face()
    if not os.path.exists(baseFolder):
        os.mkdir(baseFolder)
    for item in FaceWorker.faces:
        fileName=baseFolder+'\\'+item.name+fileClass
        savingFile(item, fileName)
    print(baseCreatedText)

def checkingBase():
    if not os.path.exists(baseFolder):
        creatingBase()

def loadingBase():
    checkingBase()
    FaceWorker.faces=[]
    filesNames=os.listdir(baseFolder)
    for fileName in filesNames:
        filePath=baseFolder+'\\'+fileName
        try:
            item=openingFile(filePath)
            FaceWorker.faces.append(item)
        except Exception as e:
            print(notLoadedRecordText+ filePath+'.')
    FaceWorker.getAllEncodings()
    print(baseLoadedText)


def removingBase():

    FaceWorker.faces=[]
    if os.path.exists(baseFolder):
        shutil.rmtree(baseFolder)
    print(baseRemovedText)

def updatingBase(start, count):
    SiteWorker.count=count
    SiteWorker.startPosition=start
    creatingBase()
    loadingBase()
    print(baseUpdatedText)