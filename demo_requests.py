from client import protel_request
from functools import partial

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
		with file('examples/{}-{}'.format(title, kind), 'w+') as f:
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

	req = partial(demo_request, target=target)

	#demo_requests(to_stdout)
	req('ValidateReservation with invalid ResNo',
		 'ValidateReservation', 
		 "<Body><ResNo>5</ResNo></Body>")

	req('FindReservationByName - name does not exist', 
		'FindReservationByName', 
		"<Body><Search>Protel</Search></Body>")

	req('FindReservationByRoom - room does not exist',
		'FindReservationByRoom',
	 	"<Body><Room>1408</Room></Body>")


if __name__ == "__main__":		

	demo_requests(STDOUT)

