import asyncio
from pathlib import Path
from time import time
from urllib.parse import urlparse

import aiohttp


def write_image(content, url):
    filename = Path(urlparse(url).path).name
    folder = Path('./pictures')
    folder.mkdir(exist_ok=True)
    with open(folder.joinpath(filename), 'wb') as file:
        file.write(content)


async def fetch_image(url, session: aiohttp.ClientSession):
    # response = requests.get(url, allow_redirects=True)
    async with session.get(url, allow_redirects=True) as response:
        result = await response.read()
        write_image(result, str(response.url))


async def main():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(10):
            task = asyncio.create_task(fetch_image(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main())
    print(time() - t0)
