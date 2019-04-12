import datetime
#Just some helper methods to assist the other Query files

def str_to_datetime(dateStr):
    split = dateStr.split("/")
    month = split[0]
    month = int(month)
    day = split[1]
    day = int(day)
    year = split[2]
    year = "20" + str(year)
    year = int(year)
    date = datetime.datetime(year,month,day)
    return date

def datetime_to_str(dateObj):
    date = dateObj.strftime("%x")
    return date

def dateRange(start, end):
    outputList = []
    startDate = str_to_datetime(start)
    endDate = str_to_datetime(end)
    for n in range(int ((endDate - startDate).days)+1):
        ans = startDate + datetime.timedelta(n)
        ans = datetime_to_str(ans)
        outputList.append(ans)
    return outputList

def additionalDays(start, days):
    startDate = str_to_datetime(start)
    outputList = []
    date_list = [startDate + datetime.timedelta(days=x) for x in range(0, days)]
    for date in date_list:
        outputList.append(datetime_to_str(date))
    return outputList

def previousDays(start, days):
    startDate = str_to_datetime(start)
    outputList = []
    date_list = [startDate - datetime.timedelta(days=x) for x in range(0, days)]
    for date in date_list:
        outputList.append(datetime_to_str(date))
    return outputList
