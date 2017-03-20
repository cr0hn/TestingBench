import json
import random
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

async def hello(x: int, sem: asyncio.Semaphore):
    r = random.randint(1, 5)

    async for key in redis.iscan(match='something*'):
        print('Matched:', key)

    print("Waiting {}".format(x))
    await asyncio.sleep(r)
    print("Finish: " + str(x))

    print("Waiting {}".format(x))
    await asyncio.sleep(r)
    print("Finish: " + str(x))

    print("Waiting {}".format(x))
    await asyncio.sleep(r)
    print("Finish: " + str(x))

    f = asyncio.Future()

    sem.release()

async def total(loop: asyncio.AbstractEventLoop):
    """
    asdf asd f asd f asd f asdf

    .. note:

        asdfasdfas df as df

    >>> a = 1
    >>> int(a)
    1

    @param loop: asdfasdf as df asdf
    :param loop:
    :type loop:
    :return:
    :rtype:
    """
    t = []
    sem = asyncio.Semaphore(10, loop=loop)
    for x in range(1000):
        await sem.acquire()
        t.append(loop.create_task(hello(x, sem)))

    return t


def main():
    loop = asyncio.get_event_loop()
    t = loop.run_until_complete(total(loop))
    loop.run_until_complete(asyncio.wait(t, loop=loop))

if __name__ == '__main__':

    # main()
    print("asdfasdfasdf ''")

