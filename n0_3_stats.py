from decouple import config
from time import sleep
import redis

db_redis = redis.Redis(db=config('REDIS_DB'), decode_responses=True)

while True :

    print('--------------------------------')
    print(f'Subreddits: {db_redis.scard("subreddit" )}')
    print(f'Submissions: {db_redis.scard("submission")}')
    print(f'Authors: {db_redis.scard("redditor"  )}')

    sleep(30)