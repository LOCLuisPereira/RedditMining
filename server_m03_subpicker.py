'''
MICROSERVER THAT FEEDS INFORMATION TO THE WEBPAGE THAT ALLOWS
    THE CHOICE OF SUBREDDITS TO MINE
'''
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from decouple import config
from json import load, dumps
import redis
import os

db_redis = redis.Redis(db=config('REDIS_DB'), decode_responses=True)

app = FastAPI()

origins = [
    "*",
    "localhost:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup_event() :
    print(f'== STARTING SERVER ==')




''' 5 minute cycle '''
'''
5 MINUTE CYCLE TASK.
STARTS BY CHECKING THE EXISTANCE OF THE CONTROL VARIABLE.
IF DOES NOT EXISTS, IT STARTS BY CREATING AND POPULATING WITH DEFAULT.
OTHERWISE, IT ITERATES THROUGHT THE MEMBERS OF SUBREDDIT CONTROL VAR INSIDE REDIS
    AND GIVES THE DEFAULT VALUE TO NEW ENTRIES

BY CHANGING THE BOOL VARIABLE, THE SYSTEM IS RESETED.

ADDED A NEW FILE, CREATING AS THE INFO IS UPDATED.
THIS FILE IS MORE CONVINIENT FOR FUTURE MININGS OR FAST DATA CHECK UP.
INITIALLY THE IDEA WAS TO KEEP THE FILE ON THE POST REQUEST, BUT KEEPING IT
    INSIDE THE CYCLE AND ALLOW ABSTRACTION FOR THE FRONTEND IS BETTER.
'''
@app.on_event('startup')
@repeat_every(seconds=5*60)
async def populateControlSubreddit() :
    print(f'== STARTING POPULATING SUBREDDIT CONTROL ON REDDIS ==')

    if False :
        db_redis.delete('selected')
        print( db_redis.keys() )

    if 'selected' not in db_redis.keys() :
        for sub in db_redis.smembers('subreddit') :
            db_redis.hset( 'selected', sub, 0 )

    for sub in db_redis.smembers('subreddit') :
        if not db_redis.hexists('selected',sub) :
            db_redis.hset( 'selected', sub, 0 )

    print(f'== FINISHED POPULATING SUBREDDIT CONTROL ON REDDIS ==')


    '''FILE UPDATE/ CREATION'''
    print(f'== STARTING CREATING CONVENIENCE FILE ==')
    
    if 'ConfigFiles' not in os.listdir() :
        os.mkdir('ConfigFiles')
    with open('ConfigFiles/subreddits2mine.json', 'w') as fs :
        obj = {}
        for k,v in db_redis.hgetall('selected').items() :
            obj[k] = v
        fs.write(dumps(obj, indent=2))

    print(f'== FINISHED CREATING CONVENIENCE FILE ==')


'''
SEND INFORMATION TO THE FRONT END PAGE ABOUT THE SUBREDDIT LISTS TO MINE.
FROM REDIS HSET - SELECTED -  THE PROGRAM PARSES THE INFORMATION TO FIT
    INSIDE THE MSG FORMAT
'''
@app.get('/rcv_subreddit_list')
async def f() :
    print(f'SENDING INFORMATION ABOUT SELECTED SUBREDDITS')

    def f( item ) :
        value = True if item[1] == '1' else False
        return {'name':item[0], 'status':value}

    subreddits = [ f(item) for item in db_redis.hgetall('selected').items() ]
    subreddits.sort(key=lambda item: item['name'])
    return {'subredditList' : subreddits}


'''
RECEIVE INFORMATION FRMO THE FRONT END PAGA ABOUT THE SUBREDDIT LISTS TO MINE.
PARSES IT AND UPDATES THE INFORMATION ON REDIS HSET - SELECTED.
'''
@app.post('/snd_subreddit_list')
async def f( request: Request ) :
    print(f'RECEIVING INFORMATION ABOUT SELECTED SUBREDDITS')
    rcvd = await request.json()
    
    for k,v in rcvd.items() :
        value = 1 if v else 0
        db_redis.hset('selected', k, value)


@app.on_event('shutdown')
async def shutdown_event() :
    print(f'== SHUTTING DOWN SERVER ==')