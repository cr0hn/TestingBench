# -*- coding: utf-8 -*-

"""
This file contains helpers for the project
"""

import zmq

from enum import Enum


class WorkerMode(Enum):
	PULL = zmq.PULL
	PUSH = zmq.PUSH

	SUB = zmq.SUB
	PUB = zmq.PUB


class ServiceRegistry(object):

	def __init__(self, address, port, password, role):
		self.port = port
		self.role = role
		self.address = address
		self.password = password


class ServiceDiscover(object):

	def __init__(self, port=None, password=None):
		self.port = port or 50000
		self.password = password


class Services(object):

	def __init__(self, remote_service, monitor_service=None):
		self.monitor_service = monitor_service
		self.remote_service = remote_service
