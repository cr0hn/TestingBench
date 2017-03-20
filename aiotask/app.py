import asyncio

from functools import partial


class C:
    def __init__(self, *args, **kwargs):
        self.fn = args[0]
        self.args = args[1:]
        self.kwargs = kwargs
    
    async def __aenter__(self):
        resp = await self.fn(*self.args, **self.kwargs)
        
        return resp
    
    async def __aexit__(self, exc_type, exc, tb):
        pass


class AsyncTask:
    
    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self.pending_tasks = asyncio.PriorityQueue(loop=self._loop)
        self.all_tasks = dict()
        self.running_tasks = dict()
    
    # --------------------------------------------------------------------------
    # Decorator and helpers
    # --------------------------------------------------------------------------
    def accepts(*types):
        def check_accepts(f):
            assert len(types) == f.func_code.co_argcount
        
            def new_f(*args, **kwds):
                for (a, t) in zip(args, types):
                    assert isinstance(a, t), \
                        "arg %r does not match %s" % (a, t)
                return f(*args, **kwds)
        
            new_f.func_name = f.func_name
            return new_f
    
        return check_accepts
    
    def task(self):
        """Decorator"""

        def real_decorator(f):
            
            # Real call to funcion
            def new_f(*args, **kwargs):
                return f(*args, **kwargs)
        
            # if function is a coro, add some new functions
            if asyncio.iscoroutinefunction(f):
                new_f.delay = partial(self._delay, new_f)
                new_f.wait = partial(C, new_f)

            return new_f
        return real_decorator

    # --------------------------------------------------------------------------
    # Extra functions
    # --------------------------------------------------------------------------
    async def _delay(self, function, *args, **kwargs):
        await self.pending_tasks.put((function, args, kwargs))
    
    # --------------------------------------------------------------------------
    # Waiting
    # --------------------------------------------------------------------------
    async def wait(self, timeout=10):
        """
        :param timeout: Time in seconds
        :type timeout: int
        """
        TIME_STEP = 0.01
        
        _current_timeout = timeout

        while (not self.pending_tasks.empty() or self.running_tasks) \
                and _current_timeout > 0:
            
            await asyncio.sleep(TIME_STEP, loop=self._loop)
            
            _current_timeout -= TIME_STEP

    # --------------------------------------------------------------------------
    # Stopping
    # --------------------------------------------------------------------------
    async def async_stop(self):
        
        # Remove all pending coroutines
        while self.pending_tasks.qsize() > 0:
            await self.pending_tasks.get()
        
        # Cancel all running tasks
        for t in self.all_tasks.values():
            try:
                t.cancel()
            except asyncio.CancelledError:
                pass
            
    def stop(self):
        for task in self.all_tasks.values():
            task.cancel()

    # --------------------------------------------------------------------------
    # Running Tasks functions
    # --------------------------------------------------------------------------
    def _done_task(self, task_id, future):
        self.all_tasks.pop(task_id)
        self.running_tasks.pop(task_id)
        
    async def _run(self):
        """Async run"""
        
        while True:
            fn, args, kwargs = await self.pending_tasks.get()

            # Build task
            task = self._loop.create_task(fn(*args, **kwargs))
            
            # Build stop task
            done_fn = partial(self._done_task, id(task))
            
            task.add_done_callback(done_fn)
            
            self.all_tasks[id(task)] = task
            self.running_tasks[id(task)] = task
    
    def run(self):
        """Blocking run"""
        # Launch background tasks
        run_task = self._loop.create_task(self._run())
        
        self.all_tasks[id(run_task)] = run_task
        

loop = asyncio.get_event_loop()
loop.set_debug(True)

manager = AsyncTask(loop=loop)


# --------------------------------------------------------------------------
# Tasks
# --------------------------------------------------------------------------
@manager.task()
async def task_01(num):
    print("Task 01 starting: {}".format(num))
    
    await asyncio.sleep(2, loop=loop)

    print("Task 01 stopping")

async def main_async():
    manager.run()
    
    # await task_01.delay(1)
    
    # async with task_01.wait() as f:
    async with task_01.wait(1) as f:
        print(f)
    
    # await asyncio.sleep(10)
    
    # return
    await manager.wait(5)
    
    manager.stop()
    # await manager.async_stop()


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    loop.run_until_complete(main_async())

if __name__ == '__main__':
    main()
