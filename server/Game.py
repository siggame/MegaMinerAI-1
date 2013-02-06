"""

   Copyright (C) 2008 by Steven Wallace, Ben Murrell
   snwallace@gmail.com, ben@benmurrell.com

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
import random
import math

class ResourceNode:
    def __init__(self, juice, x, y, mult1, mult2, id):
        self.juice = juice
        self.x = x
        self.y = y
        self.mult1 = mult1
        self.mult2 = mult2
        self.id = id
    
    def toList(self):
        list = [self.id, self.juice, self.x, self.y, self.mult1, self.mult2]
        return list
	  

class Unit:
    name = ""
    cost = 0
    maxHP = 0
    attack = 0
    splashRange = 0
    maxMoves = 0
    range = 0
    def __init__(self, player, x, y, id):
        self.x = x
        self.y = y
        self.player = player
        
        self.hp = self.maxHP
        self.attack = self.attack
        self.range = self.range
        self.moves = self.maxMoves
        self.id = id
        
    def newTurn(self, myTurn):
        if myTurn:
            self.moves = self.maxMoves
        else:
            self.moves = 0
        return True
    
    def toList(self):
        list = [self.name, self.id, self.hp, self.x, self.y]
        return list
    
    def toDefineUnitList(self):
        list = [self.name, self.cost, self.maxHP, self.attack, self.maxMoves, self.range]
        return list
    

class Fighter(Unit):
    name = "Fighter"
    cost = 15
    maxHP = 50
    attack = 10
    splashRange = 0
    maxMoves = 2
    range = 1
    def __init__(self, player, x, y, unitID):
        Unit.__init__(self, player, x, y, unitID)
        
class Healer(Unit):
    name = "Healer"
    cost = 45
    maxHP = 100
    attack = -10
    splashRange = 0
    maxMoves = 2
    range = 3
    def __init__(self, player, x, y, unitID):
        Unit.__init__(self, player, x, y, unitID)
        
class Bomber(Unit):
    name = "Bomber"
    cost = 20
    maxHP = 20
    attack = 15
    splashRange = 4
    maxMoves = 3
    range = 0
    def __init__(self, player, x, y, unitID):
        Unit.__init__(self, player, x, y, unitID)
        
class Sniper(Unit):
    name = "Sniper"
    cost = 35
    maxHP = 30
    attack = 25
    splashRange = 0
    maxMoves = 1
    range = 6
    def __init__(self, player, x, y, unitID):
        Unit.__init__(self, player, x, y, unitID)

unitTypes = [Fighter, Healer, Sniper, Bomber]

class Game:
    def __init__(self, id):
        self.players = [] #list of player objects
        self.units = []
        self.resourceNodes = []
        self.turn = None #the player whose turn it is; None before and after the game.
        self.turnNum = 0
        self.maxTurns = 400
        self.id = id
        self.winner = None #the player who won, set after the game  is ended
        self.unitID = 0
        self.resourceID = 0
        random.seed()
    
    #Gameplay functions
    def createResource(self, x, y, juice):
        if self.unitAt(x,y):
            return False
        if self.nodeAt(x,y):
            return False
        if (x == 0 and y == 0) or (x == 25 and y == 25):
            return False
        self.resourceID += 1
        #multiplier between 1 and 10 (35.3553391 = distance from 0 0 to 25 25, 17.5 = half) ceil(dist / 3.5)
        #mult1 for (0,0), mult2 for (25,25)
        self.resourceNodes.append(ResourceNode(juice, x, y, math.ceil(math.sqrt(math.pow(0-x,2) + math.pow(0-y,2))/3.5), math.ceil(math.sqrt(math.pow(25-x,2) + math.pow(25-y,2))/3.5), self.resourceID))
        return True
    
    def makeUnit(self, player, type):
        if player not in self.players:
            return False
        if(player is self.players[0]):
            return self.addUnit(player, type, 0, 0)
        if(player is self.players[1]):
            return self.addUnit(player,type, 25, 25)
        return False
    
    def addUnit(self, player, type, x, y):
        if self.unitAt(x, y):
            if self.unitAt(x,y) not in self.unitsForPlayer(player):
                return False
        if self.nodeAt(x,y):
            return False
        self.unitID += 1
        self.units.append(type(player, x, y, self.unitID))
        self.units[-1].moves = 0
        return True
    
    def buildUnit(self, player, num):
        if player not in self.players:
            return ("player does not exist")
        if not 0 <= num < len(unitTypes):
            return (str(num)+" is an invalid unit type number")
        type = unitTypes[num]
        if type.cost > player.resources:
            return ("Player has insufficient points to buy: "+str(num))
        if not self.makeUnit(player, type):
            return ("Unable to create unit")
        player.resources -= type.cost
        return True
    
    def moveUnitToPoint(self, id, x, y):
        if not self.getUnit(id): #check whether the unit exists
            return (str(id)+" does not exist")
        unit = self.getUnit(id)
        if (max(abs(unit.x - x) , abs(unit.y - y))) > 1:
            return (str(id)+" cannot move to non-adjaced square") #bad move
        if self.unitAt(x, y):
            if self.unitAt(x,y) not in self.unitsForPlayer(unit.player):
                return (str(id)+" cannot move onto enemy units") #occupied
        if self.nodeAt(x,y):
            return (str(id)+" cannot move into a resource node") #occupied
        if unit.moves < 1:
            return (str(id)+" is out of moves for this turn") #cannot move
        if unit.player != self.turn:
            return (str(id)+" is not your unit")#not your unit!
        if x > 25 or x < 0 or y > 25 or y < 0:
            return (str(id)+" cannot move out of bounds") #out of ranges
        if (unit.player == self.players[0] and x == 25 and y ==25) or (unit.player == self.players[1] and x==0 and y ==25):
            return (str(id)+" cannot move onto the enemy base") #going onto enemy base
            
        unit.moves -= 1
        unit.x = x
        unit.y = y
        return True
    
    def moveUnit(self, id, direction):
        if not self.getUnit(id): #check whether the unit exists
            return False
        unit = self.getUnit(id)
        x = unit.x
        y = unit.y
        if direction & 1:
            if direction & 2:
                y -= 1
            else:
                y += 1
        else:
            if direction & 2:
                x -= 1
            else:
                x += 1
        return self.moveUnitToPoint(unit, id, x, y)
    
    def attack(self, id, x, y):
        if not self.getUnit(id): #check whether the unit exists
            return (str(id)+" does not exist")
        unit = self.getUnit(id)
        print 1
        
        #Check attack range
        if (max(abs(unit.x - x),abs(unit.y - y))) > 1 or unit.range == 0: #Special case for the diagonal 
            if (abs(unit.x - x) + abs(unit.y - y)) > unit.range: #Manhattan distance 
                return (str(id)+" tried to attack out of range") #out of range
        
        print 2
        if not self.unitAt(x, y):
            unit.moves -= 1
            return (str(id)+" attacked an empty space") #no target
        print 3
        if unit.moves < 1:
            return (str(id)+" is out of moves") #cannot move
        print 4
        if unit.player != self.turn:
            return (str(id)+" is not your unit") #not your unit!
        print 5
        unit.moves -= 1
        
        #Diamond shaped splash attack (see excel file)
        splashRange = unit.splashRange
        if unit.splashRange > 0:
            print unit.x, unit.y, unit.splashRange
            for i in range(unit.x-splashRange, unit.x+splashRange):
                for j in range(unit.y-splashRange, unit.y+splashRange):
                    if i >= 0 and i <= 25 and j >= 0 and j <= 25:
                        if ((abs(unit.x-i) + abs(unit.y-j)) <= splashRange) or (max(abs(unit.x - x),abs(unit.y - y)) == 1):
                            units = self.unitsAt(i,j)
                            if units:
                                for u in units:
                                    self.damage(unit, u)
        #Non splash attack
        else:
            for i in self.unitsAt(x,y):
                self.damage(unit, i)
	print 6
        #Bomber kills himself
        if unit.name == "Bomber":
            self.units.remove(unit)
        print 7
        return True
    

    def damage(self, attacker, target):
        if attacker not in self.units or target not in self.units:
            return False
        
        #Disable friendly fire
        if target in self.unitsForPlayer(attacker.player):
            if(attacker.attack > 0):
                return False

        #only receive half damage if you're in a base (but don't reduce healing power)
        coeff = 1
        if( ((target.x is 0 and target.y is 0) or (target.x is 25 and target.y is 25)) and attacker.attack > 0 ):
            coeff = 0.5
        
        target.hp -= coeff*attacker.attack
        
        healCoeff = 1.5
        
        if target.hp <= 0:
            self.units.remove(target)
        if target.hp >= int(math.ceil(target.maxHP*healCoeff)):
            target.hp = int(math.ceil(target.maxHP*healCoeff))
        return True
    

    def gather(self, id, x, y):
        if not self.getUnit(id):
            return (str(id)+" does not exist")
        unit = self.getUnit(id)
        if (max(abs(unit.x - x) , abs(unit.y - y))) > 1:
            return (str(id)+" tried to gather out of range") #out of range
        if not self.nodeAt(x,y):
            unit.moves -= 1
            return (str(id)+" gathered from an empty space") #no target
        if unit.moves < 1:
            return (str(id)+" is out of moves") #out of moves
        if unit.player != self.turn:
            return (str(id)+" is not your unit") #not your unit!
        unit.moves -= 1
        self.collect(unit, self.nodeAt(x,y))
        return True
    
    #administrative functions
    def addPlayer(self, player):
        if len(self.players) < 2:
            self.players.append(player)
            player.resources = 0
            return True
        return False
    
    def removePlayer(self, player):
        try:
            self.players.remove(player)
            if self.turn:
                self.turn = None
                self.winner = self.players[0] #the remaining player
                for i in self.players:
                    i.writeSExpr(['game-over', self.id])
                print "Game " + `self.id` + " ended! Winner:" + self.winner.user
            return True
        except:
            return False
    
    def unitsForPlayer(self, player):
        list = [i for i in self.units if i.player == player]
        return list
    
    def unitListsForPlayer(self, player):
        list = self.unitsForPlayer(player)
        return [i.toList() for i in list]
    
    def start(self):
        if len(self.players) != 2 or self.turn or self.winner:
            return False
        for i in self.players:
            i.resources = 100
        #self.makeUnit(self.players[0], Fighter)
        #self.makeUnit(self.players[1], Fighter)
        self.createResource(12,13, 25)
        self.createResource(13,12, 25)
        self.createResource(12,12, 25)
        self.createResource(13,13, 25)
        
        self.turn = self.players[1]
        self.turnNum = 0
        self.sendUnitTypes(self.players)
        self.sendIdent(self.players)
        self.nextTurn()
        return True
    
    def sendStatus(self, players):
        if self.turn == None:
	       list = [None]
	       resourceList = []
        else:
            list = [self.turnNum]
            resourceList = []
        for i in self.players:
            list += [[i.ID, i.resources, self.unitListsForPlayer(i)]]
        for i in self.resourceNodes:
            resourceList += [i.toList()]
        list += [resourceList]
        for i in players:
            i.writeSExpr(['status', list])
            
    def sendIdent(self, players):
        if len(self.players) != 2:
            return False #bad bad bad
        list = []
        for i in self.players:
            list += [[i.ID, i.user]]
            
        for i in players:
            i.writeSExpr(['ident', list])
            
    def sendUnitTypes(self, players):
        list = []    
        for i in unitTypes:
            list += [[i.name, i.cost, i.maxHP, i.attack, i.maxMoves, i.range]]
        for i in players:
            i.writeSExpr(['unit-types', list])   

               
    #utility functions
    def chat(self, player, message):
        for i in self.players:
            i.writeSExpr(['says', player.user, message])
        return True
    
    def nextTurn(self):
        if (not self.turn) or self.winner:
            return False
        self.turn = [i for i in self.players if i != self.turn][0]
        for i in self.units:
            i.newTurn(self.turn == i.player)
        self.turnNum += 1

        if (self.turnNum >= self.maxTurns) or (self.players[0].resources < 15 and len(self.unitsForPlayer(self.players[0])) == 0) or (self.players[1].resources < 15 and len(self.unitsForPlayer(self.players[1])) == 0):
            if self.players[0].resources >= self.players[1].resources:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
            for i in self.players:
                i.writeSExpr(['game-over', self.winner.ID])
                print "Game " + `self.id` + " ended! Winner:" + self.winner.user
                
            self.sendStatus(self.players)
            self.turn = None
            return True
        for i in self.players:
            i.writeSExpr(['new-turn', self.turn.ID])
        self.sendStatus(self.players)
        return True
    
    def unitAt(self, x, y):
        unit = [i for i in self.units if i.x == x and i.y == y]
        if not unit:
            return False
        return unit[0]
    
    def unitsAt(self, x, y):
        unit = [i for i in self.units if i.x == x and i.y == y]
        if not unit:
            return False
        return unit
    
    def nodeAt(self, x, y):
        node = [i for i in self.resourceNodes if i.x == x and i.y == y]
        if not node:
            return False
        return node[0]
        
    def getNode(self, id):
        node = [i for i in self.resourceNodes if i.id == id]
        if not node:
            return False
        return node[0]
    
    def getUnit(self, id):
        unit = [i for i in self.units if i.id == id]
        if not unit:
            return False
        return unit[0]

    def collect(self, collecter, target):
        if collecter not in self.units or target not in self.resourceNodes:
            return False
        if(collecter.player is self.players[0]):
            juiceCollected = 1*target.mult1
        if(collecter.player is self.players[1]):
            juiceCollected = 1*target.mult2
            
    	target.juice -= 1 #only take out one per hit
        (collecter.player).resources += juiceCollected
        if target.juice <= 0:
            self.resourceNodes.remove(target)
            placed = False
            while not placed:
                x = random.randint(0,25)
                y = random.randint(0,25)
                placed = self.createResource(x,y, 25)
        return True
                
