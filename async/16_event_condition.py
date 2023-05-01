import asyncio
from random import randint

async def worker(event):
    print('Before the wait()')
    await event.wait()

    if event.is_set():
        print(f'Event is set, random number = {randint(1, 5)}')


async def waiter(condition: asyncio.Condition, id):
    async with condition:
        print(f'Waiter {id} is awaiting')
        await condition.wait()

        num = randint(1, 5)
        print(f'Waiter {id} generated {num}')


async def starter(event: asyncio.Event, condition: asyncio.Condition):
    timeout = randint(3, 5)
    await asyncio.sleep(timeout)

    event.set()
    async with condition:
        condition.notify_all()

    print(f'Start after {timeout} sec.')


async def main():
    event = asyncio.Event()
    condition = asyncio.Condition()

    tasks = [asyncio.create_task(
        worker(event)
    ) for _ in range(5)]

    waiters = [asyncio.create_task(
        waiter(condition, i)
    ) for i in range(5)]

    asyncio.create_task(starter(event, condition))

    await asyncio.gather(*tasks, *waiters)


asyncio.run(main())
