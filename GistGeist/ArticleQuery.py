import pymongo
import datetime
import matplotlib.pyplot as plt
from HelperQuery import dateRange
from HelperQuery import additionalDays
from HelperQuery import previousDays

#This file contains various methods for querying the various article databases.
#It it split into 3 sections, level 1, 2, and 3 queries.

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["GistGeist"]
FOXcol = mydb["FoxArticles"]
CNNcol = mydb["CNNArticles"]
BBCcol = mydb["BBCArticles"]
AJcol = mydb["AJArticles"]


#Set of methods which take in a collection to query, as well as info to sort by
#These are the only methods that hit the database directly
#I refer to these as level 1 queries

#Given a date, AND pymongo COLLECTION, returns all articles (raw) stored on that date
def returnDate(date, col):
    query = col.find({"date":date})
    return query

#Given a word and COllECTION, returns articles (raw) where that word appears at least once
def returnArticlesWithWord(word, col):
    query = col.find({"contents." + word:{"$gt":0}})
    return query

#Number of articles scraped for a given collection on a given date
def numArticles(date, col):
    query = col.count_documents({"date":date})
    query = int(query)
    return query
    


#Set of methods which take in the results of a level 1 query to extract specific info
#I refer to this as a level 2 query

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






#Set of methods to analyze the results of level 2 queries
#I refer to these as level 3 queries


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











 
def plotGeneration(word, col, startDate, endDate):

    dates = dateRange(startDate, endDate)


    simpDates = []
    plotList = []

    for date in dates:

        simpDates.append(date[:-3])
        query = returnDate(date,col) 

        num = numArticles(date,col)
        content = returnContents(query)
        freq = wordFreqContents(content,word)
        if num > 0:
            freq = freq/num
        
        
        
        plotList.append(freq)


    plt.plot(simpDates, plotList)
    plt.show()

def returnWordFreq(word, col, startDate, endDate):
    dates = dateRange(startDate, endDate)

    outputList = []
    
    for date in dates:
        query = returnDate(date,col)
        content = returnContents(query)
        freq = wordFreqContents(content,word)
        num = numArticles(date,col)
        if num > 0:
            freq = freq/num
        outputList.append(freq)
    return outputList

