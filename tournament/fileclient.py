import sys
import time

from networking.Server import *
from networking.Filter import *


class ConnectionWrapper:
    def __init__(self):
        import thread
        
        
        self.server = TCPServer(None,  PacketizerFilter(), Filter())
        self.connection = None
        thread.start_new_thread(self.run_server, ())
    
    def connect(self, server, port, filters = []):
        if self.connection:
            self.disconnect()
        if filters:
            self.server.filters = filters
        self.connection = self.server.openConnection(server, port)
    
    def disconnect(self):
        if not self.connection:
            return False
        self.connection.end()
    
    def send(self, f, n):
        if not self.connection:
            return False
        self.connection.writeOut(n + "\n" + file(f, 'rb').read())
        #time.sleep(5)
        
        
    def run_server(self):
        try:
            self.server.run()
        except Exception, e:
            print e
    
if __name__ == "__main__":
    w = ConnectionWrapper()
    w.connect(sys.argv[1], int(sys.argv[2]))
    w.send(sys.argv[3], sys.argv[4])
