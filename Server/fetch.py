import json
from time import gmtime, strftime

from database import *

def fetchData(data):

    """
    with open('dataFetched.json') as dataFetched:
        result = {}
        result["time"] = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        result["map"] = json.loads(data)
        stats = result

    with open('dataFetched.json', 'w') as dataFetched:
        dataFetched.write(str(stats))
    """

    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, "datafetching")

    #seleziona ultimo elemento fetch
    #inserisci i nuovi risultati
    #salva elemento fetch
    result = insertElementMongoDB(collection, data)
    strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)

    closeMongoDB(client)