# -*- coding: utf-8 -*-

import random
import asyncio

import time
import zmq
import zmq.asyncio

url = "tcp://*:5000"

CHANNEL = b"status"


@asyncio.coroutine
def server_zeromq():
	print("#")
	ctx = zmq.asyncio.Context(3)
	# sock = ctx.socket(zmq.PUB)
	sock = ctx.socket(zmq.PUSH)

	sock.bind(url)

	i = 0
	while True:
		# print("Sent %s" % i)

		# yield from sock.send_string(str(random.randint(0, 10000)))
		yield from sock.send_string(str(i))

		yield from asyncio.sleep(0.0001)

		i += 10


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
