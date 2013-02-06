from Server import *
from Filter import *

class PrintFilter(Filter):
    def begin(self):
        self.writeOut("test!" * 4000)
    
    def readOut(self, data):
        print data

class DumpFilter(Filter):
    def readIn(self, data):
        print "Read In: ", data
        Filter.readIn(self, data)
    
    def readOut(self, data):
        print "Read Out: ", data
        Filter.readOut(self, data)

server = TCPServer(None, DumpFilter(), PacketizerFilter(), CompressionFilter(), PrintFilter())
server.openConnection('127.0.0.1', 2100)
server.run()
