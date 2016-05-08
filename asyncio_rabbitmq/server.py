# -*- coding: utf-8 -*-

import asyncio
import aioamqp


@asyncio.coroutine
def run_server():
	transport, protocol = yield from aioamqp.connect(host="10.211.55.70",
	                                                 port=5672,
	                                                 login="admin",
	                                                 password="admin")
	channel = yield from protocol.channel()

	yield from channel.queue_declare(queue_name='hello')

	i = 0

	print("Serving")
	while True:
		yield from channel.basic_publish(
			payload=str(i),
			exchange_name='',
			routing_key='hello'
		)

		i += 1

	yield from protocol.close()

	# ensure the socket is closed.
	transport.close()


def main():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run_server())


if __name__ == '__main__':
	main()