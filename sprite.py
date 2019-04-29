import pygame
from constants import *

class Sprite:
    def __init__(self, game, pos, size=(50,50), img=None, nimg=1, angle=0, offset=(0,0)):
        self.game = game
        self.size = size
        self.pos = pos
        self.name = img
        self.target = pos
        self.offset = offset
        self.state = "Unfought"
        self.souls = 1
        self.t = 0
        self.layer = 0
        if img:
            self.imgs = game.loadImage(img, nimg)
            if not hasattr(self.imgs, '__iter__'):
                self.imgs = [self.imgs]
            imgs = []
            for i, im in enumerate(self.imgs):
                self.imgs[i] = pygame.transform.scale(im, self.size)
                if angle != 0:
                    imgs.append(pygame.transform.rotate(im, angle))
                else:
                    self.imgs[i] = pygame.transform.rotate(im, angle)
            if angle != 0:
                self.game.images[img+str(angle)] = imgs
                self.imgs = imgs
            if len(self.name)>5 and self.name[:5] == "Human":
                self.gray = self.game.loadImage(img[:6]+"2"+".png")

    def update(self, dt):
        self.t += dt/1000
        if self.souls == 0 and len(self.name)>5 and self.name[:5] == "Human":
            self.draw(self.gray, self.offset)
        else:
            self.draw(self.imgs[int((self.t*5)%len(self.imgs))], self.offset)
        
    def draw(self, img, offset=(0,0)):
        pos = [p-s/2+o+c for p, s, o, c in zip(self.pos, self.size, offset, self.game.offset)]
        self.game.screen.blit(img, pos)

    def drawText(self, offset):
        self.game.screen.blit(self.caption, (self.pos[0] - self.caption.get_width()//2 + offset[0], self.pos[1] - self.caption.get_height()//2 + offset[1]))

    def setText(self, text, color=(255,0,0)):
        self.caption = self.font.render(text, True, color)

    def translate(self, dx, dy):
        target = [p+o for p, o in zip(self.target, [dx,dy])]
        if not self.game.getTile(*target):
            return
        if self.game.getTile(*target).name == "river.png":
            return
        if self.game.getTile(*target).name[:5] == "Human":
            return self.game.getTile(*target)
        self.target = target
        self.hop = 1

    def __repr__(self):
        return self.name[0]