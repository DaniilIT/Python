import asyncio

import aiohttp


async def make_request(url, condition: asyncio.Condition):
    async with aiohttp.ClientSession() as session:
        async with condition:  # из-за этих двух строчек
            await condition.wait()  # корутины выполняются последовательно
            async with session.get(url) as response:
                data = await response.json()
                print(data)
                await asyncio.sleep(1)


async def get_data(url, condition):
    await make_request(url, condition)


async def done(condition: asyncio.Condition):
    print('Will start after 5 seconds')
    await asyncio.sleep(5)
    async with condition:
        condition.notify_all()


async def main():
    condition = asyncio.Condition()

    tasks = [asyncio.create_task(
        get_data('http://localhost:8000', condition)
    ) for _ in range(20)]

    asyncio.create_task(done(condition))

    await asyncio.gather(*tasks)


asyncio.run(main())
