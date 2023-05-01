import asyncio
from contextlib import contextmanager, asynccontextmanager

from redis import asyncio as aioredis


@contextmanager
def custom_open(filename, mode='w'):
    file_obj = open(filename, mode)
    # до __enter__
    yield file_obj
    # после __exit__
    file_obj.close()


# with custom_open('file.txt') as file:
#     file.write('hello world')


@asynccontextmanager
async def redis_connection():
    try:
        redis = await aioredis.from_url('redis://localhost')
        yield redis
    finally:
        await redis.close()


async def main():
    async with redis_connection() as redis:
        await redis.set('course', 'asyncio')


if __name__ == '__main__':
    asyncio.run(main())
