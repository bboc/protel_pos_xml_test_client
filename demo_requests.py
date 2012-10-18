from client import protel_request

HOST = '217.6.121.163'
PORT = 5015              # The same port as used by the server


def to_stdout(title, request, response):
	print "#"*len(title)
	print title
	print "#"*len(title)
	print '------------ Request ------------\n', str(request)
	print '------------ Response------------\n', str(response)


def to_file(title, request, response):

	def write(title, kind, data):
		with file('{}-{}'.format(title, kind), 'w+') as f:
			f.write(data)

	write(title, 'request', request)
	write(title, 'response', response)	

FILE = to_file
STDOUT = to_stdout

def demo_request(title, method, body, headers=None, target=STDOUT):

	request, response = protel_request(method, HOST, PORT, body)	
	print str(target)
	target(title, request, response)

		


def demo_requests(target):

	# ok
	protel_request('ValidateReservation', HOST, PORT, "<Body><ResNo>5</ResNo></Body>")

	headline("FindReservationByName")
	protel_request('FindReservationByName', HOST, PORT, "<Body><Search>Protel</Search></Body>")

	headline("FindReservationByRoom")
	protel_request('FindReservationByRoom', HOST, PORT, "<Body><Room>1408</Room></Body>")





if __name__ == "__main__":		
	target = FILE
	#demo_requests(to_stdout)
	demo_request('ValidateReservation with invalid ResNo',
				 'ValidateReservation', "<Body><ResNo>5</ResNo></Body>", target=target)

