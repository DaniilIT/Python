import asyncio
from random import randint


class Color:
    norm = '\033[0m'
    blue = '\033[94m'
    green = '\033[92m'


c = Color()


async def producer(queue: asyncio.Queue, num: int):
    timeout = randint(1, 5)
    await queue.put(timeout)
    print(f'{c.blue}Producer {num} put {timeout}{c.norm}  {queue}')
    await asyncio.sleep(timeout)


async def consumer(queue: asyncio.Queue, num: int):
    # while not queue.empty():
    while True:
        timeout = await queue.get()
        print(f'{c.green}Consumer {num} get {timeout}{c.norm} {queue}')
        await asyncio.sleep(timeout)
        queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=4)
    producers = [asyncio.create_task(producer(queue, i)) for i in range(12)]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(3)]
    # create_task запускает в event loop корутины, gather позволяет дождаться завершения
    await asyncio.gather(*producers)
    await queue.join()  # завершается при опустошении очереди

    for consume in consumers:
        consume.cancel()

    print(queue)


if __name__ == '__main__':
    asyncio.run(main())
