from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from mix_logging import Logs
from time import sleep
from multiprocessing import Process

processes = []
processes_status = []
logs = Logs(True)
count = 0
app = FastAPI()


print(count)

def f( child_number ) :
    global logs

    logs.log( f'Im am the {child_number} child' )
    sleep( 3 )
    logs.log( f'Im am the {child_number} and I am going to sleep' )




@app.on_event('startup')
@repeat_every(seconds=1)
async def startup_event() :
    global processes
    global processes_status
    global count
    global logs

    count += 1
    processes.append(
        Process(
            target=f, args=([count])
        )
    )
    processes[-1].start()

    processes_status.append(False)

    if count == 5 :
        while True :
            if sum(processes_status) == len(processes_status) :
                sys.exit(0)
            sleep(1)



@app.on_event('shutdown')
async def shutdown_event() :
    global processes
    global logs

    for p in processes :
        p.join()
    
    logs.read()