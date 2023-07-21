import urllib.request

import lxml.html
import requests

import FaceWorker

site_start="https://www.imdb.com/search/name/?match_all=true&start="
site_end="&ref_=rlm"
siteName='https://www.imdb.com'
position_distance=50
count=551
src='*//img/@src'
alt='*//img/@alt'
div="//div[@class='lister-item mode-detail']"
href='*//a/@href'
pageLoadingText="Завантаження сторінки: "
imageLoadingText="Завантаження адреси зображення "
startPosition=501
headers = {
    'User-Agent': '...',
    'referer': 'https://...'
}
ID=['/name/nm0000255', '/name/nm0097504', '/name/nm0940851', '/name/nm0010075']


class Record:
    name=''
    site=''
    def __init__(self,name, site):
        self.name=name
        self.site=site

def getResponse(url):
    try:
        return requests.get(url)
    except Exception as e:
        return None

def getPositions(distance):
    global startPosition
    positions=[]
    while startPosition < count:
        positions.append(startPosition)
        startPosition+=distance
    return positions

def checkingItems(items):
    records=[]
    for record in items:
        site = record.xpath(href)[0]
        result = checkingID(site)
        if not result:
            continue
        name = record.xpath(alt)[0]
        if existedRecord(name):
            continue
        url=record.xpath(src)[0]
        records.append(Record(name, url))
    return records

def getRecords():
    positions=getPositions(position_distance)
    records=[]
    i=0
    while i<len(positions):

        print(pageLoadingText+str(i))
        response = getResponse(site_start+str(positions[i])+site_end)
        if not response:
            continue
        tree = lxml.html.fromstring(response.text)
        items = tree.xpath(div)
        records=records+checkingItems(items)
        i+=1
        #positions+=position_distance
    return records

def checkingID(id):
    for item in ID:
        if item == id:
            return False
    return True


def gettingSite(record, i):
    try:
        print(imageLoadingText + str(i))
        site = record.site
        name = siteName + site  #

        site = requests.get(name, headers=headers).text
        tree = lxml.html.fromstring(site)
        result = tree.xpath(src)[0].split(' ')
        length=len(result)
        site=result[length-2]
        return site

    except Exception as e:
        return None

def existedRecord(site):
    for face in FaceWorker.faces:
        if face.name==site:
            return True
    return False

def getBase():
    records = getRecords()
    return records