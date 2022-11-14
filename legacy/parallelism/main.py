from multiprocessing import Process, Lock, Queue
from os import system, getpid
from time import time, sleep
from sys import argv, exit

from mix_logging import Logs




def slaves_behaviour(child_number, task, logs) :
    if task[0] == 'routine' :
        logs.log( f'{child_number} rechecking {task[2]} ({task[1]})' )
    elif task[0] == 'exploratory' :
        logs.log( f'{child_number} exploring {task[1]}' )




def process_behaviour( child_number, lock, tickets, logs ) :
    if not child_number :
        logs.log( f'[MAIN][{getpid()}][START] starting the server', 8 )
        
        system('uvicorn main_server:app --reload')
        
        logs.log( f'[MAIN][{getpid()}][END] closing the server', 8 )

    else :
        while True :
            if child_number == 1 :
                logs.log(f'[MAINSLAVE][{getpid()}][START] Generating tasks for exploratory data', 6 )

                for i in range(5) :
                    tickets.put(('exploratory', 'new'))

                logs.log(f'[MAINSLAVE][{getpid()}][END] Generating tasks for exploratory data', 6 )




            task = tickets.get()
            slaves_behaviour(child_number, task, logs)




            if child_number == 1 :
                logs.log(f'[MAINSLAVE][{getpid()}][START] Generating tasks for routine schedules', 6 )

                for i in range(5) :
                    tickets.put(('routine', 'subreddit', 'some'))

                logs.log(f'[MAINSLAVE][{getpid()}][END] Generating tasks for routine schedules', 6 )

            sleep(2)




if __name__ == '__main__' :
    
    lock = Lock()
    tickets = Queue()
    logs = Logs(True)

    num_process = 4

    procs = [
        Process(
            target=process_behaviour, args=([n, lock, tickets, logs])
        ) for n in range(num_process)
    ]

    [p.start() for p in procs]
    [p.join() for p in procs]