#purely for testing stuff when I don't want to comment out too much of my code

import datetime
x = datetime.datetime.now()
date = x.strftime("%x")

date = str(date)
date = date.replace("/", "-")

stringy = "C:\\Users\\sanig\\Documents\\GistGeist logs\\" + "GISTGEIST_LOG_" + date + ".txt"

f = open(stringy, "w+")

f.write("ttestset")

