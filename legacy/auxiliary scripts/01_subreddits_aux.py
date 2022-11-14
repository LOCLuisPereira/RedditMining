def f( s ) :
    return s.decode()


from prettytable import PrettyTable
from pymongo import MongoClient
from termcolor import colored
from decouple import config
from bson import ObjectId
from json import dumps

import redis
import praw




r = redis.Redis(db=config('REDIS_DB'))

reddit = praw.Reddit(
    client_id=config('REDDIT_CLIENT_ID'),
    client_secret=config('REDDIT_CLIENT_SECRET'),
    user_agent=config('REDDIT_USER_AGENT'),
)

client = MongoClient(config('MONGO_URL'))['test']['test']






data = {}
mem = {}

data['count'] = []
for i, (k, v) in enumerate(r.hgetall('count').items()) :
    k, v = f(k), f(v)
    data['count'].append ( {'id' : i, 'name':k, 'num':v} )
    mem[v] = mem.get(v, 0) + 1

data['sample'] = []
for p in client.find({}).limit(10) :
    del p['_id']
    data['sample'].append(p)

data['total_posts'] = client.count_documents({})

data['total_subreddits'] = len(data['count'])

data['bar'] = mem

open('dummy.json','w').write(dumps(data,indent=2))
open('dashboard/data/dummy.json','w').write(dumps(data,indent=2))