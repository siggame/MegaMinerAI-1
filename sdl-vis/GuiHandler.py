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
from OpenGL.GL import *
from OpenGL.GLU import *
class GuiHandler(object):
    def __init__(self, x, y):
        self.l = 0
        self.b = 0
        self.r = x
        self.t = y
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        self.setView()
    
    def setSize(self, x, y):
        self.r = x
        self.t = y
        self.setView()
    
    def setDimensions(self, l, r, b, t):
        self.l = l
        self.b = b
        self.r = r
        self.t = t
        self.setView()
    
    def setView(self):
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(self.l, self.r, self.b, self.t)
        glMatrixMode(GL_MODELVIEW)
    
    def draw(self, l, r, b, t):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex2f(l, b)
        glTexCoord2f(1.0, 0.0); glVertex2f(r, b)
        glTexCoord2f(1.0, 1.0); glVertex2f(r, t)
        glTexCoord2f(0.0, 1.0); glVertex2f(l, t)
        glEnd()
    
    def clear(self):
        pygame.display.flip()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity() 
