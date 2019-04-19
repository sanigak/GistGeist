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




#Plots a single word from a single collection over date range
def plotGenerationSingle(word, col, startDate, endDate):

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

#Plots a pair of words from a single collection over date range
def plotGenerationDouble(word1, word2, col, startDate, endDate):

    dates = dateRange(startDate, endDate)


    simpDates = []
    plotList1 = []
    plotList2 = []

    for date in dates:

        simpDates.append(date[:-3])


        query = returnDate(date,col) 
        num = numArticles(date,col)
        content = returnContents(query)
        freq1 = wordFreqContents(content,word1)
        freq2 = wordFreqContents(content,word2)
        
        if num > 0:
            freq1 = freq1/num
        if num > 0:
            freq2 = freq2/num
        

        
        
        plotList1.append(freq1)
        plotList2.append(freq2)


    plt.plot(simpDates, plotList1, label = word1)
    plt.plot(simpDates, plotList2, label = word2)
    plt.legend()
    plt.show()

#Plots a single word from all 4 collections over date range
def plotGenerationAllCol(word, startDate, endDate):

    dates = dateRange(startDate, endDate)

    simpDates = []
    plotListFox = []
    plotListCNN = []
    plotListBBC = []
    plotListAJ = []

    for date in dates:

        simpDates.append(date[:-3])
        
        queryFox = returnDate(date,FOXcol) 
        numFox = numArticles(date,FOXcol)
        contentFox = returnContents(queryFox)
        freqFox = wordFreqContents(contentFox,word)
        if numFox > 0:
            freqFox = freqFox/numFox
        plotListFox.append(freqFox)

        queryCNN = returnDate(date,CNNcol) 
        numCNN = numArticles(date,CNNcol)
        contentCNN = returnContents(queryCNN)
        freqCNN = wordFreqContents(contentCNN,word)
        if numCNN > 0:
            freqCNN = freqCNN/numCNN
        plotListCNN.append(freqCNN)

        queryBBC = returnDate(date,BBCcol) 
        numBBC = numArticles(date,BBCcol)
        contentBBC = returnContents(queryBBC)
        freqBBC = wordFreqContents(contentBBC,word)
        if numBBC > 0:
            freqBBC = freqBBC/numBBC
        plotListBBC.append(freqBBC)

        queryAJ = returnDate(date,AJcol) 
        numAJ = numArticles(date,AJcol)
        contentAJ = returnContents(queryAJ)
        freqAJ = wordFreqContents(contentAJ,word)
        if numAJ > 0:
            freqAJ = freqAJ/numAJ
        plotListAJ.append(freqAJ)


    plt.plot(simpDates, plotListFox, label = "Fox")
    plt.plot(simpDates, plotListCNN, label = "CNN")
    plt.plot(simpDates, plotListBBC, label = "BBC")
    plt.plot(simpDates, plotListAJ, label = "AJ")
    plt.legend()
    plt.show()



#Returns a list of frequencies of a given word from a given collection over a date range
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

