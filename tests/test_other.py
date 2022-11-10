#!/usr/bin/python

import time
import asyncio, threading


async def test1(delay, what):
    time.sleep(delay)

    print(what)


async def test2(delay, what):
    await asyncio.sleep(delay)
    print(what)
    print(asyncio.current_task())

    print(asyncio.all_tasks(loop=None))


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def main():
    task1 = asyncio.create_task(test1(10, "hello"))
    task2 = asyncio.create_task(test2(1, "world"))
    print(f"started at {time.strftime('%X')}")
    await task2
    await task1
    # new_loop = asyncio.new_event_loop()
    # t = threading.Thread(target=start_loop, args=(new_loop,))
    # t.start()
    # asyncio.run_coroutine_threadsafe()
    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
