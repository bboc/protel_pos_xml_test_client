import argparse
from functools import partial
import textwrap
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
        with file('examples/{}-{}'.format(title, kind), 'wb+') as f:
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

    req('CloseInvoice (simple)',
         'CloseInvoice', 
         textwrap.dedent("""<Body>
            <Creation>20121020164510</Creation>
            <Outlet>1</Outlet>
            <User>1</User>
            <Invoice>124</Invoice>
            <Item>
                <Type>Revenue</Type>
                <Productgroup>1</Productgroup>
                <TaxClassification>2</TaxClassification>
                <TotalAmount>2.50</TotalAmount>
            </Item>
            <Item>
                <Type>Payment</Type>
                <TotalAmount>2.50</TotalAmount>
                <ResNo>533</ResNo>
            </Item>
            </Body>"""))

    req('CloseInvoice (complex with expenses and gratuity)',
         'CloseInvoice', 
         textwrap.dedent("""<Body>
            <Creation>20121020164510</Creation>
            <Outlet>1</Outlet>
            <User>1</User>
            <Invoice>123</Invoice>
            <Item>
                <Type>Revenue</Type>
                <Text>Astra</Text>
                <Article>115</Article>
                <Productgroup>1</Productgroup>
                <TaxClassification>2</TaxClassification>
                <SingleAmount>2.50</SingleAmount>
                <Quantity>3</Quantity>
                <TotalAmount>7.50</TotalAmount>
            </Item>
            <Item>
                <Type>Revenue</Type>
                <Text>Otternasen im Schlafrock</Text>
                <Article>212</Article>
                <Productgroup>9</Productgroup>
                <TaxClassification>2</TaxClassification>
                <SingleAmount>12.50</SingleAmount>
                <Quantity>1</Quantity>
                <TotalAmount>12.50</TotalAmount>
            </Item>
            <Item>
                <Type>Gratuity</Type>
                <TotalAmount>0.50</TotalAmount>
            </Item>
            <Item>
                <Type>Expense</Type>
                <Text>Zigarren</Text>
                <TotalAmount>300</TotalAmount>
            </Item>
            <Item>
                <Type>Payment</Type>
                <TotalAmount>320.50</TotalAmount>
                <ResNo>533</ResNo>
            </Item>
            </Body>"""))

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


    # for i in range(97, 97+26):
    #     req('FindReservationByName - name exists ({})'.format(chr(i)), 
    #         'FindReservationByName', 
    #         "<Body><Search>{}</Search></Body>".format(chr(i)))


if __name__ == "__main__":  
    args = parse_args() 

    if args.target == 'file':
        target = to_file
    else:
        target = to_stdout

    demo_requests(target, args.host, args.port)
