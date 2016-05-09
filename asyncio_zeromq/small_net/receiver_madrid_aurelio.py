# -*- coding: utf-8 -*-

import asyncio
import zmq
import zmq.asyncio

url = "tcp://127.0.0.1:6000"
loop = zmq.asyncio.ZMQEventLoop()


@asyncio.coroutine
def recv_and_process():

	ctx = zmq.asyncio.Context()

	sock = ctx.socket(zmq.SUB)
	sock.setsockopt(zmq.SUBSCRIBE, b"aurelio")

	sock.connect(url)

	print("connected")

	while True:
		msg = yield from sock.recv()  # waits for msg to be ready
		print("Recv-%s: " % msg)


def main():
	asyncio.set_event_loop(loop)
	loop.run_until_complete(recv_and_process())


if __name__ == '__main__':
	main()
