#### Imoporting Libraries

if "MongoClient" not in dir():
    from pymongo import MongoClient
if "pd" not in dir():
    import pandas as pd
if "time" not in dir():
    import time
if "requests" not in dir():
    import requests
if "urllib" not in dir ():
    import urllib.parse
from dotenv import load_dotenv
if "os" not in dir():
    import os
from src.criteria import conditions #imports dictionary with the criteria

##### getting paswords

env_path = (os.path.join("", ".env"))
load_dotenv(env_path)
FP = os.getenv("FP")

##### Mongo Query functions

def mongo_con (collection, database="Ironhack", mongoclient = "localhost:27017"):
    '''
    Contects to MongoDB and returns collection
    '''
    client = MongoClient(mongoclient)
    db=client[database]
    c =db.get_collection(collection)
    return c

##### Foursquare queries

def foursquare(location, condition, sort="DISTANCE"):
    '''
    Function to make queries in foursuare for a given condition
        Parameters: 
            location: tuple
                cordinates latitude, longitude in decimal format
            condition: int
                Condition to asses the location
            sort: "string"
                Foursquare sorting parameter = 
            
    '''
    condition = conditions[condition] #get the dictionary of the given condition
    #defining headers
    headers = {
        "accept": "application/json",
        "Authorization": FP
    }
    # parsing request
    url = "https://api.foursquare.com/v3/places/search?"
    parameters = {
    "ll": ",".join(map(str,list(location))),
    "radius" : condition["max_dist"]*1000,
    "sort": sort,
    "fields": "name,geocodes,categories,distance"
    }
    if condition["categories"]:
        parameters['categories'] =  ",".join(map(str,condition["categories"]))
    if condition["query"]:
        parameters['query']= condition["query"]
    url = url + urllib.parse.urlencode(parameters)
    response = requests.get(url, headers=headers)
    # parsing response and checking for errors
    if response.status_code == 200:
        response = response.json()['results']
        # changing distance to Km
        if response:
            for e in response:
                e["distance"] = e["distance"]/1000
                e["latitude"] = e['geocodes']['main']['latitude']
                e["longitude"] = e['geocodes']['main']['longitude']
    else: 
        print(f"{location}:  {response.status_code}")
        response = None
    # Avoiding to exceede the quota of 50 queries per second
    time.sleep(0.025)
    return response