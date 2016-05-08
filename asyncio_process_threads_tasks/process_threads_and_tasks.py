# -*- coding: utf-8 -*-
#
# Author: Daniel Garcia (cr0hn) - @ggdaniel
#


import asyncio
import random

from threading import Thread, Event
from multiprocessing import Process


@asyncio.coroutine
def task(con_info, t, e):
	"""
	A task

	:param e: Event obj
	:type e: Event
	"""

	for x in range(200):

		if not e.isSet():
			print("task-", random.randint(1, 100000), "-", t)
			yield from asyncio.sleep(0.5)


# Thread _launch_tasks
def worker(name, state):

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)

	try:
		loop.run_until_complete(asyncio.wait([task(x, name, state) for x in range(10)]))
	except KeyboardInterrupt:

		# Canceling tasks
		tasks = asyncio.Task.all_tasks()

		map(asyncio.Task.cancel, tasks)

		loop.run_forever()
		tasks.exception()
	finally:
		loop.close()


# Thread pool
def launch_threads(proc_number, num=5):
	state = Event()

	th = []

	try:
		for i in range(num):
			n = "proc-%s -- thread-%s" % (proc_number, i)
			t = Thread(target=worker, args=(n, state, ))

			th.append(t)

			# t.daemon = True
			t.start()

		for t in th:
			t.join()

	except KeyboardInterrupt:
		print("\n[*] CTRL+C Caught. Exiting threads form process '%s'..." % proc_number)
	finally:

		state.set()


# Process pool
def launch_processes(num=2):

	ps = []

	try:
		for i in range(num):
			p = Process(target=launch_threads, args=(i, ))

			ps.append(p)

			p.start()

		for x in ps:
			x.join()

	except KeyboardInterrupt:

		for x in ps:
			x.terminate()


if __name__ == '__main__':

	#
	# This code build this process-> threads-> asyncio tasks distribution:
	#
	#   Process -> Thread 1 -> Task 1.1
	#                       -> Task 1.2
	#                       -> Task 1.3
	#           -> Thread 2
	#                       -> Task 2.1
	#                       -> Task 2.2
	#                       -> Task 2.3
	#           -> Thread 3
	#                       -> Task 3.1
	#                       -> Task 3.2
	#                       -> Task 3.3

	launch_processes(2)
