import os
from io import BytesIO

import face_recognition
import requests
from face_recognition import face_encodings, load_image_file

import SiteWorker
from SiteWorker import getBase

photos_base='C:\\Photo_base\\'
test_path='C:\\Test7.jpg'
faces =[]
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
site=''
startingFromFilesBase=False
base=[]
encodings=[]
encodingText="Кодування зображення "
imageNotLoadingText="Зображення не завантажене"
returningCount=6
inText="У масиві зображень довжиною "
notOneFaceText=" знаходиться не одне обличчя."
workedWithFacesCountText="Опрацьовано зображень - "

class Face:
    name=''
    site=''
    encoding=None
    def __init__(self, name, embedding, site):
        self.name=name
        self.encoding=embedding
        self.site=site


class FaceRecognitionWorker:
    def toGetImageFromSite(self, site):
        image = requests.get(site, headers=SiteWorker.headers).content
        return load_image_file(BytesIO(image))

    def loadingImageFile(self, path):
        result = load_image_file(path)
        return result

    def __init__(self):
        self.name='FaceRecognitionWorker'

    def face_encodings(self, image):
        try:
            return face_encodings(image)
        except Exception as e:
            return []

    def face_encoding(self, image):
        encoding=self.face_encodings(image)
        if len(encoding)>0:
            return encoding[0]
        return []

    def face_distances(self, encodings, encoding):
        return face_recognition.face_distance(encodings, encoding)

class Record:
    def __init__(self ,name, image, site):
        self.name=name
        self.site=site
        self.image=image

worker=FaceRecognitionWorker()


def getImagesFromBase():
    base=getBase()
    images=[]
    length=len(base)
    i=1
    for record in base:
        print("Завантаження " +str(i)+" із " +str(length))
        try:
            image=worker.toGetImageFromSite(record.site)
            images.append(Record(record.name,image, record.site))
        except Exception as e:
            print(imageNotLoadingText)
        i+=1
    return images



def getImagesFromFiles():
    filesNames=os.listdir(photos_base)
    images=[]
    for fileName in filesNames:
        site=photos_base+ fileName
        image=worker.loadingImageFile (site)
        images.append(Record(fileName,image, site))
    return images

def existedRecord(site):
    for face in faces:
        if face.site==site:
            return True
    return False



def getFaces(images):
    global faces
    i=0
    for image in images:
        i+=1
        print(encodingText+str(i))

        result=worker.face_encoding(image.image)
        if len(result)>0:
            faces.append(Face(image.name, result, image.site))
    getAllEncodings()

class ComparisonResult:
    def __init__(self, face, distance):
        self.face=face
        self.distance=distance

def find_face():
    images=[]
    if startingFromFilesBase:
        images=getImagesFromFiles()
    else:
        images=getImagesFromBase()
    getFaces(images)


def toGetEncodings(path):
    image=worker.toGetImageFromSite(path)
    return worker.face_encodings(image)

def toGetEncoding(path):
    encodings= toGetEncodings(path)
    if len(encodings)>0:
        return encodings[0]

def getAllEncodings():
    global encodings
    encodings=[]
    for face in faces:
        encodings.append(face.encoding)
    return encodings

def getFirstNotNoneItemPosition(array):
    length=len(array)
    positionMin=0
    while positionMin<length and not array[positionMin]:
        positionMin += 1
    if positionMin<length:
        return positionMin
    return None


def findingMinPosition(array):
    positionMin=getFirstNotNoneItemPosition(array)
    minItem=array[positionMin]
    length=len(array)
    i=positionMin+1
    while i< length:
        item=array[i]
        if  item ==None:
            i+=1
            continue
        if item<minItem:
            positionMin=i
            minItem=item
        i+=1
    return positionMin

def getFirst(number,distances):
    positions=[]
    for i in range(0,number):
        argmin=findingMinPosition(distances)

        positions.append(argmin)
        distances=distances[:argmin]+[None]+distances[argmin+1:]

    return positions

def getComparedFaces(positions, distances):

    result=[]
    for position in positions:
        result.append(ComparisonResult(faces[position], distances[position]))
    return result

def gettingPositionByName(name):
    i=0
    for face in faces:
        if face.name==name:
            return i
        i+=1

def compareFaces(face):

    encoding = worker.face_encodings(face)
    if len(encoding) != 1:
        return [inText+str(1)+notOneFaceText]
    face_distances = worker.face_distances(encodings, encoding[0])
    positions=getFirst(returningCount, list(face_distances))
    return ["Знайдено.", getComparedFaces(positions, face_distances)]

def printResult(result):
    for position in range(0, len(result)):
        print()

def findingFaceInBase(site):
    test_face = worker.loadingImageFile(site)
    result=compareFaces(test_face)
    return result

def inList(resultList, result):
    for item in resultList:
        if item.face == result.face:
            return True
    return False

def gettingMin(resultListItem):
    return resultListItem.distance

def deletingSame(results):
    result=[]
    for item1 in results:
        inList=False
        for item2 in result:
            if item1.face==item2.face:
                inList=True
                break
        if not inList:
            result.append(item1)
    return result

def removingSame(results):
    results.sort(key=gettingMin)
    faces=[result.face for result in results]
    def gettingCount(item):
        return faces.count(item.face)
    results.sort(key=gettingCount,reverse=True)
    return deletingSame(results)

def findingFacesInBase(faces):
    results=[]
    n=0
    for face in faces:
        result=findingFaceInBase(face)
        if len(result)>1:
            results=results + result[1]
        else:
            n+=1
    return [workedWithFacesCountText+str(len(faces)-n)+'.',removingSame(results)[:returningCount]]


