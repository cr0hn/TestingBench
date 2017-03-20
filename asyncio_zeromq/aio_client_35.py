import zmq
import asyncio
import zmq.asyncio

url = "tcp://127.0.0.1:5000"
loop = zmq.asyncio.ZMQEventLoop()


async def recv_and_process():
    ctx = zmq.asyncio.Context()
    
    sock = ctx.socket(zmq.PULL)
    sock.connect(url)
    
    while True:
        msg = await sock.recv()  # waits for msg to be ready
        print("Recv-%s: " % msg)


def main():
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(recv_and_process())


if __name__ == '__main__':
    main()
