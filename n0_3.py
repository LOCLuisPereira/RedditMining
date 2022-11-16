'''
Goal is employ a flooding algorithm in the mining process.
No data retrieval, except for the listing of subreddits,
    submissions and redditors
'''

from json import dumps, load
from decouple import config
import redis
import praw
import os

LIMIT_PER_SUB = 50
LIMIT_PER_USER = 1000

api_reddit = praw.Reddit(
    client_id=config('REDDIT_CLIENT_ID'),
    client_secret=config('REDDIT_CLIENT_SECRET'),
    user_agent=config('REDDIT_USER_AGENT'),
)

db_redis = redis.Redis(db=config('REDIS_DB'), decode_responses=True)


'''
final part of the tree
get author
'''
def miningComments( instance ) :
    pass

'''
parse comments and submissions
'''
def miningRedditor( instance, limit=LIMIT_PER_USER ) :
    print( f'----> Subredditor {instance.id}' )

    if db_redis.sismember( 'redditor', instance.id ) :
        print('----> Skipping')
        return

    db_redis.sadd('redditor', instance.id )

    for sub in instance.submissions.new(limit=limit) :
        miningSubmission( sub )

    # for comm in instance.comments :
    #    miningComments( comm )




def miningSubmission( instance ) :
    print( f'----> Submission {instance.id}' )

    if db_redis.sismember( 'submission', instance.id ) :
        print('----> Skipping')
        return

    db_redis.sadd('submission', instance.id )
    
    if not db_redis.sismember('subreddit', instance.subreddit.display_name) :
        miningSubreddit( instance.subreddit.display_name )
    if not db_redis.sismember('redditor', instance.author.id) :
        miningRedditor( instance.author )
    miningComments( instance.comments )




def miningSubreddit( id, limit=LIMIT_PER_SUB ) :
    print( f'--> Subreddit {id}' )
    
    db_redis.sadd('subreddit', id )

    instance = api_reddit.subreddit( id )
    instances = [
        instance.hot(limit=limit),
        instance.new(limit=limit),
        instance.top(limit=limit)
    ]
    for inst in instances :
        for submission in inst :
            miningSubmission( submission )




def miningSubreddits() :
    for subreddit in db_redis.smembers( 'subreddits' ) :
        miningSubreddit( subreddit )




if __name__ == '__main__' :

    # for key in db_redis.keys() :
    #     db_redis.delete( key )

    db_redis.sadd('subreddits', 'all')
    miningSubreddits()