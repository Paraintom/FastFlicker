from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

class FastFlicker(WebSocket):

	clientsAndChannels = {}
	def __init__(self, server, sock, address):
		self.subject = None
		WebSocket.__init__(self, server, sock, address)
		
	def handleMessage(self):
		if self.data is None:
			self.data = ''
		
		msg = str(self.data)
		try:
			if self.subject is None:
				#It is the first message, we echo the subject choosen
				self.subject = msg
				print 'subject choosen : {} '.format(self.subject)
				FastFlicker.clientsAndChannels[self] = self.subject
				self.sendMessage(self.subject)
				return
			self.handleNewMessage(msg)
		except Exception,e:
			print 'Exception while handling message'
			print 'Message: {} '.format(msg)
			print str(e)

	#Forward the message to every listener except the one who wrote the messsage
	def handleNewMessage(self, msg):
		print self.address, 'broadcasting ', msg
		for client, subject in FastFlicker.clientsAndChannels.iteritems():
			if subject == self.subject and client != self:
				client.sendMessage(msg)
		
	def handleConnected(self):
		print self.address, 'connected'

	def handleClose(self):
		del FastFlicker.clientsAndChannels[self]
		print self.address, 'closed'		

server = SimpleWebSocketServer('', 8099, FastFlicker)
server.serveforever()