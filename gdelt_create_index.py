import requests
import os

from requests.auth import HTTPBasicAuth

ES_HOST = os.environ.get("ES_HOST")
ES_USER = os.environ.get("ES_USER")
ES_PASSWORD = os.environ.get("ES_PASSWORD")
ES_GDELT_INDEX = os.environ.get("ES_EVENTS_INDEX")
ES_GKG_INDEX = os.environ.get("ES_GKG_INDEX")
ES_MENTIONS_INDEX = os.environ.get("ES_MENTIONS_INDEX")
INDEX = ES_GKG_INDEX
URL = ES_HOST + INDEX

def create_indice(delete=None):

    headers = {
        "Content-Type": "application/json"
    }

    print URL
    print " "

    if delete:
        requests.delete(URL, auth=HTTPBasicAuth(ES_USER, ES_PASSWORD), headers=headers)

    template = open("elasticsearch/gkg-template.json").read()
    res = requests.put(URL, data=template, auth=HTTPBasicAuth(ES_USER, ES_PASSWORD), headers=headers)

    print res.content


if __name__ == "__main__":
    delete = raw_input("Want to delete the actual '{0}' index? Y/N: ".format(INDEX)) == "Y"
    create_indice(delete)