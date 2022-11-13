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

client = MongoClient(config('MONGO_URL'))






for k in r.keys() :
    r.delete( k )

database = client['test']
col = database['test']
col.drop()




for submission in reddit.subreddit("all").hot(limit=1000):
    mem = {}
    for k, v in submission.__dict__.items() :
        try :
            mem[k] = eval(str(v))
        except :
            mem[k] = str(v)

    try :
        id_ = col.insert_one(mem).inserted_id
    except :
        print(mem)
    
    r.hincrby('count', mem['subreddit'])




tbl = PrettyTable()
tbl.field_names = ['SubReddit', 'Count']
tbl.sortby = 'Count'

x = r.hgetall('count')
for k, v in x.items() :
    tbl.add_row([f(k), f(v)])

print( colored( '\nSubReddits found\n', 'green' ) )
print(tbl)

print( colored( '\nPosts mined', 'green'), end=' ' )
print( col.count_documents({}) )


print( colored( '\nPost structure example\n', 'green' ) )
random = col.find_one()
del random['_id']
print(dumps(random,indent=4))




'''
Existing categorics for subreddits
    - controversial
    - gilded
    - hot
    - new
    - rising
    - top




### REDIS ###
print(config('REDIS_DB'))


for i in range(5) :
    r.lpush( 'test', i )


print( f"Here {r.llen('test')}" )

print( r.lrange( 'test', 0, -1 ) ) 


for _ in range( r.llen('test') ) :
    print(r.lpop('test').decode())
### XXXXX ###




print( r.hgetall('count') )

print( id_ )

for item in col.find() :
    print( '---> ', item)

print( col.find_one( {'_id' : ObjectId(id_)} ) )

# print(col.delete_one())
'''