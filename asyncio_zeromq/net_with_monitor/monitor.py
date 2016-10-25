# -*- coding: utf-8 -*-

import asyncio

import zmq
import zmq.asyncio

url = "tcp://127.0.0.1:9000"


class MonitorWorker(object):
	
	def __init__(self, listen, loop=None):
		
		self.loop = loop or zmq.asyncio.ZMQEventLoop()
		self.listen = listen
	
	@asyncio.coroutine
	def handle_worker(self, sock):
		print("[*] handling new worker")
		
		while True:
			yield from sock.send_string("connected")
			
			msg_received = yield from sock.recv()
			print(msg_received)
			
			if msg_received == "finish":
				print("client finished correctly")
			else:
				print("  - Monitor: ", msg_received)
			
			# yield from asyncio.sleep(1)
	
	@asyncio.coroutine
	def start_worker(self):
		ctx = zmq.asyncio.Context()
		sock = ctx.socket(zmq.REP)
		
		sock.bind(self.listen)
		
		i = 0
		print("[+] Starting monitor")
		
		while True:
			msg = yield from sock.recv()  # waits for msg to be ready
			
			asyncio.ensure_future(self.handle_worker(sock))
	
	def run(self):
		asyncio.set_event_loop(self.loop)
		
		try:
			self.loop.run_until_complete(self.start_worker())
		except KeyboardInterrupt:
			pass


if __name__ == '__main__':
	MonitorWorker(url).run()