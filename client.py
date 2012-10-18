import socket
import uuid

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
		return self.s

	def __exit__(self, type, value, traceback):
		self.s.close()


class ProtelClient(object):
	"""Handle requests and responses to the protel server."""

	def __init__(self, method, headers, body, host=None, port=None):
		self._method = method
		self._headers = headers
		self._body = body
		self._host = host
		self._port = port

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
			result = s.sendall(self.request)
			if result == None:
				# send successful
				response = s.recv(1024)
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

