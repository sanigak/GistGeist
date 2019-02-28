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
                    outputList.append(URLS)


    return(outputList) 

#Given URL for specific option, returns relevant data as dict
def ReadOptions(URL):

    homeurl = URL

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('span')

    iterator = 0

    
    
    for item in list:
           

        if iterator == 8:
            price = item.contents
        elif iterator == 9:
            change = item.contents
        elif iterator == 13:
            prevClose = item
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
        elif iterator == 20:
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

    mydict = {
                "price": strprice,
                "changeABS": changelist[0],
                "changePER": changelist[1],
                "prevClose": strprevClose,
                "open": stropen,
                "bid": strbig,
                "ask": strask,
                "contents": frequency,
                "contents": frequency,
                "date": date
                }
    
#Helper method for ReadOptions(URL)
def CleanData(string):
    stringy = str(string)
    stringy = stringy.strip('[]\'')
    return stringy




ReadOptions("https://finance.yahoo.com/quote/FB190301C00100000")