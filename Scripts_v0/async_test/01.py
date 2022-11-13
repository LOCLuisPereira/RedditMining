import asyncio

'''
async def main() :
    print('Hello...')
    await asyncio.sleep(1)
    print('... World!')

asyncio.run(main())
'''

async def say(i,s) :
    print('hello')
    await asyncio.sleep(i)
    print(s)

async def main() :
    tasks = [
        asyncio.create_task(say(i, f'world {i}'))
        for i in range(4)
    ]

    for t in tasks :
        await t
    
    print( f'Finished' )

asyncio.run(main())