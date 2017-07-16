import sys
import datetime


def saveLog(filename, string):
    file = open("logs.md", "a")
    file.write("##"+filename+"\n")
    file.write("**["+str(datetime.datetime.now())+"]:** "+string+"\n")
    file.close()


