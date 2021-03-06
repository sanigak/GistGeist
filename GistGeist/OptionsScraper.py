import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import pymongo
import datetime


#Given stock ticket, returns all URLS for option chain
def GetOptions(ticket):
     
    homeurl = 'https://finance.yahoo.com/quote/' + ticket + '/options/'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')
    
    outputList = []
    
    for item in list:

        URLS = item.get('href')
        if "/" + ticket + "/" not in URLS:
            if "/quote/" in  URLS:
                if len(URLS) > 15:
                    URLS = "https://finance.yahoo.com" + URLS
                    index = URLS.find("?p=")
                    outputList.append(URLS[:index])


    return(outputList) 

#Given URL for specific option, returns relevant data as dict
def ReadOptions(URL):

    homeurl = URL

    page = requests.get(homeurl)
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
    symbol = str(symbol)
    
    
    for item in list:
           
        print(item)
        if iterator == 6:
            price = item.contents
        elif iterator == 7:
            change = item.contents
        elif iterator == 11:
            prevClose = item.contents
        elif iterator == 13:
            open = item.contents
        elif iterator == 15:
            bid = item.contents
        elif iterator == 17:
            ask = item.contents
        elif iterator == 19:
            strike = item.contents
        elif iterator == 26:
            volume = item.contents
        elif iterator == 28:
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
    
    x = datetime.datetime.now()
    date = x.strftime("%x")
    date = str(date)
    date = date.replace("/", "-")
    stringy = "C:\\Users\\sanig\\Documents\\GistGeist logs\\" + "GISTGEIST_OPTIONS_LOG_" + date + ".txt"
    f = open(stringy, "w+")


    #Opens file to import symbols
    file = open("C:\\Users\\sanig\\source\\repos\\GistGeist\\GistGeist\\symbols.txt","r")
    symbols = file.readlines()


    for item in symbols:
        symbol = item.rstrip("\n")
        URLlist = GetOptions(symbol)
        print(symbol)
        for URL in URLlist:
            try:
                print(URL)
                dictyBOI = ReadOptions(URL)
                mycol.insert_one(dictyBOI)
            except:
                f.write(symbol + (" HAS FAILED!\n"))
                pass

            

    pass


Engine()