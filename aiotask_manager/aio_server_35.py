import zmq
import random
import asyncio
import zmq.asyncio

url = "tcp://127.0.0.1:5000"

CHANNEL = b"status"

async def server_zeromq():
    ctx = zmq.asyncio.Context()
    sock = ctx.socket(zmq.PUB)
    
    sock.bind(url)
    
    channels = ["channel1", "channel2", "channel3"]
    
    total = 0
    while True:
        for ch in channels:
            for x in range(random.randint(1, 4)):
                resp = await sock.send_string("{} sendChannel <{}> - Payload: {} - Total: {}".format(ch, ch, x, total))
        
                if resp == b"quit":
                    break
        
        await asyncio.sleep(0.1)

        total += 1


def main():
    loop = zmq.asyncio.ZMQEventLoop()
    asyncio.set_event_loop(loop)
    
    print("Bind in %s" % url)
    try:
        loop.run_until_complete(server_zeromq())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
