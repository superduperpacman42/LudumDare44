import logo
import pygame
import sys
import os
import random
import numpy as np
import time
from devil import Devil
from sprite import Sprite
from player import Player
from card import Card
from constants import *
from level import *

class Game:

    def __init__(self):
        self.screen = logo.display(caption="Demonic Dealings")
        self.screen = pygame.display.set_mode([W, H])
        self.sprites = []
        self.font = pygame.font.Font("lcd-solid_lcd-solid/LCD_Solid.ttf", 30)
        self.fontBig = pygame.font.Font("lcd-solid_lcd-solid/LCD_Solid.ttf", 70)
        self.t = 0
        self.level = -4
        self.grid = None
        self.player = Player(self, (0,0),color=True)
        self.fighting = False
        self.background = self.loadImage('Table.png')
        self.cards = []
        self.hand = []
        self.key = 0
        self.instructions = 0
        self.text = ""
        self.opponentHand = []
        self.loadImage('CardSlot.png')
        self.loadImage('Card.png')
        self.loadImage('SelectedSlot.png')
        self.images['CardSlot.png'] = pygame.transform.scale(self.images['CardSlot.png'], (110, 140))
        self.images['Card.png'] = pygame.transform.scale(self.images['Card.png'], (110, 140))
        self.images['SelectedSlot.png'] = pygame.transform.scale(self.images['SelectedSlot.png'], (126, 156))
        self.challengeText = [["You want to bet your", "soul against mine?", "You're on!"],
                              ["A soul for a soul?","It's a bet!"],
                              ["You want my soul?","You gotta beat me first!"]]
        self.soullessText = [["You already took my soul!", "What more do you want?"],
                             ["My parents warned me", "not to gamble..."],
                             ["Are you back to gloat?"]]
        self.cockyText = [["Double or nothing?"],["Let's raise the stakes!"]]
        self.winText = [["Ha, another soul", "for my collection!"],
                        ["Like taking candy", "from a baby..."],
                        ["Better luck next time,", "sucker!"]]
        self.loseText = [["Congratulations,", "my soul is yours."],
                         ["Well played."],
                         ["You just got lucky."],
                         ["Take my soul then,", "see if I care."]]
        self.deck = []
        for i in range(4):
            for j in range(1,14):
                self.deck += [(i,j)]
        self.run()


    def run(self):
        clock = pygame.time.Clock()
        self.pause = False
        while not self.pause:
            for event in pygame.event.get():
                if event.type is pygame.KEYDOWN:
                    self.keyPressed(event.key)
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            dt = clock.tick(TIME_STEP)
            self.t += dt/1000
            self.update(dt)
            pygame.display.flip()
            # pygame.display.update()

    def update(self, dt):
        if self.level == -4:
            self.sprites += [Devil(self, 1)]
            self.level = -3
            self.playMusic("DemonicDealings.wav",1)
        elif self.level == -3 and self.t > 14:
            self.level = -2
            self.t = 0
            self.sprites = []
        elif self.level == -2:
            self.fighting = Sprite(self, (-1000,-1000), img="Devil.png")
            self.level = -1
            self.opponentHand = self.getOpponentHand('!')
        elif self.level == 0:
            self.playSound('laugh.wav')
            self.playMusic("DemonicDealings.wav",1)
            self.sprites += [Devil(self)]
            self.level = 1
        elif self.level == 1 and self.t > 14:
            self.level = 2
            self.load(0)
            self.playMusic("SoulSearch.wav")
        elif self.level == 3:
            self.sprites = [Devil(self, 2)]
            self.level = 4
            self.playMusic("DemonicDealings.wav", 1)
        elif self.level == 4 and self.t > 10:
            self.playSound('laugh.wav')
            time.sleep(1)
            pygame.display.quit()
            time.sleep(6)
            sys.exit()
        if self.fighting:
            self.screen.blit(self.background, (0,0))
        else:
            self.screen.fill((0,0,0))
        if self.player:
            self.offset = (W/2-self.player.pos[0], H/2-self.player.pos[1])
        # NOT IN COMBAT
        if not self.fighting:
            for s in self.sprites:
                s.update(dt)
            if self.player and self.level > 1 and self.level < 3:
                self.caption = self.font.render("$ouls: " + str(self.player.souls), True, (255,255,255))
                self.screen.blit(self.caption, (10,10))
        elif self.player:
            # CARD COMBAT
            im = pygame.transform.scale(self.player.img, (200,200))
            self.screen.blit(im, (-20, 300))
            im2 = pygame.transform.scale(self.fighting.imgs[0], (200,200))
            self.screen.blit(im2, (620, 300))
            self.screen.blit(self.loadImage('ScoreCard.png'), (W-200,0))
            # arrow = self.loadImage('Arrow.png')
            angles = [180, 90, 0, 270]
            slot = self.loadImage('CardSlot.png')
            sel = self.loadImage('SelectedSlot.png')
            klist = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]
            # setup
            if self.level > 1:
                if self.fighting.state == "Defeated" and self.text == "":
                    self.text = self.soullessText[random.randint(0,2)]
                    self.opponentHand = []
                elif self.fighting.state == "Victorious" and self.text == "":
                    self.text = self.cockyText[0]
                elif self.text == "":
                    self.text = self.challengeText[random.randint(0,2)]
            elif len(self.hand)==0:
                if self.instructions==0:
                    self.text = ["Select a column using", "the arrow keys", "or number keys", "(press any key to continue)"]
                elif self.instructions==1:
                    self.text = ["Catch cards as they fall", "to create a winning hand", "(press any key to continue)"]
                elif self.instructions==2:
                    self.text = ["Refer to the score card", "to see which hands", "can beat your opponent", "(press any key to continue)"]
            # begin
            if len(self.cards) == 0 and (self.t > 2 and self.level>1):
                if self.fighting.state == "Defeated":
                    self.fighting = None
                    self.text = ""
                    # self.playMusic("SoulSearch.wav")
                else:
                    if len(self.opponentHand) > 0:
                        self.loadCards()
                    self.key = 0
            if len(self.cards) == 0 and (self.instructions==3 and self.level<=1):
                self.loadCards()
                self.playMusic("RiskyBusiness.wav",1)
                self.key = 0
            # playing
            if len(self.cards) and len(self.hand)<3:
                self.text = ""
                for i in range(4):
                    # a = pygame.transform.scale(pygame.transform.rotate(arrow, angles[i]), (100,100))
                    if i == self.key:
                        self.screen.blit(sel, (i*120+170-13, 350-8))
                    else:
                        self.screen.blit(slot, (i*120+170-5, 350))
                    caption = self.fontBig.render(str(i+1), True, (27,91,0))
                    self.screen.blit(caption, (i*120+197, 390))

                    # self.screen.blit(a, (i*120+170, 370))
                for c in self.cards[:]:
                    if c.update(dt):
                        self.cards.remove(c)
                        if self.key == c.column:
                            self.hand += [c]
                            self.t = 0
                            if len(self.hand) >= 3:
                                win = self.score(self.opponentHand) <= self.score(self.hand)
                                if self.level <= 1:
                                    self.text = ["Uh oh! It looks like", "you lost..."]
                                    self.playSound('Lose.wav')
                                elif win:
                                    self.text = self.loseText[random.randint(0,2)]
                                    self.playSound('Win.wav')
                                else:
                                    self.text = self.winText[random.randint(0,2)]
                                    self.playSound('Lose.wav')
                            else:
                                self.playSound('Ding.wav')
                            break
            elif len(self.hand)>=3:
                win = self.score(self.opponentHand) <= self.score(self.hand)
                if self.t > 2:
                    if win:
                        self.fighting.state = "Defeated"
                        self.player.souls += self.fighting.souls
                        self.fighting.souls = 0
                    else:
                        self.fighting.state = "Victorious"
                        self.player.souls -= self.fighting.souls
                        self.fighting.souls *= 2
                    self.fighting = False
                    if self.level == -1:
                        self.level += 1
                        self.t = 0
                    else:
                        self.playMusic("SoulSearch.wav")
                    self.text = ""
                    if self.player.souls >= 10:
                        self.level += 1
            for i, c in enumerate(self.hand):
                c.update(dt, i+1)
            for i, c in enumerate(self.opponentHand):
                c.update(dt, i+1, True)
            for i, line in enumerate(self.text):
                self.caption = self.font.render(line, True, (0,0,0))
                self.screen.blit(self.caption, (W/2-100 - self.caption.get_width()//2, 20+i*50))


    def load(self, level):
        self.sprites = []
        self.map = [([None] * (len(levels[level])))[:] for x in range(len(levels[level][0]))]
        for y, line in enumerate(levels[level]):
            for x, c in enumerate(line):
                pos = (x*50, y*50)
                if c == ' ':
                    self.map[x][y] = Sprite(self, pos, img="grass.png")
                elif c == '-':
                    self.map[x][y] = Sprite(self, pos, img="river.png", nimg=4)
                elif c == '!':
                    self.map[x][y] = Sprite(self, pos, img="river.png", nimg=4, angle=270)
                elif c == '|':
                    self.map[x][y] = Sprite(self, pos, img="river.png", nimg=4, angle=90)
                elif c == '/':
                    self.map[x][y] = Sprite(self, pos, img="river.png", nimg=4, angle=180)
                elif c == '*':
                    self.map[x][y] = Sprite(self, pos, img="grass.png")
                    self.player = Player(self, pos)
                    self.sprites += [self.player]
                else:
                    self.map[x][y] = Sprite(self, pos, img="Human"+c+".png", offset=(0,-10))
                    self.sprites += [Sprite(self, pos, img="grass.png")]
                self.sprites += [self.map[x][y]]
        self.sprites.sort(key=lambda x:x.layer)

    def getTile(self, x, y):
        if x < 0 or y < 0 or x//50 >= len(self.map) or y//50 >= len(self.map[0]):
            return False
        return self.map[x//50][y//50]

    def keyPressed(self, key):
        klist = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]
        if not self.player:
            return
        if self.fighting:
            if self.level == -1:
                self.instructions += 1
            if key == pygame.K_LEFT:
                self.key = (self.key-1)%4
            if key == pygame.K_RIGHT:
                self.key = (self.key+1)%4
            if key == pygame.K_1:
                self.key = 0
            if key == pygame.K_2:
                self.key = 1
            if key == pygame.K_3:
                self.key = 2
            if key == pygame.K_4:
                self.key = 3
        elif self.level > 1:
            r = None
            if key == pygame.K_DOWN:
                r = self.player.translate(0,50)
            elif key == pygame.K_UP:
                r = self.player.translate(0,-50)
            elif key == pygame.K_RIGHT:
                r = self.player.translate(50,0)
            elif key == pygame.K_LEFT:
                r = self.player.translate(-50,0)
            if r:
                self.fighting = r
                self.hand = []
                self.cards = []
                self.t = 0
                self.key = 0
                self.opponentHand = self.getOpponentHand(r.name[5:6])
                if self.fighting.state != "Defeated":
                    self.update(1)
                    print("A")
                    self.playMusic("RiskyBusiness2.wav",1,fade=500)

    def loadCards(self):
        score = self.score(self.opponentHand)
        while 1:
            deck = self.deck[:]
            for card in self.opponentHand:
                if card in deck:
                    deck.remove((card.suit, card.number))
            random.shuffle(deck)
            for j in range(3):
                for i in range(4):
                    card = deck[0]
                    self.addCard(i, card[0], card[1], delay=j)
                    deck.remove(card)
            n = 0
            for i in self.cards[:4]:
                for j in self.cards[4:8]:
                    for k in self.cards[8:12]:
                        if (self.score([i,j,k]) > score) != (score==100014):
                            n += 1
                            print([i,j,k])
            if n >= 1:
                return
            self.cards = []

    def addCard(self, column, suit, number, delay=0):
        Card(self, column, suit, number)
        self.cards.append(Card(self, column, suit, number, delay))

    def fight(self, opponent):
        self.fighting = True

    def loadImage(self, name, number=1):
        ''' Loads an image or list of images '''
        if not hasattr(self, "images"):
            self.images = {}
        elif name in self.images:
            return self.images[name]
        if EXE:
            path = os.path.join(os.path.dirname(sys.executable), 'images')
        else:
            path = os.path.join(os.path.dirname(__file__), 'images')
        if number==1:
            img = pygame.image.load(os.path.join(path, name))
        else:
            img = []
            for i in range(number):
                key = name[:-4]+str(i)+name[-4:]
                img.append(pygame.image.load(os.path.join(path, key)))
        self.images[name] = img
        return img

    def playSound(self, name):
        ''' Plays the given sound effect ''' 
        if EXE:
            path = os.path.join(os.path.dirname(sys.executable), 'audio')
        else:
            path = os.path.join(os.path.dirname(__file__), 'audio')
        sound = pygame.mixer.Sound(os.path.join(path, name))
        sound.play()

    def playMusic(self, name, n=-1, fade = 0):
        ''' Plays the given background track '''
        if EXE:
            path = os.path.join(os.path.dirname(sys.executable), 'audio')
        else:
            path = os.path.join(os.path.dirname(__file__), 'audio')
        if fade:
            pygame.mixer.music.fadeout(fade)
        else:
            pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(path, name))
        pygame.mixer.music.play(n)
        
    def getOpponentHand(self, difficulty):
        if difficulty == 'A':
            return (Card(self, 0, 2, 11),Card(self, 0, 2, 5),Card(self, 0, 2, 2))
        elif difficulty == 'B':
            return (Card(self, 0, 1, 5),Card(self, 0, 3, 5),Card(self, 0, 0, 5))
        elif difficulty == 'C':
            return (Card(self, 0, 1, 11),Card(self, 0, 2, 12),Card(self, 0, 3, 13))
        elif difficulty == 'D':
            return (Card(self, 0, 1, 2),Card(self, 0, 1, 3),Card(self, 0, 1, 4))
        elif difficulty == 'E':
            return (Card(self, 0, 3, 12),Card(self, 0, 2, 12),Card(self, 0, 0, 12))
        elif difficulty == '!':
            return (Card(self, 0, 1, 12),Card(self, 0, 1, 13),Card(self, 0, 1, 1))

    def score(self, hand):
        score = 1
        vals = [hand[0].number,hand[1].number,hand[2].number]
        for i, v in enumerate(vals):
            if v == 1:
                vals[i] = 14
        vals.sort()
        if vals[0] == vals[1] and vals[1] == vals[2]:
            score = 10000*score + vals[0]
        if hand[0].suit == hand[1].suit and hand[1].suit == hand[2].suit:
            score *= 100
        if vals[2]-vals[1] == vals[1]-vals[0] and abs(vals[1]-vals[0]) == 1:
            score = score * 1000 + max(vals)
            return score
        for i, v in enumerate(vals):
            if v == 14:
                vals[i] = 1
        vals.sort()
        if vals[2]-vals[1] == vals[1]-vals[0] and abs(vals[1]-vals[0]) == 1:
            score = score * 1000 + max(vals)
        return score

        


if __name__ == "__main__":
    g = Game()