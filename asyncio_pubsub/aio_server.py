# -*- coding: utf-8 -*-

import msgpack
import random
import asyncio
import zmq
import zmq.asyncio

ASYNCIO = False

url = "tcp://127.0.0.1:5000"
i = 0
max_tasks = 5

if ASYNCIO:
	ctx = zmq.asyncio.Context()
	loop = zmq.asyncio.ZMQEventLoop()
	asyncio.set_event_loop(loop)


	@asyncio.coroutine
	def recv_and_process_zmq():
		global i
		sock = ctx.socket(zmq.PUB)
		# print("Connected in %s" % url)
		print("Bind in %s" % url)
		# sock.connect(url)
		sock.bind(url)

		while True:
			print("Sent %s" % i)
			yield from sock.send_string("%s %s" % ("hola", random.randint(0, 10000)))
			yield from asyncio.sleep(0.0001)
			i += 1

	loop.run_until_complete(recv_and_process_zmq())

else:

	@asyncio.coroutine
	def handle_echo(reader, writer):
		print("handler")

		i = 0
		while True:
			data = yield from reader.readline()

			if not data:
				break

			print("%i - Received %s" % (i, msgpack.unpackb(data)))

			i += 1

		writer.close()

	loop = asyncio.get_event_loop()
	coro = asyncio.start_server(handle_echo, '127.0.0.1', 5000, loop=loop)
	loop.run_until_complete(coro)
	server = loop.run_forever()
