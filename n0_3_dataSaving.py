'''
SCRIPT FOR DUMPING THE ITEMS INSIDE THE DATABASE INTO A SINGLE FILE.
'''
from json import dumps, load
from decouple import config
import redis

db_redis = redis.Redis(db=config('REDIS_DB'), decode_responses=True)

data = {}

for key in db_redis.keys() :
    if db_redis.type(key) == 'hash' :
        data[key] = db_redis.hgetall(key)
    if db_redis.type(key) == 'set' :
        data[key] = [x for x in db_redis.smembers(key)]

print(f'== SAVING DATA ON Data/n0_3_savings.json ==')
print(f'== STATS ==')
print(f'Subreddits: {len(data["subreddit"])}')
print(f'Submissions: {len(data["submission"])}')
print(f'Authors: {len(data["redditor"])}')
print(f'Picked: {sum(int(y) for x,y in data["selected"].items())}')

print(f'Selected Surbeddits:')
xs = [(x,x.lower()) for x,y in data['selected'].items() if int(y)]
[print(f'-- {x}') for x,y in sorted(xs, key=lambda x:x[1])]

open('Data/n0_3_savings.json','w').write(dumps(data,indent=2))