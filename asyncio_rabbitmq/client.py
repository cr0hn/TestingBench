# -*- coding: utf-8 -*-

import asyncio
import aioamqp


@asyncio.coroutine
def callback(channel, body, envelope, properties):
	print(body)


@asyncio.coroutine
def run_client():
	transport, protocol = yield from aioamqp.connect(host="10.211.55.70",
	                                                 port=5672,
	                                                 login="admin",
	                                                 password="admin")

	channel = yield from protocol.channel()

	yield from channel.queue_declare(queue_name='hello')

	yield from channel.basic_consume(callback, queue_name='hello', no_ack=True)


def main():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run_client())
	loop.run_forever()


if __name__ == '__main__':
	main()
