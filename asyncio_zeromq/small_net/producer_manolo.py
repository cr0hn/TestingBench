# -*- coding: utf-8 -*-

import asyncio

import zmq
import zmq.asyncio

url = "tcp://127.0.0.1:5000"

CHANNEL = b"status"


@asyncio.coroutine
def server_zeromq():
	ctx = zmq.asyncio.Context()
	sock = ctx.socket(zmq.PUSH)

	# sock.bind(url)
	sock.connect(url)

	i = 0
	print("[+] Starting server 'Manolo'")

	while True:
		print("Sent %s" % i)

		yield from sock.send_string("manolo manolo-%s" % str(i))

		yield from asyncio.sleep(0.5)

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
