import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import pymongo
import datetime
from html.parser import HTMLParser



def CNNFrontPageLinks():
     
    homeurl = 'http://www.cnn.com/us'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    outputList = []
      
    for item in list:

        URLS = item.get('href')

        if "/politics/" in URLS or "/us/" in URLS:
            if "specials" not in URLS and "video" not in URLS:
                outputList.append(URLS)

    homeurl = 'http://www.cnn.com/world'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    outputList = []
      
    for item in list:

        URLS = item.get('href')

        if "world" in URLS or "asia" in URLS or "middleeast" in URLS or "africa" in URLS or "americas" in URLS or "europe" in URLS:
            if (URLS.count('-') > 3):
                if "video" not in URLS:
                    outputList.append(URLS)
        




    finalList = set(outputList)
    return finalList 

def FoxFrontPageLinks():
     
    homeurl = 'http://www.foxnews.com'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    outputList = []
    

    for item in list:

        URLS = item.get('href')
        if URLS.count('-') > 3:

            if(URLS.startswith('/')):
                URLS = URLS[2:]

            if(URLS.startswith('w')):
                URLS = "http://" + URLS
            
            if ("insider." not in URLS):
                outputList.append(URLS)


    finalList = set(outputList)
    return finalList  

def CNNArticleToText(URL):

    h = HTMLParser()

    text_file = open("output.txt", "w")

    homeurl = URL

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all("div")

    for item in list:
        #print(item)
        #print()
        temp = str(item.contents)
        if "zn-body" in temp:
            temp = re.sub('<[^<]+?>', '', temp)
            print(temp)
            print()
    pass

def FoxArticleToText(URL):

    text_file = open("output.txt", "w")

    homeurl = URL

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('p')
    headline = soup.find_all('h1')

    

    for item in headline:
        str = item.string
        text_file.write(str)

    text_file.write("\n")

    for item in list:
        item = item.string
        try:
            text_file.write(item)
        except:
            print(item)
    pass

def cleanupTXT():
    f = open("output.txt","r+")
    g = open("CLEANoutput.txt","w")


    if (linesInFile("output.txt") == 6):
        d = f.readlines()
        g.write(d[0])
        g.write(d[5])
    else:
        d = f.readlines()
        g.write(d[0])
        s = d[1]
        s = s.strip("Advertisement")
        s = s.strip("URL")
        g.write(s)

def getTitle():

    file_object = open("output.txt", "r")
    return file_object.readline()

def linesInFile(file):
    f = open("output.txt","r+")
    for i, l in enumerate(f):
        pass
    return i + 1

def Engine():

    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["GistGeist"]

    mycol = mydb["FoxArticles"]

    links = FoxFrontPageLinks()

    for link in links:

        if link != None:

            print(link)
            FoxArticleToText(link)
            cleanupTXT()

        
            title = getTitle()
            contents = re.findall(r'\w+', open('output.txt').read().lower())
            frequency = Counter(contents)
            x = datetime.datetime.now()
            date = x.strftime("%x")
        

            mydict = {
                "title": title,
                "contents": frequency,
                "date": date
                }
            
            mycol.insert_one(mydict)
    pass

Engine()