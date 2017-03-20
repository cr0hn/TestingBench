import asyncio
import aioredis
import datetime
import random

loop = asyncio.get_event_loop()
redis_send = None
redis_recv = None
now = lambda: datetime.datetime.now().strftime("[%H:%M:%S.%f]")  # %Y-%m-%d %H:%M:%S


async def connect():
    global redis_send, redis_recv
    redis_send = await aioredis.create_redis(
        ('localhost', 6379), loop=loop, db=10)
    redis_recv = await aioredis.create_redis(
        ('localhost', 6379), loop=loop, db=10)


async def sender():
    counter = 1
    while True:
        print(now(), 'send %s' % counter)
        redis_send.lpush('mylist', '%s' % counter)
        # await asyncio.sleep(random.random() * 2.5)
        await asyncio.sleep(200000)
        counter += 1


async def receiver():
    print("starting receiver")
    while True:
        val = await redis_recv.brpop('mylist', timeout=0)
        print(now(), 'recv %s' % val)


if __name__ == '__main__':
    loop.run_until_complete(connect())
    
    loop.create_task(receiver())
    loop.run_until_complete(sender())
    
    redis_send.close()
    redis_recv.close()
