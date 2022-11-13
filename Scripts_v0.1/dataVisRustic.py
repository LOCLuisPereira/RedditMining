'''
DATA FROM REDDIS DOES NOT COME IN UTF-8 FORMAT
NEEDS A DECODING PHASE
'''
def dcd( s ) :
    return s.decode()




'''
IMPORTING LIBRARIES.
- PRETTYTABLE FOR AESTHETIC PRINTING.
- PYMONGO FOR MONGO CONNECTION AND USAGE.
- TERMCOLOR FOR EASY TERMINAL COLORING.
- DECOUPLE FOR SECURITY REASONS.
    - DECOUPLE AUTHENTICATION VARIABLES FROM THE LOGIC.
    - SIMILAR ENV FILE AS IN JS ENVIRONMENTS.
- FASTAPI BUILDING A RESTFUL API THAT WORKDS AS A MIDDLEWARE
BETWEEN BACKEND AND FRONTEND.
- BSON FOR USING THE OBJECTID ON MONGODB ECOSSYSTEM.
- JSON FOR SMART STRING FORMATING ON JSON.
    - ALLOWS PRINTING AND SAVING FILES IN A BETTER STRUCTURED
        WAY.
- REDIS FOR REDIS CONNECTION AND USAGE.
- PRAW FOR CONNECTION AND USAGE OF REDDIT SERVERS AND API.
- MATH FOR CEILING FUNCTION
'''
from fastapi.middleware.cors import CORSMiddleware
from prettytable import PrettyTable
from pymongo import MongoClient
from termcolor import colored
from decouple import config
from fastapi import FastAPI
from bson import ObjectId
from json import dumps

import redis
import praw
import math



'''
CONSTANTS FOR SCRIPT FLOW
'''
DB_CLEAN = True
API_INITIAL_POSTS = 5000
API_INITIAL_DATA_CRAWLING = True



'''
STARTING THE FASTAPI SERVER
CREATING ENDPOINTS FOR APIS AND DATABASES.
ALL USING THE .ENV FILE.
'''
app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




api_reddit = None
db_mongo = None
col = None
db_redis = None

distribution = {}


@app.on_event('startup')
async def startup_event() :
    global api_reddit
    global db_redis
    global db_mongo
    global col

    api_reddit = praw.Reddit(
        client_id=config('REDDIT_CLIENT_ID'),
        client_secret=config('REDDIT_CLIENT_SECRET'),
        user_agent=config('REDDIT_USER_AGENT'),
    )

    db_redis = redis.Redis(db=config('REDIS_DB'))

    db_mongo = MongoClient(config('MONGO_URL'))
    col = db_mongo['test']['test']


@app.get('/mongo/count')
async def f() :
    return {'data':col.count_documents({})}

@app.get('/reddis/count_pairs')
async def f() :
    xs = sum([1 for _ in db_redis.keys()])
    return {'data':xs}

@app.get('/reddis/count_authors')
async def f() :
    return {'data':db_redis.scard("authors")}

@app.get('/reddis/count_posts')
async def f() :
    return {'data':db_redis.scard("posts")}

@app.get('/reddis/count_subreddits')
async def f() :
    return {'data':db_redis.scard("subreddits")}

@app.get('/reddis/subreddits_posts/{page}/{itemspage}')
async def f(page:int, itemspage:int) :
    global distribution
    if not distribution :
        for k,v in db_redis.hgetall('count').items() :
            k, v = dcd(k), dcd(v)
            distribution[k] = v

    maxpages = math.ceil( len(list(distribution.items())) // itemspage )
    if page >= maxpages : page = maxpages

    mem = []
    bottom, top = itemspage * page, itemspage * (page + 1)
    for i, (k, v) in enumerate(sorted(list(distribution.items()), key=lambda x : x[1], reverse=True)) :
        if i < bottom : continue
        elif i >= bottom and i < top :
            mem.append((i,k,v))
        else : break

    print(mem)
    return {'data':{'current' : page, 'max' : maxpages, 'distribution' : mem}}