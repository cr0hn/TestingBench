# -*- coding: utf-8 -*-

import time
import zerorpc

#
# Thanks to:
#
#   https://gist.github.com/kbourgoin/2915148
#
# For their example
#


class TestPuller(object):
	def test(self, msg):
		print(msg.split('.', 1)[0])


def main():

	p = zerorpc.Pusher()
	p.bind('tcp://127.0.0.1:8080')

	i = 0
	# while True:
	for x in range(100000):
		print('sending %i' % x)

		# p('test', ('received %i.' % i) * 100000)  # Huge to see memory usage
		p.test('received %i.' % (x * 100000))  # Huge to see memory usage

		# i += 1

		# time.sleep(0.0001)


if __name__ == '__main__':
	main()

