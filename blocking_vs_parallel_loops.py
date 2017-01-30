#!/usr/bin/env python3
import asyncio


@asyncio.coroutine
def a():
    for i in range(0, 5, 1):
        print('a %d' % i)
        yield from asyncio.sleep(1)


@asyncio.coroutine
def b():
    for i in range(0, 5, 2):
        print('b %d' % i)
        yield from asyncio.sleep(2)

@asyncio.coroutine
def sequential_a_b():
    while True:
        print('just launch a')
        yield from a()
        print('just launch b')
        yield from b()


@asyncio.coroutine
def overlapping_a_b():
    while True:
        print('just launch a')
        asyncio.ensure_future(a())
        print('just launch b')
        asyncio.ensure_future(b())
        print('wait a bit in main function')
        yield from asyncio.sleep(2)


loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
loop.run_until_complete(overlapping_a_b())
