"""

   Copyright (C) 2008 by Steven Wallace
   snwallace@gmail.com

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the
    Free Software Foundation, Inc.,
    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 """
import struct

import sys, traceback

class NetworkException(Exception):
    pass

class Filter:
    def __init__(self, *args):
        self.input = None
        self.output = None
        self.__args = args #save the args for duplication
        self.server = False
        self.master = None

        self.initialize(*args) #overridable initializer

    def initialize(self, *args):
        pass

    def duplicate(self):
        return self.__class__(*self.__args) #finds the objects class, and returns
                                        #a new object of the same type


    def connect(self):
        if self.output:
            self.output.connect()

    def disconnect(self):
        if self.input:
            self.input.disconnect()
    
    def begin(self):
        if self.input:
            self.input.begin()
           
    def end(self):
        if self.output:
            self.output.end()


    def setIn(self, input = None):
        self.input = input

    def setOut(self, output = None):
        self.output = output

    def readIn(self, data):
        self.writeOut(data)

    def readOut(self, data):
        self.writeIn(data)

    def writeIn(self, data):
        if self.input:
            self.input.readOut(data)

    def writeOut(self, data):
        if self.output:
            self.output.readIn(data)


    def error(self, error):
        raise NetworkException(error)


class PacketizerFilter(Filter):
    def initialize(self):
        self.received = ""
        
    def readOut(self, data):
        self.received += data
        while len(self.received) > 3:
            length ,= struct.unpack("!i",self.received[:4])
            if length + 4 <= len(self.received):
                self.writeIn(self.received[4:length+4])
                self.received = self.received[length+4:]
            else:
                return
    def writeOut(self, data):
        Filter.writeOut(self, struct.pack("!i",len(data))+data)

class CompressionFilter(Filter):
    def initialize(self):
        self.algorithms = {}
        self.otherAlgorithms = []
        self.initialized = False
        try:
            import zlib
            self.algorithms['z'] = zlib
        except:
            pass
        try:
            import bz2
            self.algorithms['b'] = bz2
        except:
            pass
        try:
            import noCompress
            self.algorithms['n'] = noCompress
        except:
            pass
        
    def begin(self):
        if self.server:
            self.writeOut(''.join(self.algorithms.keys()))
        
    def readOut(self, data):
        if not self.initialized:
            if self.server:
                self.otherAlgorithms = [i for i in data]
                self.initialized = True
                Filter.begin(self)
            else:
                self.otherAlgorithms = [i for i in data]
                self.writeOut(''.join(self.algorithms.keys()))
                self.initialized = True
                Filter.begin(self)
        else:
            algorithm = data[0]
            if algorithm not in self.algorithms:
                self.error("UNKNOWN COMPRESSION ALGORITHM " + data)
            self.writeIn(self.algorithms[algorithm].decompress(data[1:]))
    def writeOut(self, data):
        if not self.initialized:
            Filter.writeOut(self, data)
        else:
            algorithm = 'n'
            newData = data
            for i in self.otherAlgorithms:
                if i in self.algorithms:
                    tmpData = self.algorithms[i].compress(data, 9)
                    if len(tmpData) < len(newData):
                        newData = tmpData
                        algorithm = i
            Filter.writeOut(self, ''.join((algorithm, newData)))


class TCPFilter(Filter):
    def initialize(self, connection = None):
        self.connection = connection

    def writeOut(self, data):
        if self.connection:
            try:
                self.connection.send(data)
            except:
                self.disconnect()
        #Filter.writeOut(self, data)
        
    def poll(self):
        try:
            data = self.connection.recv(4096)
            if data:
                self.readOut(data)
            else:
                self.disconnect()
        except:
            print "bleh!"
            traceback.print_exc(file=sys.stdout)
            self.disconnect()

    def connect(self):
        self.begin()

    def disconnect(self):
        self.master.remove(self.connection)
        if self.connection:
            self.connection.close()
        Filter.disconnect(self)

    def end(self):
        self.disconnect()
