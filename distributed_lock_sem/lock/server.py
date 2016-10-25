import json
import logging
import asyncio

from functools import partial
from collections import defaultdict

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

log = logging.getLogger("rlock")


def server(listen_addr: str = "127.0.0.1", listen_port: int = 37710):
    
    resources = defaultdict(partial(asyncio.Semaphore, 1))
    
    def encode(data: str):
        return json.dumps(data).encode()
    
    def decode(data: bytes):
        raw = json.loads(data.decode())
    
        return raw.get("resource", "default")

    async def acquire(resource: str, remote_info: tuple = None):
        await resources[resource].acquire()
    
    async def release(resource: str, remote_info: tuple = None):
        resources[resource].release()
        
    async def handle_connection(reader, writer):
        addr = writer.get_extra_info('peername')

        log.debug('Connection from {}:{}'.format(addr[0], addr[1]))

        resource = decode(await reader.read(1000))
        
        # Putting remote waiting until a lock was released
        log.debug("Acquiring resource: {}".format(resource))
        await acquire(resource, addr)
        
        # Send Ok to remote. Now it can lock
        writer.write(encode({"acquire": "ok"}))
        await writer.drain()

        # Wait for remote
        await reader.read()

        # Release the resource and end the comunication
        await release(resource, addr)
        writer.close()
        
    # Start server
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_connection,
                                listen_addr,
                                listen_port,
                                loop=loop)
    running_server = loop.run_until_complete(coro)

    log.critical('Serving on {}'.format(running_server.sockets[0].getsockname()))

    try:
        loop.run_forever()
    finally:
        log.debug('Closing server')
        loop.close()

if __name__ == '__main__':
    server()
