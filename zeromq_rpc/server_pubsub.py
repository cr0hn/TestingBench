# -*- coding: utf-8 -*-

import zerorpc


class HelloRPC(object):
	def hello(self, name):
		return "Hello, %s" % name


def main():
	s = zerorpc.Server(HelloRPC())
	s.bind("tcp://0.0.0.0:4242")
	s.run()


if __name__ == '__main__':
	main()

