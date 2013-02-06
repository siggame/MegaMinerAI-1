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

from OpenGL.GL import *
import pygame
import PIL.Image
import os
import math

def nextPow2(n):
    """Returns the next power of 2 that is greater than or equal to n"""
    return int(2 ** math.ceil(math.log(n, 2)))

class TextureHandler:
    def __init__(self, dir, font = None):
        self.dir = dir
        self.images = {}
        if not font:
            self.font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        else:
            self.font = pygame.font.Font(font, 16)
    def load(self, image):
        if image not in self.images:
            print image
            if image[0][0] == image[0][-1] == '"':
                bitmap = self.font.render(image[0][1:-1], True, image[1])
                size = (nextPow2(bitmap.get_width()),nextPow2(bitmap.get_height()))
                buffer = pygame.transform.smoothscale(bitmap, size)
                #buffer = pygame.Surface((32 * (len(image[0]) - 2), 32 * (len(image[0]) - 2)), 0, bitmap)
                #buffer.fill((0, 0, 0, 0))
                #buffer.blit(bitmap, ((16 * (len(image[0]) - 2) - bitmap.get_size()[0] / 2), (16 * (len(image[0]) - 2) - bitmap.get_size()[1] / 2)))
            else:
                try:
                    bitmap = pygame.image.load(os.path.join(self.dir, image[0]))
                    buffer = pygame.Surface(bitmap.get_size(), 0, bitmap)
                    buffer.fill(image[1])
                    buffer.blit(bitmap, (0, 0))
                    print buffer.get_at((0, 0))
                    print buffer.get_at((0, 1))
                    for i in xrange(buffer.get_size()[0]):
                        for j in xrange(buffer.get_size()[1]):
                            if buffer.get_at((i, j)) in [(254, 0, 254, 255), (254, 0, 255, 255), (255, 0, 254, 255), (255, 0, 255, 255)]:
                                buffer.set_at((i, j), (0, 0, 0, 0))
                except pygame.error:
                    bitmap = self.font.render(image[0][0], True, image[1])
                    buffer = pygame.Surface((32, 32), 0, bitmap)
                    buffer.fill((0, 0, 0, 0))
                    buffer.blit(bitmap, ((16 - bitmap.get_size()[0] / 2), (16 - bitmap.get_size()[1] / 2)))
            
            #get image meta-data (dimensions) and data
            ix, iy, bitmap = buffer.get_size()[0], buffer.get_size()[1], pygame.image.tostring(buffer, "RGBA", True)
            
            self.images[image] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.images[image])
            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bitmap)
        glBindTexture(GL_TEXTURE_2D, self.images[image])
         
