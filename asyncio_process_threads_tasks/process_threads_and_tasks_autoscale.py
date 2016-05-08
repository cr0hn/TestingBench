# -*- coding: utf-8 -*-
#
# Author: Daniel Garcia (cr0hn) - @ggdaniel
#


import aiohttp
import asyncio
import random

from threading import Thread, Event, BoundedSemaphore, currentThread
from multiprocessing import Process


class ConcurrentManager:

	def __init__(self, n_process=2, n_threads=5, n_taks=10, daemon=False):
		self.daemon = daemon
		self.n_taks = n_taks
		self.n_threads = n_threads
		self.n_process = n_process

		self.sem_threads = BoundedSemaphore(self.n_threads)
		self.sem_tasks = asyncio.BoundedSemaphore(self.n_taks)

		self.running_process = []

	# --------------------------------------------------------------------------
	# Public methods
	# --------------------------------------------------------------------------
	def run(self):
		self._launch_processes()

	def wait_until_complete(self):
		try:
			for x in self.running_process:
				x.join()
		except KeyboardInterrupt:
			print("\n[*] CTRL+C Caught. ...")

			for x in self.running_process:
				x.terminate()

	@asyncio.coroutine
	def task(self, t, e):
		"""
		A task

		:param e: Event obj
		:type e: Event
		"""

		# if not e.isSet():
		# 	for x in range(100):
		#
		# 		with aiohttp.ClientSession() as session:
		# 			res = yield from session.get('https://api.github.com/events')
		#
		# 			print(res.status)
		#
		# 			# body = yield from res.text()
		#
		# 		yield from asyncio.sleep(1)

		for x in range(200):
				print(t, " - ", currentThread().name, " - task-%s" % random.randint(1, 100000))
				yield from asyncio.sleep(0.5)

	# Thread _launch_tasks
	def worker(self, name, state, sem):

		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)

		try:
			loop.run_until_complete(self._launch_coroutines(loop, name, state))
		except KeyboardInterrupt:

			# Canceling tasks
			tasks = asyncio.Task.all_tasks()

			map(asyncio.Task.cancel, tasks)

			loop.run_forever()
			tasks.exception()
		finally:
			loop.close()
			sem.release()

	# --------------------------------------------------------------------------
	# Private launchers
	# --------------------------------------------------------------------------

	# Thread pool
	def _launch_threads(self, proc_number):
		state = Event()

		th = []

		try:
			while True:

				if state.isSet():
					break

				n = "proc-%s" % proc_number
				t = Thread(target=self.worker, args=(n, state, self.sem_threads, ))

				th.append(t)

				# t.daemon = True
				t.start()

				self.sem_threads.acquire()

			for t in th:
				t.join()

		except KeyboardInterrupt:
			# print("\n[*] CTRL+C Caught. Exiting threads form process '%s'..." % proc_number)
			pass
		finally:

			state.set()

	# Process pool
	def _launch_processes(self):

		try:
			for i in range(self.n_process):
				p = Process(target=self._launch_threads, args=(i,))

				if self.daemon is True:
					p.daemon = True

				self.running_process.append(p)

				p.start()

			if self.daemon is False:
				for x in self.running_process:
					x.join()

		except KeyboardInterrupt:

			for x in self.running_process:
				x.terminate()

				@asyncio.coroutine
				def _launch_coroutines(self, loop, name, state):

					while True:
						if state.isSet():
							break

						yield from self.sem_tasks.acquire()

						loop.create_task(self.task(name, state))

	# Tasks pool
	@asyncio.coroutine
	def _launch_coroutines(self, loop, name, state):

		while True:
			if state.isSet():
				break

			yield from self.sem_tasks.acquire()

			loop.create_task(self.task(name, state))

	# --------------------------------------------------------------------------
	# Scalability methods
	# --------------------------------------------------------------------------
	@property
	def threads_num(self):
		"""
		:return: Return the current active threads
		:rtype: int
		"""
		return self.sem_threads._value

	def threads_inc(self, n):
		"""
		Increases the thread pool in 'n'.

		:param n: number which increment the thread pool
		:type n: int
		"""
		self.sem_threads._value += n

		if self.sem_threads._value < self.sem_threads._initial_value:
			self.sem_threads.release()

	def threads_dec(self, n):
		"""
		Decreases the threads number in 'n'

		:param n: number which decrement the thread pool
		:type n: int
		"""
		if n > 0:
			if self.sem_threads._value - n > 1:
				self.sem_threads._value -= n

	@property
	def tasks_num(self):
		"""
		:return: Return the current active asyncio tasks
		:rtype: int
		"""
		return self.sem_tasks._value

	def tasks_inc(self, n):
		"""
		Increases the asyncio tasks pool in 'n'.

		:param n: number which increment the asyncio Task pool
		:type n: int
		"""
		self.sem_tasks._value += n

		if self.sem_tasks._value < self.sem_tasks._bound_value:
			self.sem_tasks.release()

	def tasks_dec(self, n):
		"""
		Decreases the asyncio Tasks number in 'n'

		:param n: number which decrement the tasks pool
		:type n: int
		"""
		if n > 0:
			if self.sem_tasks._value - n > 1:
				self.sem_tasks._value -= n

if __name__ == '__main__':

	#
	# This code build this process-> threads-> asyncio tasks distribution:
	#
	#   main -> Process 1 -> Thread 1.1 -> Task 1.1.1
	#                                   -> Task 1.1.2
	#                                   -> Task 1.1.3
	#
	#                     -> Thread 1.2
	#                                   -> Task 1.2.1
	#                                   -> Task 1.2.2
	#                                   -> Task 1.2.3
	#
	#           Process 2 -> Thread 2.1 -> Task 2.1.1
	#                                   -> Task 2.1.2
	#                                   -> Task 2.1.3
	#
	#                     -> Thread 2.2
	#                                   -> Task 2.2.1
	#                                   -> Task 2.2.2
	#                                   -> Task 2.2.3
	import time

	# c = ConcurrentManager(n_process=1, n_taks=2, n_threads=2, daemon=True)
	c = ConcurrentManager(n_process=4, n_taks=20, n_threads=10)
	c.run()

	# time.sleep(1)
	#
	# print("Incrementing", "#" * 200)
	# c.threads_inc(4)
	#
	# # time.sleep(2)
	#
	# c.tasks_inc(5)
	# c.wait_until_complete()
