#!/bin/env python
import popen2
import glob
import random
import time


def startGame(file, svnum):
    proc  = popen2.Popen3(file + " rc0"+str(svnum)+"cslinux.managed.mst.edu 19000")
    while 1:
        line = proc.fromchild.readline()
        if line.startswith("Game created: # "):
    	    return int(line[15:].strip()), proc

def startChild(file, game, svnum):
    proc  = popen2.Popen3(file + " rc0"+str(svnum)+"cslinux.managed.mst.edu 19000 " + `game`)
    return proc
    

#game, child1 = startGame("./client")
#child2 = startChild("./client", game)

#child1.wait()
#child2.wait()

clients = glob.glob("./clients/*")

c1 = random.choice(clients)
c2 = random.choice(clients)
print "Get ready for the fight of the century! Between " + c1 + " and " + c2 + "!!!"
time.sleep(3)

svnum = random.randint(1,3)
game, child1 = startGame(c1, svnum)
child2 = startChild(c2, game, svnum)

#child2.wait()
#child1.wait()
