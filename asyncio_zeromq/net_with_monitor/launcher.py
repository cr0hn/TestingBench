# -*- coding: utf-8 -*-

import os
import sys
import time

from multiprocessing import Process

listen_monitor = "tcp://*:9000"
listen_exchange_in = "tcp://*:4000"
listen_exchange_out = "tcp://*:5000"

url_exchange_in = "tcp://127.0.0.1:4000"
url_exchange_out = "tcp://127.0.0.1:5000"
url_monitor = "tcp://127.0.0.1:9000"


def main():
	from .monitor import MonitorWorker
	from .producer_proxy import ExchangeWorker
	from .receiver import ReceiverWorker
	from .producer import ProducerWorker

	# Infrastructure
	monitor = MonitorWorker(listen_monitor)
	exchange = ExchangeWorker(listen_exchange_in, listen_exchange_out)

	# Some clients
	client_1 = ReceiverWorker(url_exchange_out, url_monitor)
	client_2 = ReceiverWorker(url_exchange_out, url_monitor)

	# Some producers
	producer_1 = ProducerWorker(url_exchange_in)
	producer_2 = ProducerWorker(url_exchange_in)

	# --------------------------------------------------------------------------
	# Build threads
	# --------------------------------------------------------------------------
	t2 = Process(target=exchange.run)
	t1 = Process(target=monitor.run)

	t5 = Process(target=producer_1.run)
	t6 = Process(target=producer_2.run)

	t3 = Process(target=client_1.run)
	t4 = Process(target=client_2.run)

	threads = [
		t1,
		t2,
		t3,
		t4,
		t5,
		t6
	]

	# --------------------------------------------------------------------------
	# Run!
	# --------------------------------------------------------------------------
	for t in threads:
		t.start()

		time.sleep(0.5)

	# Wait
	try:
		for t in threads:
			t.join()
	except KeyboardInterrupt:
		print("Exiting...")


if __name__ == '__main__':
	parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.insert(1, parent_dir)
	import net_with_monitor

	__package__ = str("net_with_monitor")

	del sys, os

	main()
