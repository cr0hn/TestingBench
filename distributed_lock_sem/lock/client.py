import json
import logging
import asyncio


try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

log = logging.getLogger("rlock")


class RLock(object):
    
    def __init__(self, resource: str,
                 remote_addr: str = "127.0.0.1",
                 remote_port: int = 37710):
        self.resource = resource
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.loop = asyncio.get_event_loop()
        
        self.con_reader = None
        self.con_writer = None
        
        log.info('Connection to on {}:{}'.format(remote_addr, remote_port))
    
    async def __aenter__(self):
        # Make connection
        await self._connect()
        
        # Send resource to lock
        log.debug('Sending resource for lock, "{}" to server'.format(self.resource))
        
        self.writer.write(self._custom_encode({"resource": self.resource}))
        await self.writer.drain()
    
        # Wait until lock is released
        log.debug('Waiting for remote releases')
        await self.reader.read(10000)
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Close connection
        log.debug('Closing remote connection')
        self.writer.close()
    
    async def _connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.remote_addr,
                                                                 self.remote_port)

    def _custom_encode(self, data: dict):
        return json.dumps(data).encode(errors="ignore")


async def main(sleep):
    lock = RLock("printer")
    
    async with lock:
        await asyncio.sleep(int(sleep))
        print("XXX")

if __name__ == '__main__':
    import sys
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1]))

