import socket
import uuid

HOST = '217.6.121.163'
PORT = 5015              # The same port as used by the server

VERBOSE = False

class SocketManager(object):
	"""
	Context manager for the actual socket, so we make sure that the 
	socket is closed

	"""
	def __init__(self, host, port):
		self.host = host
		self.port = port

	def __enter__(self):
		self.s = socket.create_connection((self.host, self.port),5)
		#print "created socket", self.host, self.port, "and connected"
		return self.s

	def __exit__(self, type, value, traceback):
		self.s.close()
		print "closed"


class ProtelClient(object):
	"""Handle requests and responses to the protel server."""


	def __init__(self, method, headers, body, host=None, port=None):
		self._method = method
		self._headers = headers
		self._body = body
		self._host = host
		self._port = port
		self.verbose = VERBOSE

	@property
	def request(self):
		return ''.join(list((self.header, "\r\n", self._body)))

	@property
	def header(self):

		# create header
		hdr = list()
		hdr.append("POST {} HTTP/1.1".format(self._method))
		for key in self._headers:
			hdr.append("{}: {}".format(key, self._headers[key]))
		hdr.append("Content-length: {}".format(len(self._body)))
		hdr.append('') # end of header
		return "\r\n".join(hdr)

	def send(self):

		with SocketManager(self._host, self._port) as s:
	
			if self.verbose: print '------------ Request ------------\n', self.request
			result = s.sendall(self.request)
			if result == None:
				# send successful
				response = s.recv(1024)
				if self.verbose: print '------------ Response------------\n', str(response)
				return response

			else:
				print "### error while sending ###"


def protel_request(method, host, port, body='', headers=None, outlet='1',transaction=None):

	if transaction == None:
		transaction = str(uuid.uuid1().int)[:9] # protel only supports 9 digits ;-)
	if headers == None:
		headers = dict()

	headers['Transaction'] = transaction
	headers['Outlet'] = outlet

	r = ProtelClient(method, headers, body, host, port)
	return r.request, r.send()





def headline(s):
	if VERBOSE:
		print "#"*len(s)
		print s
		print "#"*len(s)


def demo_request(title, method, body, headers=None):
	headline(title)
	request, response = protel_request(method, HOST, PORT, body)	

	def write(title, kind, data):
		with file('{}-{}}'.format(title, kind), 'w+') as f:
			f.write(data)

	write(title, 'request', request)
	write(title, 'response', response)
		


def demo_requests():
	globals()['VERBOSE'] = True

	# ok
	headline("ValidateReservation: invalid Reservation")
	protel_request('ValidateReservation', HOST, PORT, "<Body><ResNo>5</ResNo></Body>")

	headline("FindReservationByName")
	protel_request('FindReservationByName', HOST, PORT, "<Body><Search>Protel</Search></Body>")

	headline("FindReservationByRoom")
	protel_request('FindReservationByRoom', HOST, PORT, "<Body><Room>1408</Room></Body>")



if __name__ == "__main__":		

	demo_requests()

