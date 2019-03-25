import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import pymongo
import datetime


#Given stock ticket, returns all URLS for option chain
def GetOptions(ticket):
     
    homeurl = 'https://finance.yahoo.com/quote/' + ticket + '/options/'

    page = requests.get(homeurl, verify = False)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')
    
    outputList = []
    
    for item in list:

        URLS = item.get('href')
        if "/" + ticket + "/" not in URLS:
            if "/quote/" in  URLS:
                if len(URLS) > 15:
                    URLS = "https://finance.yahoo.com" + URLS
                    outputList.append(URLS)


    return(outputList) 

#Given URL for specific option, returns relevant data as dict
def ReadOptions(URL):

    homeurl = URL

    page = requests.get(homeurl, verify = False)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('span')

    iterator = 0

    #This horrible mess extracts the stock symbol from the URL
    temp = URL.replace("https://finance.yahoo.com/quote/","")
    digits = filter(str.isdigit, temp)
    for item in digits:
        temp = temp.replace(item, "")
    type = temp[-1]
    symbol = temp[:-1]
    
    
    for item in list:
           

        if iterator == 8:
            price = item.contents
        elif iterator == 9:
            change = item.contents
        elif iterator == 13:
            prevClose = item.contents
        elif iterator == 15:
            open = item.contents
        elif iterator == 17:
            bid = item.contents
        elif iterator == 19:
            ask = item.contents
        elif iterator == 21:
            strike = item.contents
        elif iterator == 28:
            volume = item.contents
        elif iterator == 30:
            openInterest = item.contents

        iterator += 1


    
    strchange = str(change)
    strchange = strchange.strip('[]\'')
    changelist = strchange.split(' ')


    strprice = CleanData(price)
    strprevClose = CleanData(prevClose)
    stropen = CleanData(open)
    strbid = CleanData(bid)
    strask = CleanData(ask)
    strstrike = CleanData(strike)
    strvolume = CleanData(volume)
    stropenInt = CleanData(openInterest)

    x = datetime.datetime.now()
    date = x.strftime("%x")

    mydict = {
                "symbol": symbol,
                "type": type,
                "price": strprice,
                "changeABS": changelist[0],
                "changePER": changelist[1],
                "prevClose": strprevClose,
                "open": stropen,
                "bid": strbid,
                "ask": strask,
                "strike": strstrike,
                "volume": strvolume,
                "openInt": stropenInt,
                "date": date
                }
    return mydict
    
#Helper method for ReadOptions(URL)
def CleanData(string):
    stringy = str(string)
    stringy = stringy.strip('[]\'')
    return stringy

#Brings Everything Together
def Engine():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["GistGeist"]

    mycol = mydb["Options"]

    

    #This block is stuff for the log
    
    f = open(stringy, "w+")
    x = datetime.datetime.now()
    date = x.strftime("%x")
    date = str(date)
    date = date.replace("/", "-")
    file = open("symbols.txt","r")
    symbols = file.readlines()
    stringy = "C:\\Users\\sanig\\Documents\\GistGeist logs\\" + "GISTGEIST_OPTIONS_LOG_" + date + ".txt"

    for item in symbols:
        symbol = item.rstrip("\n")
        URLlist = GetOptions(symbol)

        for URL in URLlist:
            try:
                dictyBOI = ReadOptions(URL)
            except:
                f.write(symbol + ("HAS FAILED!"))

            mycol.insert_one(dictyBOI)

Engine()