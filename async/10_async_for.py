import asyncio

from redis import asyncio as aioredis


class RedisReader:
    def __init__(self, redis, keys):
        self.redis = redis
        self.keys = keys

    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self

    async def __anext__(self):
        try:
            key = next(self.ikeys)
        except StopIteration:
            raise StopAsyncIteration
        else:
            async with self.redis.client() as con:
                name = await con.get(key)
            return name.decode('utf-8')


async def main():
    redis = await aioredis.from_url('redis://localhost')

    keys = ['manuilov', 'ivanov', 'petrov']

    async for name in RedisReader(redis, keys):
        print(name)


asyncio.run(main())
