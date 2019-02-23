import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import pymongo
import datetime





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


def ReadOptions():

    homeurl = 'https://finance.yahoo.com/quote/GOOG190301C01135000?p=GOOG190301C01135000'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('span')
    
    for item in list:
        print(item.contents)





ReadOptions()