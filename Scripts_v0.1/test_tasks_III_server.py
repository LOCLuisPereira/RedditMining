from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from time import sleep
from sys import exit

from mix_logging import Logs

count = 0
log = Logs(False)

app = FastAPI()

@app.on_event('startup')
@repeat_every(seconds=3)
async def startup_event() :
    global count
    global log

    log.read()

    if count == 5 :
        exit(0)

    count += 1
    print(f'Im am the main process and Im running the server')

@app.on_event('shutdown')
async def shutdown_event() :
    print('Closing main process')