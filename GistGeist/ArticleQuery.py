import pymongo
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["GistGeist"]
col = mydb["FoxArticles"]

def returnDate(date):
    query = col.find({"date":date})
    return query

def returnTitles(query):
    titlesList = []
    for item in query:
        title = item["title"]
        titlesList.append(title)
    return titlesList

def returnContents(query):
    contentsList = []
    for item in query:
        content = item["contents"]
        contentsList.append(content)
    return contentsList

def returnArticlesWithWord(word):
    query = col.find({"contents." + word:{"$gt":0}})
    return query

def wordInTitles(titlesList, word):
    counter = 0
    for title in titlesList:
        if word in title:
            counter += 1
    return counter

def wordHitsContents(contentsList, word):
    counter = 0
    for content in contentsList:
        try:
            freq = content[word]
            counter += 1
        except:
            pass
    return counter        

def wordFreqContents(contentsList, word):
    counter = 0
    for content in contentsList:
        try:
            freq = content[word]
            freq = int(freq)
            counter += freq
        except:
            pass
    return counter

def wordHitsTitles(titlesList, word):
    counter = 0
    for title in titlesList:
        if word in title:
            counter+=1
    return counter


