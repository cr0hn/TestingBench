# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
import asyncio
import zmq
import zmq.asyncio

url = "tcp://127.0.0.1:5000"
loop = zmq.asyncio.ZMQEventLoop()


@asyncio.coroutine
def recv_and_process(num):

	ctx = zmq.asyncio.Context()

	# sock = ctx.socket(zmq.SUB)
	sock = ctx.socket(zmq.PULL)

	sock.connect(url)
	# sock.setsockopt(zmq.SUBSCRIBE, b'')
	import time
	print("conectado")
	while True:
		msg = yield from sock.recv()  # waits for msg to be ready
		print("Thread-%s # Recv-%s: " % (num, msg))

		yield from asyncio.sleep(0.1)
		# time.sleep(2)


def launcher(num, sem):
	print("Starting:", num)
	asyncio.set_event_loop(loop)

	loop.run_until_complete(recv_and_process(num))

	sem.release()


def main():
	import threading

	threads = []
	sem = threading.BoundedSemaphore(40)
	for x in range(400):
		t = threading.Thread(target=launcher, args=(x, sem, ))
		threads.append(x)

		t.start()

		sem.acquire()


	for x in threads:
		x.join()

if __name__ == '__main__':
	main()
