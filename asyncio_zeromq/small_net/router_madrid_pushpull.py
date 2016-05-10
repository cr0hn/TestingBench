# -*- coding: utf-8 -*-

import asyncio

import zmq
import zmq.asyncio

url_in = "tcp://*:5000"
url_out = "tcp://*:6000"

CHANNEL = b"status"


@asyncio.coroutine
def proxy_zeromq():
	ctx = zmq.asyncio.Context()
	sock_in = ctx.socket(zmq.PULL)
	sock_in.bind(url_in)

	sock_out = ctx.socket(zmq.PUSH)
	sock_out.bind(url_out)

	zmq.proxy(sock_in, sock_out)


def main():

	loop = zmq.asyncio.ZMQEventLoop()
	asyncio.set_event_loop(loop)

	print("Bind proxy")
	try:
		loop.run_until_complete(proxy_zeromq())
	except KeyboardInterrupt:
		pass


if __name__ == '__main__':
	main()
