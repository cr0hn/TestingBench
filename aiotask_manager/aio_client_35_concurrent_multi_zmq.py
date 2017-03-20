import zmq
import asyncio
import tempfile
import collections
import zmq.asyncio

from collections import defaultdict

url = "tcp://127.0.0.1:5000"


# --------------------------------------------------------------------------
# Decorators
# --------------------------------------------------------------------------
class handle_data(object):
    def __init__(self, *args):
        self.channels = args
    
    def __call__(self, f):
        f.channels = self.channels
        return f


# --------------------------------------------------------------------------
# Actor example
# --------------------------------------------------------------------------
@handle_data("channel2")
async def actor_example_1(data):
    print("Actor 1 - Received: {}".format(data))
    
    return "b"


async def actor_example_2(data):
    print("Actor 2 - Received: {}".format(data))


async def actor_example_exception(data):
    print("Actor 3 - Received: {}".format(data))
    
    # Launch exception
    raise ValueError("Actor 3")

CHANNELS = {
    "channel1": actor_example_1,
    "channel2": actor_example_1,
    "channel3": actor_example_exception
}


# --------------------------------------------------------------------------
# Actors manager
# --------------------------------------------------------------------------
async def actor_manager(socket_url: str,
                        channel: str,
                        actor: callable,
                        q_in: asyncio.PriorityQueue,
                        q_out: asyncio.PriorityQueue,
                        retry_tasks: int = 3):
    
    socket.connect(url)
    
    print("Handling actors for channel: {}".format(channel))
    
    while True:
        # Get data for the actor
        data = await q_in.get()
        
        if data == b'exit':
            break
        
        #
        # Launch the actor
        #
        for retry in range(retry_tasks, 0, -1):
            try:
                resp = await actor(data)
                
                # Send actor response to the sender?
                if resp:
                    if isinstance(resp, collections.Iterable):
                        for r in resp:
                            await q_out.put(r)
                    else:
                        await q_out.put(resp)
                
                # If actor finish well, break the retry loop
                break
            
            except Exception as e:
                print("Exception in actor '{}'. Retrying {}".format(str(actor), retry))
                print(e)


# --------------------------------------------------------------------------
# Input/output proxies
# --------------------------------------------------------------------------
async def result_proxy(q: asyncio.PriorityQueue):
    while True:
        msg = await q.get()
        
        print("Sent message: ", msg)


async def in_proxy(sock, handlers):
    
    # Receive data
    while True:
        recv = await sock.recv_string()
        
        channel, msg = recv.split(" ", maxsplit=1)
        
        handlers[channel].put_nowait(msg)


def launch(loop):
    ctx = zmq.asyncio.Context()
    
    sock = ctx.socket(zmq.SUB)
    sock.connect(url)
    
    handlers = {}
    task = []
    actors = []
    
    q_results = asyncio.PriorityQueue(loop=loop)
    
    # Init:
    # - Subscribe channels
    # - Init actors manager
    # for ch, actor in CHANNELS.items():
    for ch, actors in find_actors().items():
        sock.subscribe(ch)
        
        _actor_socket_url = "ipc://{}".format(tempfile.TemporaryFile().name)
        
        _actor_socket = ctx.socket(zmq.PUSH)
        _actor_socket.connect()
        
        handlers[ch] = _actor_socket
        
        # Launch actors
        for actor in actors:
            actors.append(loop.create_task(actor_manager(_actor_socket_url, ch, actor, q_in, q_results)))
    
    #
    # Launch proxies
    #
    task.append(loop.create_task(in_proxy(sock, handlers)))
    task.append(loop.create_task(result_proxy(q_results)))
    
    loop.run_until_complete(asyncio.wait(task,
                                         loop=loop))


def find_actors(module=None):
    """
    Find the actor name and their channels
    
    Return a dict with list of INSTANCES of actors.
    
    >>> find_actors()
    {"data1": [actor_1, actor_2]}
    
    :returns: defaultdict(list)
    """
    import sys
    
    _module = module or sys.modules[__name__]
    
    decorated_funcs = defaultdict(list)
    
    for name, obj in vars(_module).items():
        
        # Check if is a function
        if callable(obj):
            # Looking for decorated functions with @handle_data
            if hasattr(obj, "channels"):
                if not asyncio.iscoroutine(obj):
                    print("Only coroutines could be decorated. Invalid '{}'".format(name))
                
                _handel_data = getattr(obj, "channels")
                
                if isinstance(_handel_data, collections.Iterable):
                    for d in _handel_data:
                        decorated_funcs[d].append(obj)
    
    return decorated_funcs


def main():
    
    loop = zmq.asyncio.ZMQEventLoop()
    asyncio.set_event_loop(loop)
    
    launch(loop)


if __name__ == '__main__':
    main()
