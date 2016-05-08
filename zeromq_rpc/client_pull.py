# -*- coding: utf-8 -*-

import zerorpc


class TestPuller(object):
	def test(self, msg):
		print(msg.split('.', 1)[0])


def main():
	p = zerorpc.Puller(TestPuller())
	p.connect('tcp://127.0.0.1:8080')
	p.run()


if __name__ == '__main__':
	main()
