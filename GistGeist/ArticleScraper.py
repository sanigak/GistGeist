import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import pymongo
import datetime
from html.parser import HTMLParser


#Returns all links on CNN/us and CNN/world
#Had trouble pulling links from CNN homepage
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
                URLS = "https://www.cnn.com" + URLS
                outputList.append(URLS)

    homeurl = 'http://www.cnn.com/world'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')
      
    for item in list:

        URLS = item.get('href')

        if "world" in URLS or "asia" in URLS or "middleeast" in URLS or "africa" in URLS or "americas" in URLS or "europe" in URLS:
            if (URLS.count('-') > 3):
                if "video" not in URLS:
                    URLS = "https://www.cnn.com" + URLS
                    outputList.append(URLS)
        




    finalList = set(outputList)
    return finalList 

#Returns links from front page of FoxNews
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

#Returns links from front page of BBC
def BBCFrontPageLinks():
     
    homeurl = 'http://www.bbc.com'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    outputList = []
    

    for item in list:

        URLS = item.get('href')
        if (URLS.count('-')> 1):
            if (hasNumbers(URLS)):
                if "pictures" not in URLS and "video" not in URLS:
                    if (URLS[0] == '/'):
                        URLS = "https://www.bbc.com" + URLS
                    outputList.append(URLS)

    finalList = set(outputList)
    return finalList

#Helper method for BBCFrontPageLinks
def hasNumbers(inputString):

    return any(char.isdigit() for char in inputString)

#Parses a CNN article into a dict of words and their frequencies
def CNNArticleToText(URL):

    h = HTMLParser()

    text_file = open("output.txt", "w")

    homeurl = URL

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all("div")
    headline = soup.find_all('h1')
    iterator = 0

    for title in headline:
        stringy = title.string
        text_file.write(stringy)
        text_file.write("\n")

    for item in list:
        temp = str(item.contents)
        if "zn-body" in temp:
            temp = re.sub('<[^<]+?>', '', temp)
            if "(CNN)" in temp:

                if (iterator == 4):
                    text_file.write(temp)
                iterator += 1


    

    pass

#Parses a Fox article into a dict of words and their frequencies
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

#Parses a BBC article into a dict of words and their frequencies
def BBCArticleToText(URL):

    text_file = open("output.txt", "w")

    homeurl = URL

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('p')

    headline = soup.find_all('h1')

    

    for item in headline:
        stringy = item.string
        text_file.write(stringy)

    text_file.write("\n")

    for item in list:
        stringy = str(item.contents)
        if "img alt" not in stringy:
            if len(stringy) > 20:
                stringy = CleanData(stringy)
                try:
                    text_file.write(stringy)
                except:
                    print(item)
    
                
    pass

#Helper method to fix certain problems with the raw output.txt file generated
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
    pass
        
#Helper method for cleanupTXT method
def linesInFile(file):
    f = open("output.txt","r+")
    for i, l in enumerate(f):
        pass
    return i + 1

#Helper for BBCArticleToText(URL)
def CleanData(string):
    stringy = str(string)
    stringy = stringy.strip('[]\'')
    return stringy

#Pulls a title from any news article
def getTitle():

    file_object = open("output.txt", "r")
    return file_object.readline()

#Sub-engine for the CNN-related tasks -- BROKEN
def CNNEngine():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["GistGeist"]
    mycol = mydb["CNNArticles"]

    CNNlinks = CNNFrontPageLinks()

    for link in CNNlinks:

        if link != None:

            print(link)
            CNNArticleToText(link)

        
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

#Sub-engine for the Fox-related tasks
def FoxEngine():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["GistGeist"]
    mycol = mydb["FoxArticles"]

    Foxlinks = FoxFrontPageLinks()

    for link in Foxlinks:

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

#Sub-engine for the BBC-related tasks
def BBCEngine():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["GistGeist"]
    mycol = mydb["BBCArticles"]

    BBClinks = BBCFrontPageLinks()

    for link in BBClinks:

        if link != None:

            print(link)
            BBCArticleToText(link)
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

#Executes article scraping
def Engine():

    
    FoxEngine()
    BBCEngine()
    CNNEngine()

    pass

Engine()
