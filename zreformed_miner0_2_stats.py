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

api_reddit = praw.Reddit(
    client_id=config('REDDIT_CLIENT_ID'),
    client_secret=config('REDDIT_CLIENT_SECRET'),
    user_agent=config('REDDIT_USER_AGENT'),
)
db_redis = redis.Redis(db=config('REDIS_DB'), decode_responses=True)
db_mongo = MongoClient(config('MONGO_URL'))

print(db_mongo['test']['submissions'].count_documents({}))
print(db_mongo['test']['redditors'].count_documents({}))




for k in db_redis.keys() :
    if k != 'SUBREDDITS' : continue
    print( k, db_redis.smembers(k) )