#This file will contain several methods for pipelining data into ML
#It will pull together methods from ArticleQuery.py and OptionsQuery.py

# Load external libraries
import pymongo
import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection

from sklearn import tree
from sklearn.neighbors import KNeighborsRegressor

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

#Load my functions
import ArticleQuery

#Connect to Mongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["GistGeist"]
FOXcol = mydb["FoxArticles"]
CNNcol = mydb["CNNArticles"]
BBCcol = mydb["BBCArticles"]
AJcol = mydb["AJArticles"]

def weekendCollapser(startingDay, startingList):

    outputList = []

    iterator = 0
    totalLen = len(startingList)


    sat = 0
    sun = 0

    while (iterator < totalLen-1):

        if (startingDay == 6):
            startingDay += 1
            iterator += 1
            sat = startingList[iterator]

        elif (startingDay == 7):
            startingDay = 1
            iterator += 1
            sun = startingList[iterator]

        elif (startingDay == 1):
            startingDay += 1
            iterator += 1
            quant = (startingList[iterator] + sat + sun)/3
            outputList.append(quant)
        else:
            startingDay += 1
            iterator += 1
            outputList.append(startingList[iterator])
    return outputList

def insertWordColumn(word, col, startingDay, endingDay, dataset):
    cols = len(dataset.columns)
    wordFreq = ArticleQuery.returnWordFreq(word, col, startingDay, endingDay)
    cleanedFreq = weekendCollapser(3, wordFreq)
    column_values = pandas.Series(cleanedFreq)
    dataset.insert(loc = cols, column = word, value=column_values)

def predictionLEGACY():

    # Load dataset
    url = "C:\\Users\\sanigaka_cadm\\source\\repos\\sanigak\\GistGeist\\GistGeist\\DB Examples\\AMZN.csv"
    names = ['Date','Open','High','Low','Close','Adj Close','Volume','Diff']
    dataset = pandas.read_csv(url, names=names)


    dataset.drop(dataset.head(1).index,inplace=True) # drop last row

    insertWordColumn("apple", FOXcol, "02/20/19","04/10/19", dataset)
    insertWordColumn("google", FOXcol, "02/20/19","04/10/19", dataset)
    insertWordColumn("amazon", FOXcol, "02/20/19","04/10/19", dataset)

    tempArray = dataset.values
    tempX = tempArray[:,8:11]
    currentTest = tempX[-1]

    dataset.drop(dataset.tail(1).index,inplace=True) # drop last row
    print(dataset)


    # Split-out validation dataset
    array = dataset.values
    X = array[:,8:12]
    Y = array[:,7]
    print("x: ")
    print(X)
    print("y: ")
    print(Y)
    validation_size = 0.25
    seed = 5
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)


    neigh = KNeighborsRegressor(n_neighbors=2)
    neigh.fit(X, Y)

    results = neigh.predict(today)
    
    print(results)
    iterator = 0

    for pred, act in zip(results, Y_validation):
        print()
        print("Predicted: " + str(pred))
        print("Actual: " + str(act))
        if (pred > 0 and act > 0):
            iterator +=1
        if (pred < 0 and act < 0):
            iterator +=1

        print()

    denom = len(results)
    print(str(iterator) + "/" + str(denom))

def tomorrowPrediction():


    # Load dataset
    url = "C:\\Users\\sanigaka_cadm\\source\\repos\\sanigak\\GistGeist\\GistGeist\\DB Examples\\GOOG.csv"
    names = ['Date','Open','High','Low','Close','Adj Close','Volume','Diff']
    dataset = pandas.read_csv(url, names=names)

    dataset.drop(dataset.head(1).index,inplace=True) # drop last row

    insertWordColumn("apple", FOXcol, "02/20/19","04/10/19", dataset)
    insertWordColumn("google", FOXcol, "02/20/19","04/10/19", dataset)
    insertWordColumn("amazon", FOXcol, "02/20/19","04/10/19", dataset)

    tempArray = dataset.values
    tempX = tempArray[:,8:11]
    currentTest = tempX[-1]

    print(dataset)

    dataset.drop(dataset.tail(1).index,inplace=True) # drop last row
    print(dataset)

    array = dataset.values
    X = array[:,8:11]
    Y = array[:,7]


    neigh = KNeighborsRegressor(n_neighbors=2)
    neigh.fit(X, Y)

    currentTest = currentTest.reshape(1,-1)
    print(currentTest)
    results = neigh.predict(currentTest)
    
    print(results)

predictionLEGACY()