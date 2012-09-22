#!/usr/bin/env python

from tornado import iostream
from tornado.netutil import TCPServer
from tornado import ioloop

class PolicyServer(TCPServer):
	def __init__(self):
		TCPServer.__init__(self, io_loop = None, ssl_options = None)
	def handle_stream(self, stream, address):
		PolicyConnection(stream, address)

class PolicyConnection(object):
	def __init__(self, stream, address):
		self.stream = stream
		self.address = address

		self.stream.read_until('\0', self._on_read_line)

	def _on_read_line(self, data):
		response = '''
<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
	<allow-access-from domain="*" to-ports="*"/>
</cross-domain-policy>
'''
		if 'policy-file-request' in data:
			self.write(response)
		else:
			# bad request
			pass
		self.finish()

	def close(self):
		self.stream.close()

	def write(self, response):
		if not self.stream.closed():
			self.stream.write(response)

	def finish(self):
		if not self.stream.writing():
			self.close()

class BadRequestException(Exception):
	pass

if __name__ == '__main__':
	policyServer = PolicyServer()
	policyServer.listen(843)
	ioloop.IOLoop.instance().start()
