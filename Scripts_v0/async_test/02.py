import asyncio

async def f(idx, tmp) :
    print(f'{idx} Hello')
    await asyncio.sleep(tmp)
    print(f'{idx} world')
    return idx


async def main() :
    L = await asyncio.gather(
        *[f(i, i) for i in range(5)]
    )
    print(L)

asyncio.run(main())