import pygame
from sprite import Sprite
from constants import *

class Devil(Sprite):
    def __init__(self, game, num=False):
        Sprite.__init__(self, game, [W/2,H/2-50], (500,500))
        self.imgs = game.loadImage("DevilHead.png", 2)
        self.font = pygame.font.Font("lcd-solid_lcd-solid/LCD_Solid.ttf", 34)
        for i, img in enumerate(self.imgs):
            self.imgs[i] = pygame.transform.scale(img, self.size)
        self.t = 0
        self.dialogue = ["Mwahahahahahaha! Your soul is mine!!!",
                         "Enjoy your last few days, foolish mortal...",
                         "Soon enough, you will join me for eternity!!!",
                         "What's that? You want another chance?",
                         "Fine, I'll make you a little deal...",
                         "Bring me back 10 new souls...",
                         "And you can have yours back."]
        if num == 1:
            self.dialogue = ["Do you like to gamble?",
                             "Let's make a bet...",
                             "We'll play a round of poker. If you win...",
                             "You can have anything your heart desires.",
                             "But if I win?",
                             "Your soul is mine!",
                             "Do we have a deal? Excellent..."]
        if num == 2:
            self.dialogue = ["Well done, well done indeed...",
                             "You have honoured our little bargain.",
                             "You are free to go",
                             "These poor souls will take your place.",
                             "It's been a pleasure doing business."]
        self.talkIndex = 0
        self.setText(self.dialogue[self.talkIndex])
        
    def update(self, dt):
        self.t += dt/1000
        if self.talkIndex+1 < len(self.dialogue) and self.t > (self.talkIndex+1) * 2:
            self.talkIndex += 1
            self.setText(self.dialogue[self.talkIndex])
        self.draw(self.imgs[int((self.t*5)%2)])

    def draw(self, img):
        pos = [p-s/2 for p, s in zip(self.pos, self.size)]
        self.game.screen.blit(img, pos)
        self.drawText((0, 200))