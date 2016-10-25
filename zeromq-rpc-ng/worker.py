# -*- coding: utf-8 -*-

import logging

from .helpers import WorkerMode

logging.basicConfig(level=logging.ERROR, format='[ PRC ] %(asctime)s - %(message)s')
log = logging.getLogger()


class Worker(object):
	"""This worker warps a function"""

	def __init__(self, fn, producer_url, status_service, mode, loop=None):
		self.fn = fn
		self.mode = mode
		self.loop = loop
		self.producer_url = producer_url
		self.status_service = status_service

	def run(self):
		pass

	def on_status(self, message):
		"""This function runs to check status"""

	def on_message(self, message):
		"""Runs when new message is received"""


class WorkerConsumer(object):
	"""This worker warps a function"""

	def __init__(self, fn, producer_url, status_service, mode, loop=None):
		self.fn = fn
		self.mode = mode
		self.loop = loop
		self.producer_url = producer_url
		self.status_service = status_service

	def run(self):
		pass

	def on_status(self, message):
		"""This function runs to check status"""

	def on_message(self, message):
		"""Runs when new message is received"""
