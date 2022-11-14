'''
DATA FROM REDDIS DOES NOT COME IN UTF-8 FORMAT
NEEDS A DECODING PHASE
'''
def f( s ) :
    return s.decode()




'''
IMPORTING LIBRARIES.
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
from pymongo import MongoClient
from termcolor import colored
from json import dumps, load
from decouple import config
from random import shuffle
''' USED FOR GENERATING THE _ID FOR MONGODB '''
from bson import ObjectId
import os

import redis
import praw




'''
CONSTANTS FOR SCRIPT FLOW
'''
API_INITIAL_POSTS = 10000



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

# db_mongo = MongoClient(config('MONGO_URL'))
# col = db_mongo['test']['test']




'''
CLEAN DUMPING FOLDER
ENTERS FOLDER AND REMOVES ALL THE ITEMS INSIDE IT
'''
def cleanFolder(folder='raw_data') :
    print('=== CLEANING DATA DUMP FOLDER ===')

    root = os.getcwd()

    os.chdir(folder)
    for fileName in os.listdir() :
        os.remove( fileName )
    
    os.chdir(root)




'''
CLEANING THE DATABASES
'''
def cleanDatabases() :
    print('=== DATABASES CLEANED ===')

    for key in db_redis.keys() :
        db_redis.delete( key )

    # database = db_mongo['test']
    # col = database['test']
    # col.drop()




'''
RAW DATA TO DICTIONARY TRANSFORAMTION
'''
def raw2dict( raw ) :
    mem = {}
    for k, v in raw.__dict__.items() :
        try :
            mem[k] = eval(str(v))
        except :
            mem[k] = str(v)
    return mem




'''
HELPS MINING INFORMATION ACCORDING TO DIFFERENT MECHANISM.
AVOIDS CLUSTERING TOO MUCH THE CODE.
'''
def subInstance(instance, flag=0) :
    if flag == 0 :
        return (instance.hot(limit=API_INITIAL_POSTS), 'hot')
    elif flag == 1 :
        return instance.new(limit=API_INITIAL_POSTS), 'new'
    elif flag == 2 :
        return instance.top(limit=API_INITIAL_POSTS), 'top'
    elif flag == 3 :
        return instance.rising(limit=API_INITIAL_POSTS), 'rising'
    elif flag == 4 :
        return instance.controversial(limit=API_INITIAL_POSTS), 'controversial'
    return instance.gilded(limit=API_INITIAL_POSTS), 'gilded'




'''
INITIAL DATA SCRAPPING
GIVEN A TARGET NUMBER OF HOT POSTS, THE GOAL FOCUS ON MINING THEM
THE METHODS CONSISTS ON.
    - SAVING THE WHOLE METADATA INSIDE A MONGODB DOCUMENT
    - SAVING THE SUBREDDIT, POSTSID AND AUTHOR ON A REDIS SET
'''
def subredditMining( subredditName ) :
    print(f'== Mining r/{subredditName} ==')

    subreddit = api_reddit.subreddit( subredditName )
    for i in [0,1,3] :

        count = 0
        subCursor, mechanism = subInstance(subreddit, i)

        print(f'=== Iteraction {mechanism} ===')

        for sub in subCursor:
            count += 1

            data = raw2dict( sub )

            try :
                db_redis.hincrby('count', data['subreddit'])

                db_redis.sadd( 'subreddits', data['subreddit'] )
                db_redis.sadd( 'authors', data['author'] )
                db_redis.sadd( 'posts', data['id'] )

                with open(f'raw_data/{data["id"]}.json', 'w') as hdl :
                    hdl.write( dumps( data, indent=2 ) )

            except :
                # print(mem)
                # print('Faulty submission')
                pass




'''
INITIAL MINING AND SETUP
CLEARS FOLDER, DATABASE AND MINES THE ALL SUBPAGE
'''
def miningInitial() :
    cleanFolder()
    cleanDatabases()
    subredditMining('all')




def miningSubreddits() :
    xs = []
    for m in db_redis.smembers( 'subreddits' ) :
        xs.append( f(m) )
    shuffle(xs)

    for subreddit in xs :
        subredditMining( subreddit )




if __name__ == '__main__' :
    # miningInitial()

    miningSubreddits()