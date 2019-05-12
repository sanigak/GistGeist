import datetime
#Just some helper methods to assist the other Query files


#converts a MM/DD/YY string date into a DateTime object
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

#converts a DateTime object into a MM/DD/YY string date 
def datetime_to_str(dateObj):
    date = dateObj.strftime("%x")
    return date

#Generates a list of DateTime Dates given a MM/DD/YY string date start and end
def dateRange(start, end):
    outputList = []
    startDate = str_to_datetime(start)
    endDate = str_to_datetime(end)
    for n in range(int ((endDate - startDate).days)+1):
        ans = startDate + datetime.timedelta(n)
        ans = datetime_to_str(ans)
        outputList.append(ans)
    return outputList

#Generates a list of DateTime Dates given a MM/DD/YY string date start, and the number of days after that
def additionalDays(start, days):
    startDate = str_to_datetime(start)
    outputList = []
    date_list = [startDate + datetime.timedelta(days=x) for x in range(0, days)]
    for date in date_list:
        outputList.append(datetime_to_str(date))
    return outputList

#Generates a list of DateTime Dates given a MM/DD/YY string date start, and the number of days before that
def previousDays(start, days):
    startDate = str_to_datetime(start)
    outputList = []
    date_list = [startDate - datetime.timedelta(days=x) for x in range(0, days)]
    for date in date_list:
        outputList.append(datetime_to_str(date))
    return outputList
