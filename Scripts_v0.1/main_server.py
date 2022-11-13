from mix_logging import Logs

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every


app = FastAPI()
logs = Logs()


@app.on_event('startup')
async def startup_event() :
    print(f'Server started')

@app.on_event('startup')
@repeat_every(seconds=3, wait_first=True)
async def startup_event() :
    logs.read()

@app.on_event('shutdown')
async def shutdown_event() :
    print(f'Server shuting down')