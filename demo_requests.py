import argparse
from functools import partial

from client import protel_request


def parse_args():
	parser = argparse.ArgumentParser(description='Send requests to protel test server and print or save responses')
	parser.add_argument('-t', '--target', choices=['file', 'stdout'], default='stdout',
						help='what to do with the output (file|stdout)')
	parser.add_argument('host', help='server host')
	parser.add_argument('port', help='server port')

	return parser.parse_args()


def to_stdout(title, request, response):
	print "#"*len(title)
	print title
	print "#"*len(title)
	print '------------ Request ------------\n', str(request)
	print '------------ Response------------\n', str(response)

def to_file(title, request, response):

	print "writing files for {}".format(title)
	def write(title, kind, data):
		with file('examples/{}-{}'.format(title, kind), 'w+') as f:
			f.write(data)
	write(title, 'request', request)
	write(title, 'response', response)

FILE = to_file
STDOUT = to_stdout

def demo_request(title, method, body='', headers=None, outlet='1', transaction=None, host=None, port=None, target=STDOUT):

	request, response = protel_request(method, host, port, body, headers, outlet, transaction)	
	target(title, request, response)


def demo_requests(target, host, port):

	req = partial(demo_request, target=target, host=host, port=port)

	req('ValidateReservation with invalid ResNo',
		 'ValidateReservation', 
		 "<Body><ResNo>5</ResNo></Body>")


	req('ValidateReservation with valid ResNo',
		 'ValidateReservation', 
		 "<Body><ResNo>533</ResNo></Body>")


	req('FindReservationByName - name does not exist', 
		'FindReservationByName', 
		"<Body><Search>Protel</Search></Body>")

	req('FindReservationByName - name exists', 
		'FindReservationByName', 
		"<Body><Search>Bockelbrink</Search></Body>")

	req('FindReservationByRoom - room does not exist',
		'FindReservationByRoom',
	 	"<Body><Room>1408</Room></Body>")


	req('FindReservationByRoom - room exists (108)',
		'FindReservationByRoom',
	 	"<Body><Room>108</Room></Body>")

	req('FindReservationByRoom - room exists (109)',
		'FindReservationByRoom',
	 	"<Body><Room>109</Room></Body>")


	for i in range(97, 97+26):
		req('FindReservationByName - name exists ({})'.format(chr(i)), 
			'FindReservationByName', 
			"<Body><Search>{}</Search></Body>".format(chr(i)))


if __name__ == "__main__":	
	args = parse_args()	

	if args.target == 'file':
		target = to_file
	else:
		target = to_stdout

	demo_requests(target, args.host, args.port)
