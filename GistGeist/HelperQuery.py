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
    for n in range(int ((end - start).days)+1):
        outputList.append(start + datetime.timedelta(n))
    return outputList

def additionalDays(start, days):
    date_list = [start + datetime.timedelta(days=x) for x in range(0, days)]
    return date_list
