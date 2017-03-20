import asyncio


class Next:

    def __init__(self):
        self.x = 0

    async def __aiter__(self):
        return self

    async def __anext__(self):
        if self.x > 100:
            raise StopAsyncIteration

        self.x += 1

        return self.x


async def coro():
    async for x in Next():
        print(x)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro())


if __name__ == '__main__':
    main()