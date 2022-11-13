from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from mix_logging import Logs

logs = Logs(False)
logs.read()

app = FastAPI()
logs = Logs(True)

first = True
second = True




@app.on_event('startup')
@repeat_every(seconds=5)
async def startup_event() :
    global first
    global logs

    if first :
        logs.log('Starting up, task 1', 5)
        first = False
    else :
        logs.log('Writing again, tasks 1', 3)
    await logs.read()




@app.on_event('startup')
@repeat_every(seconds=2)
async def startup_event() :
    global second
    global logs

    if second :
        logs.log('Starting up, task 2', 5)
        second = False
    else :
        logs.log('Writing again, tasks 2', 3)
    logs.read()