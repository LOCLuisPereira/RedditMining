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
import redis
import praw
import os

'''
RAW DATA TO DICTIONARY TRANSFORMATION
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
CREATING ENDPOINTS FOR APIS AND DATABASES.
ALL USING THE .ENV FILE.
'''
api_reddit = praw.Reddit(
    client_id=config('REDDIT_CLIENT_ID'),
    client_secret=config('REDDIT_CLIENT_SECRET'),
    user_agent=config('REDDIT_USER_AGENT'),
)
db_redis = redis.Redis(db=config('REDIS_DB'), decode_responses=True)
db_mongo = MongoClient(config('MONGO_URL'))
db_mongo = db_mongo['test']
'''
CLEANING THE DATABASES
'''
def cleanDatabases() :
    print('=== DATABASES CLEANED ===')

    for key in db_redis.keys() :
        db_redis.delete( key )

    for name in db_mongo.list_collection_names() :
        db_mongo[name].drop()

'''
REDIS
SUBREDDITS
VISIT_SUBMISSIONS
VISIT_REDDITORS
DONE_SUBMISSIONS
DONE_REDDITORS
'''
def initializeDatabases() :
    db_redis.sadd('SUBREDDITS', 'all')

'''
HELPS MINING INFORMATION ACCORDING TO DIFFERENT MECHANISM.
AVOIDS CLUSTERING TOO MUCH THE CODE.
'''
def subInstance(instance, flag=0, API_INITIAL_POSTS=100) :
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


def miningComment() : pass


def miningRedditor( authorInstance ) :
    flag = db_redis.sismember( 'DONE_REDDITORS', authorInstance.id )
    if not flag :
        data = {
            'id': authorInstance.id,
            'name': authorInstance.name,
            'comment_karma': authorInstance.comment_karma,
            'link_karma': authorInstance.link_karma,
            'created_utc': authorInstance.created_utc,
            'has_verified_email': authorInstance.has_verified_email,
            'icon_img': authorInstance.icon_img,
            'is_employee': authorInstance.is_employee,
            'is_mod': authorInstance.is_mod,
            'is_gold': authorInstance.is_gold
        }
        _id_ = db_mongo['redditors'].insert_one(data)
        db_redis.sadd('DONE_REDDITORS', authorInstance.id)
        # print(_id_)
        '''
        CAN EXTRACT INFORMATION FROM SUBMISSIONS AND COMMECTS HERE
        '''


def miningSubmission( postInstance ) :
    flag = db_redis.sismember( 'DONE_SUBMISSIONS', postInstance.id )
    if not flag :
        data = raw2dict( postInstance )
        _id_ = db_mongo['submissions'].insert_one(data)
        db_redis.sadd('DONE_SUBMISSIONS', postInstance.id)
        # print(_id_)


def miningSubreddit( instanceSubreddit, name='*' ) :
    print(f'== MINING {name} ==')
    for i in [0,1,2] :
        subGenerator, flag = subInstance( instanceSubreddit, i )
        print(f'=== TARGETING {flag} ===')
        for post in subGenerator :
            db_redis.sadd('SUBREDDITS', str(post.subreddit))

            try :
                miningSubmission( post )
                miningRedditor( post.author )
            except : pass



def miningSubreddits() :
    while True :
        xs = [xs for xs in db_redis.smembers('SUBREDDITS')]
        shuffle(xs)
        for name in xs :
            miningSubreddit( api_reddit.subreddit( name ), name )







# cleanDatabases()
initializeDatabases()
miningSubreddits()