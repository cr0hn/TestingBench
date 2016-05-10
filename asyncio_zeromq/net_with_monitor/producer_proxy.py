import zmq

url_in = "tcp://*:4000"
url_out = "tcp://*:5000"


class ExchangeWorker(object):

	def __init__(self, listen_in, listen_out):

		self.listen_in = listen_in
		self.listen_out = listen_out

	def run(self):

		print("[*] Starting proxy")

		backend = None
		frontend = None
		context = None
		try:
			context = zmq.Context()
			# Socket facing clients
			frontend = context.socket(zmq.PULL)
			frontend.bind(self.listen_in)

			# Socket facing services
			backend = context.socket(zmq.PUSH)
			backend.bind(self.listen_out)

			zmq.device(zmq.FORWARDER, frontend, backend)
		except Exception as e:
			print("bringing down zmq device")
			print(e)
		finally:
			frontend.close()
			backend.close()
			context.term()

if __name__ == "__main__":
	ExchangeWorker(url_in, url_out).run()
