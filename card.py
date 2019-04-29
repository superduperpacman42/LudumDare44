import pygame
from sprite import Sprite
from constants import *

class Card(Sprite):
    def __init__(self, game, column, suit, number, delay = 0):
        Sprite.__init__(self, game, (column*120+170-5,-200-delay*150), (47*2,62*2))
        self.img = game.loadImage("Card.png")
        self.icon = game.loadImage("Suit"+str(suit)+".png")
        self.suit = suit
        self.number = number
        self.column = column
        self.font = pygame.font.Font("lcd-solid_lcd-solid/LCD_Solid.ttf", 50)
        if number == 1:
            number = 'A'
        if number == 11:
            number = 'J'
        if number == 12:
            number = 'Q'
        if number == 13:
            number = 'K'
        if suit == 1 or suit == 2:
            self.setText(str(number), (255, 0, 0))
        else:
            self.setText(str(number), (0, 0, 0))

    def update(self, dt, hand=False, opponent=False):
        if hand:
            self.pos = (13,75*hand-63)
            if opponent:
                self.pos = (W-357, 75*hand-63)
            self.game.screen.blit(self.icon, self.pos)
            self.drawText((self.size[0]/2+6+47, self.size[1]/2-15))
            return
        self.t += dt/1000
        self.pos = [self.pos[0], self.pos[1]+dt/16]
        self.game.screen.blit(self.img, self.pos)
        self.game.screen.blit(self.icon, self.pos)
        self.drawText((self.size[0]/2+6, self.size[1]/2+40))
        if self.pos[1] >= 350:
            return True

    def __repr__(self):
        return str(self.number)+", "+str(self.suit)