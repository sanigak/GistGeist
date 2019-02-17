
import requests
from bs4 import BeautifulSoup
import re



def FoxFrontPageLinks():
     
    homeurl = 'http://www.foxnews.com'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    outputList = []
    

    for item in list:

        URLS = item.get('href')
        if URLS.count('-') > 3:
            outputList.append(URLS)




    finalList = set(outputList)
    return finalList    


def ArticleToText(URL):

    text_file = open("output.txt", "w")

    homeurl = URL

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('p')
    headline = soup.find_all('h1')



    for item in headline:
        str = item.string
        text_file.write(str)

    for item in list:
        item = item.string
        try:
            text_file.write(item)
        except:
            print(item)




ArticleToText("https://www.foxnews.com/politics/rush-limbaugh-denies-that-wacko-right-talk-radio-influences-trumps-policy-decisions")