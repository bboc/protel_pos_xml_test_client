import httplib
import time
c = httplib.HTTPConnection('217.6.121.163', 5015)
c.connect()
c.set_debuglevel(99)

c.putheader("POST ValidateReservation HTTP/1.1")
c.putheader("Outlet", '0')
c.putheader("Transaction", '11')

HTTPConnection.endheaders("<Body><ResNo>5</ResNo></Body>")
time.sleep(5)
r = c.getresponse()

print r.getheaders()
print r.msg
print r.read()
c.close()