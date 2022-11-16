'''
PROCESS.
1. MINE THE BIGGEST AMOUNT OF POSTS INSIDE THE R/ALL
2. SAVE THE SUBREDDIT, SUBMISSION AND AUTHOR ON REDISDB
3. SAVE THE SUBMISSION INFORMATION INSIDE A FILE
4. ON START UP, SHUFFLES THE LIST AND PROCESS TO MINE THE INFORMATION
'''




'''
DATA FROM REDDIS DOES NOT COME IN UTF-8 FORMAT
NEEDS A DECODING PHASE
'''
def f( s ) :
    return s.decode()




'''
RECURSIVE PRINT OF THE STRUCTURE.
THIS SERVES A AUXILIARY FUNCTION TO PRINT THE KEYS FROM THE DICTIONARIES AND
    FIND THE STRUCTURE AND WHICH FEATURES TO SAVE
'''
def recursiveKeys( obj ) :
    xs = []

    def f( obj, c='' ) :
        if type(obj) == dict :
            for k in obj : f(obj[k], f'{c}.{k}')
        else :
            xs.append(c)
    f(obj)
    return xs



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
from json import dumps, load
from decouple import config
from bson import ObjectId

import redis
import praw




'''
CONSTANTS FOR SCRIPT FLOW
'''
DB_CLEAN = True
API_INITIAL_POSTS = 50000
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
col = db_mongo['test']['test']




'''
CLEANING THE DATABASES
'''
def cleanDatabases() :
    print('=== DATABASES CLEANED ===')

    for key in db_redis.keys() :
        db_redis.delete( key )

    database = db_mongo['test']
    col = database['test']
    col.drop()

    # print(f'MongoDB: {col.count_documents({})} documents')
    # xs = sum([1 for _ in db_redis.keys()])
    # print(f'Redis: {xs} keys-values')
    # print(f'Databases cleared\n')




'''
INITIAL DATA SCRAPPING
GIVEN A TARGET NUMBER OF HOT POSTS, THE GOAL FOCUS ON MINING THEM
THE METHODS CONSISTS ON.
    - SAVING THE WHOLE METADATA INSIDE A MONGODB DOCUMENT
    - SAVING THE SUBREDDIT, POSTSID AND AUTHOR ON A REDIS SET
'''
def initialMining() :
    xs = 0
    for sub in api_reddit.subreddit('all').hot(limit=API_INITIAL_POSTS) :
        
        xs += 1
        if xs % 1000 == 0 : print(f'=== {xs/API_INITIAL_POSTS*100}% ===')

        mem = {}
        for k, v in sub.__dict__.items() :
            try :
                mem[k] = eval(str(v))
            except :
                mem[k] = str(v)
        
        # mem['_id'] = mem['id']

        try :
            id_ = col.insert_one(mem).inserted_id

            db_redis.hincrby('count', mem['subreddit'])

            db_redis.sadd( 'subreddits', mem['subreddit'] )
            db_redis.sadd( 'authors', mem['author'] )
            db_redis.sadd( 'posts', mem['id'] )

        except :
            # print(mem)
            print('Faulty submission')




'''
Auxiliary function to find the structure of the raw data.
After finding the structure, it is possible to mine it and infer what
is worth and what is not worth and should be disposable.

THE METHOD IS SIMPLE AND TAKES A GIVEN NUMBER OF NEW POSTS
    AND SAVES IT INSIDE A GIVEN JSON FILE THAT IS CORRECTLY STRCUTURED
    EITHER VISUALLY, EITHER WITH THE COMPOSED DATA.
'''
def initialStructure(fs='structure.json', limit=10) :
    xs = []    
    for sub in api_reddit.subreddit('all').hot(limit=limit) :

        mem = {}
        for k, v in sub.__dict__.items() :
            try :
                mem[k] = eval(str(v))
            except :
                mem[k] = str(v)

        xs.append(mem)

    with open(fs,'w') as handler :
        handler.write(dumps(xs, indent=4))




'''
EDA Data Validation
CHECK IF IT IS POSSIBLE TO RETRIEVE THE FOLLOW UP INFORMATION
    BASED ON THE DATA SAVED ON THE DATABASE.
POSSIBLE DATA
    - POST ID
    - AUTHOR ID
    - SUBREDDIT ID
IN THE PRESENT TIME, ALL THE DATA CAN BE RETRIEVED
'''
def EDA_01(fs) :
    data = load(open('structure.json','r'))
    for ds in data :
        idPost = ds['id']
        idAuthor = ds['author_fullname']
        print(idAuthor)
        idSubreddut = ds['subreddit']

        print( api_reddit.submission(idPost).title )
        for x in api_reddit.subreddit(idSubreddut).hot(limit=1) :
            print(x.title)
        for x in api_reddit.redditor(fullname=idAuthor).submissions.new(limit=1) :
            print(x.title)
        

        break




'''
OPENING THE STRUCTURE.JSON FILE TO CHECK THE FIELDS THAT SHOULD BE KEPT.
AD-HOC METHOD FOR FINDING RICH FIELDS THAT SHOULD BE KEPT AND CAN HAVE A
    POSSIBLE IMPACT ON FUTURE MODELS OR FUTURE ANALYSIS
'''
def EDA_02() :
    for sub in api_reddit.subreddit('all').hot(limit=5000) :

        mem = {}
        for k, v in sub.__dict__.items() :
            try :
                mem[k] = eval(str(v))
            except :
                mem[k] = str(v)

        print(f'--- {mem["id"]} ---')

        try :
            with open(f'raw_data/{mem["id"]}.json','w') as hdlr :
                hdlr.write(dumps(mem,indent=2))
        except :
            print( '--- Error ---' )




'''
FINDING THE INFORMATION ABOUT THE AUTHOR THAT CAN BE FOUND
    INSIDE THE REDDITOR INSTANCE.

INFORMATION INSIDE THE CLASS DICT IS NOT REALLY RELEVANT.

USING THE REDDITOR CLASS, NOW IT POSSIBLE TO FIND THE INFORMATION
    INSIDE THE FOLLOWING PYTHON'S OBJECT, IT'S SUBMISSION AND COMMENTS.

INFORMATION ABOUT THE COMMENTS ARE ALMOST TRIVIAL, BUT IS GOING TO BE SAVED FOR
    EXPERIMENTS.
'''
def EDA_03() :
    for sub in api_reddit.subreddit('all').hot(limit=5000) :
        red =  api_reddit.redditor(fullname=sub.author_fullname)
        mem = {}
        for k, v in red.__dict__.items() :
            try :
                mem[k] = eval(str(v))
            except :
                mem[k] = str(v)

        print(dumps(mem,indent=2))

        redditor = {
            'id': red.id,
            'name': red.name,
            'comment_karma': red.comment_karma,
            'link_karma': red.link_karma,
            'created_utc': red.created_utc,
            'has_verified_email': red.has_verified_email,
            'icon_img': red.icon_img,
            'is_employee': red.is_employee,
            'is_mod': red.is_mod,
            'is_gold': red.is_gold
        }

        print(dumps(redditor,indent=2))

        for sub in red.submissions.new(limit=50) :
            print(sub.title)
            print(sub.subreddit)

        for com in red.comments.new(limit=50) :
            print(com.subreddit, com.submission, com.body)
        #print( red.submissions )


        break




if __name__ == '__main__' :
    # cleanDatabases()

    # initialStructure()
    # EDA_01('structure.json')
    # EDA_02()
    EDA_03()

    # initialMining()


    x = [ (f(k),int(f(v))) for k,v in db_redis.hgetall('count').items() ]
    x.sort(key=lambda x : x[1])
    # print( x )

    # print(f'MongoDB: {col.count_documents({})} documents')
    # xs = sum([1 for _ in db_redis.keys()])
    # print(f'REDIS: {xs} keys-values')
    # print(f'Redis: {db_redis.smembers("posts")}')
    # print(f'REDIS - Cardinality of authors: {db_redis.scard("authors")}')
    # print(f'REDIS - Cardinality of posts: {db_redis.scard("posts")}')
    # print(f'REDIS - Cardinality of subreddits: {db_redis.scard("subreddits")}')