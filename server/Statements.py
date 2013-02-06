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
import sexpr
import random
import math
import Game

games = {}
id = 0

def verifyLength(self, expression, *lengths):
    if len(expression) not in lengths:
        self.writeSExpr(['argument-count', expression, lengths])
        return False
    return True

def login(self, expression):
    if not verifyLength(self, expression, 2):
        return False
    if  self.user:
        self.writeSExpr(['login-denied', 'already logged in'])
    else:
        if self.login(expression[1]):
            self.writeSExpr(['login-accepted'])
        else:
            self.writeSExpr(['login-denied', 'user already logged in'])

def logout(self, expression):
    if not verifyLength(self, expression, 1):
        return False
    if self.logout():
        self.writeSExpr(['logout-accepted'])
        return True
    else:
        self.writeSExpr(['logout-denied', 'not logged in'])
        return False

def whoAmI(self, expression):
    if not verifyLength(self, expression, 1):
        return False
    self.writeSExpr(['who-you-are', self.user, self.ID])
    return True

def createGame(self, expression):
    global id
    if not verifyLength(self, expression, 1):
       return False
    if not self.user:
        self.writeSExpr(['game-denied', 'not logged in'])
        return False
    if self.game != None:
        self.writeSExpr(['game-denied', 'already in game'])
        return False
    games[id] = Game.Game(id)
    games[id].addPlayer(self)
    self.game = id
    self.writeSExpr(['game-accepted', id])
    id += 1
    return True
    
def listGames(self, expression):
    if not verifyLength(self, expression, 1):
       return False
    self.writeSExpr(['games', games.keys()])
    return True

def joinGame(self, expression):
    if not verifyLength(self, expression, 2):
       return False
    try:
        game = int(expression[1])
    except:
        game = None
    if game not in games:
        self.writeSExpr(['join-denied', 'no such game'])
        return False
    if not games[game].addPlayer(self):
        self.writeSExpr(['join-denied', 'game full'])
        return False
    if self.game is not None:
        self.writeSExpr(['join-denied', 'already in a game'])
        return False
    self.writeSExpr(['join-accepted'])
    self.game = game
    return True

def leaveGame(self, expression):
    if not verifyLength(self, expression, 1):
       return False
    if self.game is None:
        self.writeSExpr(['leave-denied', 'not in a game'])
        return False
    games[self.game].removePlayer(self)
    self.writeSExpr(['leave-accepted'])
    if not len(games[self.game].players):
        del games[self.game]
    self.game = None
    return True

def myGame(self, expression):
    if not verifyLength(self, expression, 1):
       return False
    self.writeSExpr(['your-game', self.game])
    return True

def gameChat(self, expression):
    if not verifyLength(self, expression, 2):
       return False
    if self.game == None:
        self.writeSExpr(['chat-denied', 'no game'])
        return False
    games[self.game].chat(self, expression[1])
    return True

def gameStart(self, expression):
    if not verifyLength(self, expression, 1):
       return False
    if self.game == None:
        self.writeSExpr(['game-denied', 'no game'])
        return False
    if not games[self.game].start():
        self.writeSExpr(['game-denied', 'not ready'])
        return False
    #self.writeSExpr(['game-start-accepted'])
    return True

def winner(self, expression):
    if not verifyLength(self, expression, 2):
       return False
    try:
        game = int(expression[1])
    except:
        game = None
    if game not in games:
        self.writeSExpr(['winner-denied', 'no such game', game])
        return False
    self.writeSExpr(['game-winner', game, games[game].winner and games[game].winner.user])
    return True

def gameStatus(self, expression):
    if not verifyLength(self, expression, 1):
        return False
    if self.game == None:
        self.writeSExpr(['game-status-denied', 'no game'])
        return False
    games[self.game].sendStatus([self])
    return True

def gameMove(self, expression):
    if not verifyLength(self, expression, 4):
        return False
    if self.game == None:
        self.writeSExpr(['game-move-denied', 'no game'])
        return False
    if games[self.game].turn != self:
        self.writeSExpr(['game-move-denied', 'not your turn'])
        return False
    try:
        id = int(expression[1])
        x = int(expression[2])
        y = int(expression[3])
    except:
        self.writeSExpr(['game-move-denied', 'arguments not integers'])
    
    errBuff = games[self.game].moveUnitToPoint(id, x, y)
    if errBuff != True:
        self.writeSExpr(['game-move-denied', errBuff])
        return False
    return True

def gameAttack(self, expression):
    if not verifyLength(self, expression, 4):
        return False
    if self.game == None:
        self.writeSExpr(['game-attack-denied', 'no game'])
        return False
    if games[self.game].turn != self:
        self.writeSExpr(['game-attack-denied', 'not your turn'])
        return False
    try:
        id = int(expression[1])
        x = int(expression[2])
        y = int(expression[3])
    except:
        self.writeSExpr(['game-attack-denied', 'arguments not integers'])

    errBuff = games[self.game].attack(id, x, y)
    if errBuff != True:
        self.writeSExpr(['game-attack-denied', errBuff])
        return False
    return True

def gameBuild(self, expression):
    if not verifyLength(self, expression, 2):
        return False
    if self.game == None:
        self.writeSExpr(['game-build-denied', 'no game'])
        return False
    if games[self.game].turn != self:
        self.writeSExpr(['game-build-denied', 'not your turn'])
        return False
    try:
        type = int(expression[1])
    except:
        self.writeSExpr(['game-build-denied', 'arguments not integers'])


    errBuff = games[self.game].buildUnit(self, type)
    if errBuff != True:
        self.writeSExpr(['game-build-denied', errBuff])
        return False
    return True

def gameGather(self, expression):
    if not verifyLength(self, expression, 4):
        return False
    if self.game == None:
        self.writeSExpr(['game-gather-denied', 'no game'])
        return False
    if games[self.game].turn != self:
        self.writeSExpr(['game-gather-denied', 'not your turn'])
    try:
        id = int(expression[1])
        x = int(expression[2])
        y = int(expression[3])
    except:
        self.writeSExpr(['game-gather-denied', 'arguments not integers'])
        
    errBuff = games[self.game].gather(id, x, y)    
    if errBuff != True:
        self.writeSExpr(['game-gather-denied', errBuff])
        return False
    return True
        

def endTurn(self, expression):
    if not verifyLength(self, expression, 1):
        return False
    if self.game == None:
        self.writeSExpr(['end-turn-denied', 'no game'])
        return False
    if games[self.game].turn != self:
        self.writeSExpr(['end-turn-denied', 'not your turn'])
        return False
    games[self.game].nextTurn()
    return True
    
statements = {}
statements['login'] = login
statements['logout'] = logout
statements['whoami'] = whoAmI
statements['create-game'] = createGame
statements['list-games'] = listGames
statements['join-game'] = joinGame
statements['leave-game'] = leaveGame
statements['my-game'] = myGame
statements['game-chat'] = gameChat
statements['game-start'] = gameStart
statements['winner'] = winner
statements['game-status'] = gameStatus
statements['game-move'] = gameMove
statements['game-attack'] = gameAttack
statements['game-build'] = gameBuild
statements['end-turn'] = endTurn
statements['game-gather'] = gameGather
