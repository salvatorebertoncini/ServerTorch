import sys
from time import gmtime, strftime

def fetchData(data):
    with open("dataFetched.txt", "a") as myfile:
        time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        myfile.write("Fetched the %s \n" % time)
        myfile.write(str(data) + "\n \n")
