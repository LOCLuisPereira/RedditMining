import asyncio
from random import randint

flag = True

async def set(timer=30) :
    global flag

    await asyncio.sleep(timer)
    flag = False
    
    print(f'---- Leaving ----')

    return flag

async def printer(identifier, max) :
    while flag :
        await asyncio.sleep( randint(1, max+1) )
        print(f'{identifier} entering...')
        await asyncio.sleep( randint(1, max+1) )
        print(f'{identifier} leaving!')
    return identifier

async def main() :
    tasks = [set()] + [
        printer(i,6) for i in range(4)
    ]
    l = await asyncio.gather(
        *tasks
    )
    print(l)

asyncio.run( main() )