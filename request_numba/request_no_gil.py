# -*- coding: utf-8 -*-

import os

import atexit
import numba
import queue
import daemon
import psutil
import redislite
import requests
import requests_cache
import threading
import time

# print(os.path.dirname(redislite._metadata_file))


# with daemon.DaemonContext():
# 	p = redislite.Redis()

# d = daemon.DaemonContext()
# d.detach_process=False
# d.open()

print("run!")

# time.sleep(2)



try:
	r = redislite.StrictRedis("redis.db", serverconfig=dict(port=6379))
	# r._cleanup = a
	# atexit.unregister(r._cleanup)
	# atexit.unregister(r._cleanup)
	# for x in r.client_list():
	# 	r.client_kill(x['addr'])
	# r.connection_pool.disconnect()
	pid = r.pid

	p = psutil.Process(pid)
	p.kill()

except (BaseException, SystemError):
	pass
except SystemExit:
	pass
except:
	pass


# REDIS_SOCKET_PATH = 'redis://%s' % (rdb.socket_file, )

# requests_cache.install_cache(backend="redis")
# requests_cache.install_cache(backend=REDIS_SOCKET_PATH)


# @numba.jit(nogil=True)
def download(x, q):
	r = requests.get("http://www.noticiasdeoposiciones.com")
	# print(r)
	# return r.text
	# print(x)
	# return r.text
	q.put(r.status_code)

	# sem.release()
	# for x in range(10000):
	# 	(9999900**2000)*x


def main():
	q = queue.Queue()
	# sem = threading.BoundedSemaphore(10)

	threads = [threading.Thread(target=download, args=(x, q, )) for x in range(400)]

	for t in threads:
		t.start()

	for thread in threads:
		thread.join()

	while not q.empty():
		print(q.get())


def main_():
	q = queue.Queue()

	threads = [threading.Thread(target=download, args=(x, q,)) for x in range(400)]

	for t in threads:
		t.start()

	for thread in threads:
		thread.join()

	while not q.empty():
		print(q.get())

if __name__ == '__main__':
	# main()
	pass