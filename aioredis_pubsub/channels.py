import asyncio
import aioredis


def main():
    loop = asyncio.get_event_loop()
    
    async def reader(ch):
        while await ch.wait_message():
            msg = await ch.get_json()
            print("Got Message:", msg)
    
    async def go():
        pub = await aioredis.create_redis(('localhost', 6379))
        sub = await aioredis.create_redis(('localhost', 6379))
        
        res = await sub.subscribe('chan:1', *['chan:2', 'chan:3'])
        res = await sub.psubscribe('chan*')
        ch1 = res[0]
        
        tsk = loop.create_task(reader(ch1))
        
        for x in range(100):
            res = await pub.publish_json('chan:1', ["Hello", "world{}".format(x)])
            res = await pub.publish_json('chan:2', ["Hello", "world{}".format(x)])
            
            await asyncio.sleep(1)
            
            assert res == 1
        
        await sub.unsubscribe('chan:1')
        await tsk
        sub.close()
        pub.close()
    
    loop.run_until_complete(go())


if __name__ == '__main__':
    main()