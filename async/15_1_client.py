import asyncio
import time

import aiohttp


# lock = asyncio.Lock()
# semaphore = asyncio.Semaphore(4)


def limit_rate(calls_limit=5, timeout=5):
    def wrapper(coro):
        semaphore = asyncio.Semaphore(calls_limit)

        async def wait():
            try:
                await asyncio.sleep(timeout)
            finally:
                semaphore.release()

        async def inner_coro(*args, **kwargs):
            await semaphore.acquire()
            asyncio.create_task(wait())  # иначе пауза перед первыми запросами
            return await coro(*args, **kwargs)

        return inner_coro

    return wrapper


@limit_rate(calls_limit=5, timeout=10)
async def make_request(url):
    async with aiohttp.ClientSession() as session:
        # async with lock:
        # async with semaphore:
        async with session.get(url) as response:
            data = await response.json()
            print(data)
            await asyncio.sleep(1)


async def get_data(url):
    await make_request(url)


async def main():
    start = time.monotonic()

    tasks = [asyncio.create_task(
        get_data('http://localhost:8000')
    ) for _ in range(20)]

    await asyncio.gather(*tasks)

    print(time.monotonic() - start)


asyncio.run(main())
