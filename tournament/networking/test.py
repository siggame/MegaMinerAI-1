from Server import *
from Filter import *

class EchoFilter(Filter):
 def readOut(self, data):
  self.writeOut(data)
  print data

server = TCPServer(2100, PacketizerFilter(), CompressionFilter(), EchoFilter())
server.run()
