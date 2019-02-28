import pymongo
import datetime


#Currently only works for Fox articles as CNN scraping is not online yet
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["GistGeist"]
col = mydb["FoxArticles"]


#Given a date, returns all articles (raw) stored on that date
def returnDate(date):
    query = col.find({"date":date})
    return query

#Given set of raw articles, returns all their titles
def returnTitles(query):
    titlesList = []
    for item in query:
        title = item["title"]
        titlesList.append(title)
    return titlesList

#Given set of raw articles, returns all their dictionaries of word frequencies
def returnContents(query):
    contentsList = []
    for item in query:
        content = item["contents"]
        contentsList.append(content)
    return contentsList

#Given a word, returns articles (raw) where that word appears at least once
def returnArticlesWithWord(word):
    query = col.find({"contents." + word:{"$gt":0}})
    return query

#Given word and title list, returns number of titles in which that word appears
#Works well with returnTitles(query)
def wordHitTitles(titlesList, word):
    counter = 0
    for title in titlesList:
        if word in title:
            counter += 1
    return counter

#Given word and contents list, returns number of dicts that word appears in
#Works well with returnContents(query)
def wordHitsContents(contentsList, word):
    counter = 0
    for content in contentsList:
        try:
            freq = content[word]
            counter += 1
        except:
            pass
    return counter        

#Given word and contents list, returns total number of times that word appears over all contents
#Works well with returnContents(query)
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


