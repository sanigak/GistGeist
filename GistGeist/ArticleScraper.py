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

#Returns links from front page of Al Jazeera
def AJFrontPageLinks():
     
    homeurl = 'https://www.aljazeera.com/'

    page = requests.get(homeurl, verify = False)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    outputList = []
    

    for item in list:

        URLS = item.get('href')
        stringy = str(URLS)
        if (stringy.count('-')> 3) and "news" in stringy:
           stringy = "https://www.aljazeera.com" + stringy
           outputList.append(stringy)
           print(stringy)

    finalList = set(outputList)
    return finalList





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

#Parses an Al Jazeera article into a dict of words and their frequencies
#A little sloppy, as it also pulls a bunch of uneccesssary links and some junk, but also gets all the important info and that is all that is needed for now
def AJArticleToText(URL):

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
        try:
            cleaned = CleanData(stringy)
            text_file.write(CleanData(stringy))
        except:
            print(item)
    
                
    pass




#Helper method for BBCFrontPageLinks
def hasNumbers(inputString):

    return any(char.isdigit() for char in inputString)

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

#Helper for BBCArticleToText(URL), AJArticleToText(URL)
def CleanData(string):
    stringy = str(string)
    stringy = stringy.strip('[]\'')
    return stringy

#Pulls a title from any news article
def getTitle():

    file_object = open("output.txt", "r")
    return file_object.readline()

#Generates a positivity index for an article, judging how positive or negative an articles is based on its contents
def positivityIndex(frequency):

    good = frequency['good']
    excellent = frequency['excellent']
    favorable = frequency['favorable']
    great = frequency['great']
    positive = frequency['positive']
    superb = frequency['superb']
    valuable = frequency['valuable']
    wonderful = frequency['wonderful']
    superior = frequency['superior']
    strong = frequency['strong']

    bad = frequency['bad']
    awful = frequency['awful']
    dreadful = frequency['dreaful']
    lousy = frequency['lousy']
    poor = frequency['poor']
    rough = frequency['rough']
    deficient = frequency['deficient']
    substandard = frequency['substandard']
    unacceptable = frequency['unacceptable']

    index = good+excellent+favorable+great+positive+superb+valuable+wonderful+superior+strong
    index = index-bad-awful-dreadful-lousy-poor-rough-deficient-substandard-unacceptable

    return index


    

#Sub-engine for the CNN-related tasks
#Returns "CNN Worked"
def CNNEngine():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["GistGeist"]
    mycol = mydb["CNNArticles"]

    CNNlinks = CNNFrontPageLinks()

    for link in CNNlinks:

        if link != None:

           
            try:
                CNNArticleToText(link)
                title = getTitle()
            except:
                print("bleh")

        
            
            contents = re.findall(r'\w+', open('output.txt').read().lower())
            frequency = Counter(contents)
            positivity = positivityIndex(frequency)
            x = datetime.datetime.now()
            date = x.strftime("%x")
        

            mydict = {
                "title": title,
                "positivity": positivity,
                "contents": frequency,
                "date": date
                }
            
            mycol.insert_one(mydict)

    return("CNN worked\n")

#Sub-engine for the Fox-related tasks
#Returns "Fox Worked"
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
            index = positivityIndex(frequency)
            x = datetime.datetime.now()
            date = x.strftime("%x")
        

            mydict = {
                "title": title,
                "positivity": positivity,
                "contents": frequency,
                "date": date
                }
            
            mycol.insert_one(mydict)

    return("Fox worked\n")

#Sub-engine for the BBC-related tasks
#Returns "BBC Worked"
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
            index = positivityIndex(frequency)
            x = datetime.datetime.now()
            date = x.strftime("%x")
        

            mydict = {
                "title": title,
                "positivity":positivity,
                "contents": frequency,
                "date": date
                }
            
            mycol.insert_one(mydict)

    return("BBC worked\n")

#Sub-engine for the Al Jazeera-related tasks
#Returns "AJ Worked"
def AJEngine():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["GistGeist"]
    mycol = mydb["AJArticles"]

    AJlinks = AJFrontPageLinks()

    for link in AJlinks:

        if link != None:

            try:
                AJArticleToText(link)
                title = getTitle
            except:
                print("bleh")
        
            ()
            contents = re.findall(r'\w+', open('output.txt').read().lower())
            frequency = Counter(contents)
            index = positivityIndex(frequency)
            x = datetime.datetime.now()
            date = x.strftime("%x")
        

            mydict = {
                "title": title,
                "positivity": positivity,
                "contents": frequency,
                "date": date
                }
            
            mycol.insert_one(mydict)

    return("AJ worked\n")

#Executes article scraping
def Engine():

    x = datetime.datetime.now()
    date = x.strftime("%x")

    date = str(date)
    date = date.replace("/", "-")

    stringy = "C:\\Users\\sanig\\Documents\\GistGeist logs\\" + "GISTGEIST_ARTICLES_LOG_" + date + ".txt"

    f = open(stringy, "w+")


    
    try:
        f.write(CNNEngine())
    except:
        f.write("CNN failed\n")

    try:
        f.write(FoxEngine())
    except:
        f.write("Fox failed\n")

    try:
        f.write(BBCEngine())
    except:
        f.write("BBC failed\n")

    try:
        f.write(AJEngine())
    except:
        f.write("AJ failed\n")
    
    

    pass

Engine()