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
from networking.Server import *
from networking.Filter import *

import sexpr

ID = 0


class GameServerFilter(Filter):
    def initialize(self, *args):
        self.user = None
        self.hash = None
        self.game = None
        global ID
        ID += 1
        self.ID = ID
    
    def writeSExpr(self, list):
        self.writeOut(sexpr.sexpr2str(list))
    
    def readOut(self, data):
        print "Receiving message from ", self.ID, ": ", data
        try:
            self.readSExpr(sexpr.str2sexpr(data))
        except ValueError:
            self.writeSExpr(['malformed-message', data])

    def writeOut(self, data):
        print "Sending message to ", self.ID, ": ", data
        Filter.writeOut(self, data)        

    def disconnect(self):
        print self.ID, "disconnect"
        if self.game:
            pass
            #self.readSExpr("(leave-game)")

    def readSExpr(self, expression):
        for i in expression:
            self.evalStatement(i)
    def evalStatement(self, expression):
        if type(expression) != list:
            self.writeSExpr(['invalid-expression', expression])
            return False
        try:
            statements[expression[0]](self, expression)
        except (KeyError, IndexError):
            self.writeSExpr(['malformed-statement', expression])
    
    
    def login(self, user):
        self.user = user
        return True
    def logout(self):
        self.user = None
        self.hash = None
        return True
        

from Statements import statements

server = TCPServer(19000, PacketizerFilter(), CompressionFilter(), GameServerFilter())
server.run()
