import socket
import uuid

HOST = '217.6.121.163'
PORT = 5015              # The same port as used by the server


class SocketManager(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port

	def __enter__(self):
		self.s = socket.create_connection((self.host, self.port),5)
		#print "created socket", self.host, self.port, "and connected"
		return self.s

	def __exit__(self, type, value, traceback):
		self.s.close()
		#print "closed"


class ProtelRequest(object):

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
	
			print '------------ Request ------------\n', self.request
			result = s.sendall(self.request)
			if result == None:
				# send successful
				data = s.recv(1024)
				print '------------ Response------------\n', str(data)
			else:
				print "### error while sending ###"


def protel_request(method, host, port, body='', headers=None, outlet='1',transaction=None):

	if transaction == None:
		transaction = str(uuid.uuid1().int)[:9] # protel only supports 9 digits ;-)
	if headers == None:
		headers = dict()

	headers['Transaction'] = transaction
	headers['Outlet'] = outlet

	r = ProtelRequest(method, headers, body, host, port)
	r.send()


def headline(s):
	print "#"*len(s)
	print s
	print "#"*len(s)

#from lxml import etree

# create XML 
#root = etree.Element('root') 
#root.append(etree.Element('child'))
# another child with text
#child = etree.Element('child')
#child.text = 'some text'
#root.append(child)

# pretty string
#s = etree.tostring(root, pretty_print=True)
#print s


if __name__ == "__main__":		
	# ok
	headline("ValidateReservation: invalid Reservation")
	protel_request('ValidateReservation', HOST, PORT, "<Body><ResNo>5</ResNo></Body>")

	headline("FindReservationByName")
	protel_request('FindReservationByName', HOST, PORT, "<Body><Search>Meier</Search></Body>")

	headline("FindReservationByRoom")
	protel_request('FindReservationByRoom', HOST, PORT, "<Body><Room>5</Room></Body>")

