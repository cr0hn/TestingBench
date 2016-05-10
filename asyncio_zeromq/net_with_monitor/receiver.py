# -*- coding: utf-8 -*-

import asyncio
import zmq
import zmq.asyncio

url = "tcp://127.0.0.1:5000"
url_monitor = "tcp://127.0.0.1:9000"


class ReceiverWorker(object):

	def __init__(self, producer_url, monitor_url, loop=None):
		self.monitor_url = monitor_url
		self.exchange_url = producer_url
		self.loop = loop or zmq.asyncio.ZMQEventLoop()

	@asyncio.coroutine
	def status(self):
		ctx = zmq.asyncio.Context()
		sock = ctx.socket(zmq.REQ)

		sock.connect(self.monitor_url)

		print("[*] starting for real_Net")
		yield from sock.send_string("client connected")

		msg_received = yield from sock.recv()
		print(msg_received)

		for x in range(5):
			yield from sock.send_string("client status-%s" % x)

			msg_received = yield from sock.recv()

			print("    - (client) Reveived", msg_received)

			yield from asyncio.sleep(1)

		# Finish de process
		yield from sock.send_string("finish")

	@asyncio.coroutine
	def recv_and_process(self):

		ctx = zmq.asyncio.Context()
		sock = ctx.socket(zmq.PULL)

		sock.connect(self.exchange_url)

		print("[*] Starting receiver")

		while True:
			msg = yield from sock.recv()  # waits for msg to be ready

			print("    - (client) Received: ", msg)

			asyncio.ensure_future(self.status())

	def run(self):
		asyncio.set_event_loop(self.loop)
		self.loop.run_until_complete(self.recv_and_process())


if __name__ == '__main__':
	ReceiverWorker(url, url_monitor).run()
