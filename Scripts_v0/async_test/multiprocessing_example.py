import redis

r = redis.Redis(db=10)

'''
for _ in range( r.llen( 'test' ) ) :
    r.lpop( 'test' )

for i in range(10) :
    r.lpush('test', i)
'''

from multiprocessing import Process
from time import sleep

def take(idx) :
    while True :
        pipe = r.pipeline()
        pipe.lpop("test") 
        result = pipe.execute()

        if result[0] == None :
            print(f'{idx} finished the job.')
            return

        print(f'{result[0].decode()} by {idx}')
        sleep(2)



if __name__ == '__main__' :
    t = [Process(target=take, args=(i,)) for i in range(4)]
    _ = [t.start() for t in t]
    _ = [t.join() for t in t]