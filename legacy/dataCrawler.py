'''
DATA FROM REDDIS DOES NOT COME IN UTF-8 FORMAT
NEEDS A DECODING PHASE
'''
def f( s ) :
    return s.decode()




'''
IMPORTING LIBRARIES.
- PRETTYTABLE FOR AESTHETIC PRINTING.
- PYMONGO FOR MONGO CONNECTION AND USAGE.
- TERMCOLOR FOR EASY TERMINAL COLORING.
- DECOUPLE FOR SECURITY REASONS.
    - DECOUPLE AUTHENTICATION VARIABLES FROM THE LOGIC.
    - SIMILAR ENV FILE AS IN JS ENVIRONMENTS.
- BSON FOR USING THE OBJECTID ON MONGODB ECOSSYSTEM.
- JSON FOR SMART STRING FORMATING ON JSON.
    - ALLOWS PRINTING AND SAVING FILES IN A BETTER STRUCTURED
        WAY.
- REDIS FOR REDIS CONNECTION AND USAGE.
- PRAW FOR CONNECTION AND USAGE OF REDDIT SERVERS AND API.
'''
from prettytable import PrettyTable
from pymongo import MongoClient
from termcolor import colored
from decouple import config
from bson import ObjectId
from json import dumps

import redis
import praw




'''
CONSTANTS FOR SCRIPT FLOW
'''
DB_CLEAN = True
API_INITIAL_POSTS = 5000
API_INITIAL_DATA_CRAWLING = True



'''
CREATING ENDPOINTS FOR APIS AND DATABASES.
ALL USING THE .ENV FILE.
'''
api_reddit = praw.Reddit(
    client_id=config('REDDIT_CLIENT_ID'),
    client_secret=config('REDDIT_CLIENT_SECRET'),
    user_agent=config('REDDIT_USER_AGENT'),
)

db_redis = redis.Redis(db=config('REDIS_DB'))

db_mongo = MongoClient(config('MONGO_URL'))




'''
CLEANING THE DATABASES
'''
if DB_CLEAN :
    for key in db_redis.keys() :
        db_redis.delete( key )

    database = db_mongo['test']
    col = database['test']
    col.drop()

    print(f'MongoDB: {col.count_documents({})} documents')
    xs = sum([1 for _ in db_redis.keys()])
    print(f'Redis: {xs} keys-values')
    print(f'Databases cleared\n')




'''
INITIAL DATA SCRAPPING
GIVEN A TARGET NUMBER OF HOT POSTS, THE GOAL FOCUS ON MINING THEM
THE METHODS CONSISTS ON.
    - SAVING THE WHOLE METADATA INSIDE A MONGODB DOCUMENT
    - SAVING THE SUBREDDIT, POSTSID AND AUTHOR ON A REDIS SET
'''
if API_INITIAL_DATA_CRAWLING :
    for sub in api_reddit.subreddit('all').hot(limit=API_INITIAL_POSTS) :
        mem = {}
        for k, v in sub.__dict__.items() :
            try :
                mem[k] = eval(str(v))
            except :
                mem[k] = str(v)
        
        try :
            id_ = col.insert_one(mem).inserted_id

            db_redis.hincrby('count', mem['subreddit'])

            db_redis.sadd( 'subreddits', mem['subreddit'] )
            db_redis.sadd( 'authors', mem['author'] )
            db_redis.sadd( 'posts', mem['id'] )

        except :
            # print(mem)
            print('Faulty submission')




    print(f'MongoDB: {col.count_documents({})} documents')
    xs = sum([1 for _ in db_redis.keys()])
    print(f'Redis: {xs} keys-values')
    # print(f'Redis: {db_redis.smembers("posts")}')
    print(f'Reids - Cardinality of authors: {db_redis.scard("authors")}')
    print(f'Reids - Cardinality of posts: {db_redis.scard("posts")}')
    print(f'Reids - Cardinality of subreddits: {db_redis.scard("subreddits")}')
    # Also count exists