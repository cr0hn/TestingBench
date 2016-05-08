# -*- coding: utf-8 -*-
import json
import random
import asyncio
import zmq
import zmq.asyncio
import msgpack

ASYNCIO = False
url = "tcp://127.0.0.1:5000"
i = 0
max_tasks = 5

if ASYNCIO:
	ctx = zmq.asyncio.Context()
	loop = zmq.asyncio.ZMQEventLoop()
	asyncio.set_event_loop(loop)

	@asyncio.coroutine
	def recv_and_process(x):
		sock = ctx.socket(zmq.SUB)
		print("Connected in %s" % url)
		# print("Listen in %s" % url)
		# sock.bind(url)
		sock.connect(url)
		sock.setsockopt(zmq.SUBSCRIBE, b"hola")
		i = 0
		while True:
			msg = yield from sock.recv()  # waits for msg to be ready
			print("Recv-%s: " % x, msg)
			# yield from sock.send(b"ack")

	loop.run_until_complete(asyncio.wait([recv_and_process(x) for x in range(max_tasks)]))

else:

	@asyncio.coroutine
	def handle_echo(x):

		con = asyncio.streams.open_connection(host="127.0.0.1", port=5000, loop=loop)

		reader, writer = yield from con

		try:
			while True:
				msg = {'hola': "taaaaaaask-%s-%s\n" % (x, random.randint(0, 1000000)), 'adios': True, 'hello': True, 'jelou': True, 'aa': 123}
				msg_p = msgpack.packb(msg)

				print(len(json.dumps(msg)), "#", len(msg_p), "#", ((len(json.dumps(msg)) - len(msg_p))/len(json.dumps(msg)))*100)

				# writer.write(msg.encode("utf-8"))
				writer.write(msg_p)

				yield from asyncio.sleep(0.00001)
				# yield from reader.read()
		except KeyboardInterrupt:
			pass
		# writer.close()
		con.close()

	loop = asyncio.get_event_loop()
	loop.set_debug(True)
	# loop.run_until_complete(asyncio.wait([handle_echo(x) for x in range(max_tasks)]))
	loop.run_until_complete(handle_echo("1"))
