from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import Queue
from time import sleep
from os import system, getpid
from mix_logging import Logs
from random import randint

data = None

def create_proc( child_number, log, lock, q) :
    # print( f'Starting {child_number} process' )

    if not child_number :
        # system(f'uvicorn test_tasks_III_server:app --reload')
        while True :
            log.read()
            sleep(10)
    else :
        global data

        print( f'I am {getpid()}, slave number {child_number} owned by the master :(' )

        while True :
            lock.acquire()
            if q.empty() :
                item = None
            else :
                item = q.get()
            lock.release()

            if item == None : break
    
            log.log(f'From {getpid()} aka slave {child_number} got item num {item}')
        
            sleep( randint(0,10) )

        print( f'Terminating {child_number} process' )




if __name__ == '__main__' :
    log = Logs(True)

    lock = Lock()

    data = Queue()
    for i in range( 0, 20 ) :
        data.put( i )

    procs = [Process( target=create_proc, args=([i, log, lock, data])) for i in range( 5 )]

    for p in procs : p.start()
    for p in procs : p.join()
