import asyncio


async def func(t):
    await asyncio.sleep(t)
    print(t)


async def main():
    long_task = asyncio.create_task(func(60))

    # seconds = 0
    # while not long_task.done():
    #     await asyncio.sleep(1)
    #     if seconds == 5:
    #         long_task.cancel()
    #     seconds += 1

    try:
        # res = await long_task
        res = await asyncio.wait_for(long_task, timeout=5)
    # except asyncio.CancelledError:  # выбросится при отмене задачи с помощью .cancel
    #     print('long_task canceled')
    except asyncio.TimeoutError:
        print('long_task canceled')

    # событие с Timeout без прерывания
    # try:
    #     res = await asyncio.wait_for(
    #         asyncio.shield(long_task),
    #         timeout=5)
    # except asyncio.TimeoutError:
    #     print('long_task continuate')
    #     res = await long_task


if __name__ == '__main__':
    asyncio.run(main())
