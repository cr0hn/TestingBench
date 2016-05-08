# -*- coding: utf-8 -*-

import asyncio
import asyncio_redis


@asyncio.coroutine
def run_server():
	connection = yield from asyncio_redis.Connection.create(host='localhost', port=6379)

	# Create subscriber.
	# subscriber = yield from connection.start_subscribe()

	# Subscribe to channel.
	# yield from subscriber.subscribe(['our-channel'])

	# Inside a while loop, wait for incoming events.
	i = 0
	while True:
		reply = yield from connection.publish('our-channel', str(i))

		i += 1
	# When finished, close the connection.
	connection.close()


def main():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run_server())


if __name__ == '__main__':
	main()