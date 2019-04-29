import pygame
from sprite import Sprite
from constants import *

class Player(Sprite):
    def __init__(self, game, pos, color=False):
        Sprite.__init__(self, game, pos, (50,50))
        self.img = game.loadImage("Player2.png")
        self.jump = game.loadImage("PlayerJump2.png")
        self.layer = 5
        self.souls = 0
        if color:
            self.img = game.loadImage("Player.png")
            self.souls = 1
        self.img = pygame.transform.scale(self.img, self.size)
        self.jump = pygame.transform.scale(self.jump, self.size)
        self.hop = 0

    def update(self, dt):
        self.t += dt/1000
        self.pos = [self.approach(x, xdes, 0.4/2) for x, xdes in zip(self.pos, self.target)]
        dy = 0
        if self.hop > 0:
            self.hop -= dt/150/2
            self.hop = max(0, self.hop)
            dy -= (.25-(self.hop-.5)**2)*40
            self.draw(self.jump, (0,-10+dy))
        else:
            self.draw(self.img, (0,-10))

    def approach(self, x, xdes, dx, snap=5):
        err = abs(xdes-x)
        if x > xdes+snap:
            x -= dx*err
        elif x < xdes-snap:
            x += dx*err
        else:
            x = xdes
        return x