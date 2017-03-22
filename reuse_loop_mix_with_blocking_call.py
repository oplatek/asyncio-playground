#!/usr/bin/env python3
import asyncio
import time

loop = asyncio.get_event_loop()
futures = []

@asyncio.coroutine
def asyncio_run():
    global futures
    i = 0
    while True:
        if len(futures) > 0:
            i += 1
            f = futures[0]
            futures = futures[1:]
            f.set(1)
            print('future set %d' % i)
        yield from asyncio.sleep(0.1)


@asyncio.coroutine
def asyncio_blocking_call():
    global futures
    f = asyncio.Future()
    print('futures created')
    futures.append(f)
    print('futures appended')
    yield f
    print('yield from future')


def api_call_without_asyncio():
    print('start inner loop')
    yield from asyncio_blocking_call()
    print('finish inner loop')


def regular_run():
    print('regular run started')
    j = 0
    while True:
        j += 1
        print('starting %d loop in regular run' % j)
        api_call_without_asyncio()
        time.sleep(0.2)


def start_services():
    @asyncio.coroutine
    def asyncio_regular_run():
        regular_run()
        yield from asyncio.sleep(0.0)

    futures = [
        asyncio.ensure_future(asyncio_run()),
        asyncio.ensure_future(asyncio_regular_run())
    ]

    return futures


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(asyncio.wait(start_services()))

