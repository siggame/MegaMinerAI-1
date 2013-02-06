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

import pygame
import time
import sexpr 

from GuiHandler import *
from TextureHandler import *


ZOOM = 1
CENTER = [13, 13]
DIMENSIONS = [27, 27]
STATES = []
STATE = 0
NAME1 = ""
NAME2 = ""

pygame.init()
pygame.display.set_mode((1024, 768),pygame.OPENGL|pygame.DOUBLEBUF | pygame.FULLSCREEN)

GUI = GuiHandler(40, 30)
textures = TextureHandler('./sprites/')

class Unit:
    x = 0
    y = 0
    type = ""
    team = 0
    juice = 0
    
    def __init__(self, team, type):
        self.team = team
        self.type = type

    def move(self, x, y):
        self.x, self.y = x, y
    
    def loadSprite(self):
        image = self.type + ".png"
        if self.team == 0:
            color = (0, 119, 255)
        elif self.team == 1:
            color = (255, 0, 0)
        else:
            color = (0, 0, 255)
        textures.load((image, color))
    
    def draw(self):
        global GUI
        self.loadSprite()
        GUI.draw(self.x, self.x+1, self.y, self.y+1)
        if self.juice > 0:
            textures.load(('"' + `self.juice` + '"', (0, 0, 255)))
            GUI.draw(self.x+.5, self.x+1, self.y, self.y+.5)
        

class State:
    units = []
    nodes = []
    score0 = 0
    score1 = 0
    turn = 0
    
    def __init__(self):
        self.units = []
        self.nodes = []
        pass
    
    def setTurn(self, turn):
        self.turn = turn
    
    def setScore0(self, score):
        self.score0 = score
    def setScore1(self, score):
        self.score1 = score


def setWindow():
    global GUI
    global CENTER
    global DIMENSIONS
    global ZOOM
    GUI.setDimensions(CENTER[0] - DIMENSIONS[0]/2.**ZOOM,
                        CENTER[0] + DIMENSIONS[0]/2.**ZOOM,
                        CENTER[1] - DIMENSIONS[1]/2.**ZOOM,
                        CENTER[1] + DIMENSIONS[1]/2.**ZOOM)
def draw():
    global GUI
    global STATES
    global STATE
    global NAME1
    global NAME2
    
    textures.load(('background.png', (128, 128, 128)))
    for i in xrange(int(GUI.l-1), int(GUI.r + 1)):
        for j in xrange(int(GUI.b-1), int(GUI.t + 1)):
            GUI.draw(i, i+1, j, j+1)
    textures.load(('Base.png', (0, 119, 255)))
    GUI.draw(0, 1, 0, 1)
    textures.load(('Base.png', (255, 0, 0)))
    GUI.draw(25, 26, 25, 26)
    
    for i in STATES[STATE].nodes:
        i.draw()
    
    for i in STATES[STATE].units:
        i.draw()
    
    for i in xrange(int(GUI.l-1), int(GUI.r + 1)):
        for j in xrange(int(GUI.b-1), int(GUI.t + 1)):
            num = len([k for k in STATES[STATE].units if k.x == i and k.y == j])
            if num > 0:
                textures.load(('"' + `num` + '"', (0, 0, 0)))
                GUI.draw(i+.6, i+1, j, j+.4)
    title = STATES[STATE].score0 + " - " + STATES[STATE].score1 + " turn: " + `STATE`
    pygame.display.set_caption(title)
    
    label1 = '"' + NAME1 + ':' + STATES[STATE].score0 + '"'
    textures.load((label1, (0, 0, 180)))
    GUI.draw(0,0 + .2 * len(label1),25,26)
    label2 = '"' + NAME2 + ':' + STATES[STATE].score1 + '"'
    textures.load((label2, (180, 0, 0)))
    GUI.draw(24 - .2 * len(label2), 24, 25, 26)
    label3 = '"TURN:' + `STATE` + '"'
    textures.load((label3, (180, 0, 180)))
    GUI.draw(12, 12 + .2 * len(label3), 25, 26)
     
    GUI.clear()

#Misc. utilities

def loadData(file):
    global STATES
    global STATE
    global NAME1
    global NAME2
    
    NAME1 = ""
    NAME2 = ""
    STATES = []
    STATE = 0
    data = sexpr.str2sexpr(file.read())
    
    #("ident" ((2 "Example AI") (3 "Example AI")))
    NAME1 = data[0][1][0][1]
    NAME2 = data[0][1][1][1]
    
    data = data[1:]
    for i in data:
        state = State()
        state.setScore0(i[1][1][1])
        state.setScore1(i[1][2][1])
        for j in i[1][1][2]:
            state.units.append(Unit(0, j[0]))
            unit = state.units[-1]
            unit.x, unit.y = int(j[3]), int(j[4])
        for j in i[1][2][2]:
            state.units.append(Unit(1, j[0]))
            unit = state.units[-1]
            unit.x, unit.y = int(j[3]), int(j[4])
        for j in i[1][3]:
            state.nodes.append(Unit(-1, "Node"))
            node = state.nodes[-1]
            node.x, node.y = int(j[2]), int(j[3])
            node.juice = int(j[1])
        STATES.append(state)

def mainLoop():
    global ZOOM
    global CENTER
    global DIMENSIONS
    global STATE
    global STATES
    quit = False
    running = True
    lastRun = time.time()
    setWindow()
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False
                    STATE = 0
                if event.key == pygame.K_LEFT:
                    running = False
                    if STATE > 0:
                        STATE -= 1
                elif event.key == pygame.K_RIGHT:
                    Running = False
                    if STATE < len(STATES) - 1:
                        STATE += 1
                elif event.key == pygame.K_q:
                    quit = True
                elif event.key == pygame.K_SPACE:
                    running = not running
                    lastRun = time.time()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: #scroll up
                    if ZOOM < 4:
                        ZOOM += 1
                    setWindow()
                elif event.button == 5: # scroll down
                    if ZOOM > 1:
                        ZOOM -= 1
                    setWindow()
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[1]:#the scroll wheel is down
                    CENTER[0] -= event.rel[0] / 800. * DIMENSIONS[0]
                    CENTER[1] += event.rel[1] / 600. * DIMENSIONS[1]
                    setWindow()
        if time.time() > lastRun + .125 and running:
            if STATE < len(STATES) - 1:
                STATE += 1
                lastRun = time.time()
            else:
                if time.time() > lastRun + 5 and running:
                    break
        draw()
    pygame.quit()

if __name__ == '__main__':
    import sys
    data = file(sys.argv[1])
    loadData(data)
    mainLoop()
