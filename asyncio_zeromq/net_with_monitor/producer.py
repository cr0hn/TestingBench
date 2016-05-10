# -*- coding: utf-8 -*-

import asyncio

import zmq
import zmq.asyncio

url = "tcp://127.0.0.1:4000"


class ProducerWorker(object):

	def __init__(self, exchange_url, loop=None):

		self.loop = loop or zmq.asyncio.ZMQEventLoop()
		self.exchange_url = exchange_url

	@asyncio.coroutine
	def start_producer(self):
		ctx = zmq.asyncio.Context()

		sock = ctx.socket(zmq.PUSH)

		sock.connect(self.exchange_url)

		i = 0
		print("[+] Starting server")

		while True:
			print("producing-%s" % i)

			yield from sock.send_string("producing-%s" % str(i))

			yield from asyncio.sleep(1)

			i += 10

	def run(self):
		asyncio.set_event_loop(self.loop)

		try:
			self.loop.run_until_complete(self.start_producer())
		except KeyboardInterrupt:
			pass


if __name__ == '__main__':
	ProducerWorker(url).run()
