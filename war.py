import pygame
import random

from pygame import event

from pygameRogers import Game, TextRectangle, Alarm
from pygameRogers import Room
from pygameRogers import GameObject

g = Game(640, 480)
g.timer = Alarm()

Black = (0, 0, 0)
White = (255, 255, 255)

simpleBackground = g.makeBackground(Black)
gameFont = g.makeFont("Arial", 38)

r1 = Room("Game", simpleBackground)
g.addRoom(r1)
r2 = Room("War room", simpleBackground)
g.addRoom(r2)
r3 = Room("Player 1 victory room", simpleBackground)
g.addRoom(r3)
r4 = Room("Player 2 victory room", simpleBackground)
g.addRoom(r4)

#start button
class War(TextRectangle):
    def __init__(self, text, xpos, ypos, font, textcolor, buttonwidth, buttonheight, buttoncolor):
        TextRectangle.__init__(self, text, xpos, ypos, font, textcolor, buttonwidth, buttonheight, buttoncolor)
        self.timer = Alarm()

    def update(self):
        self.checkMousePressedOnMe(event)

        if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
            g.nextRoom()

            self.mouseHasPressedOnMe = False


diamondpics = []
for i in range(2, 15):
    diamondpics.append(g.makeSpriteImage("cards\DIAMONDS" + str(i) + ".jpg"))

clubpics = []
for i in range(2, 15):
    clubpics.append(g.makeSpriteImage("cards\CLUBS" + str(i) + ".jpg"))

heartpics = []
for i in range(2, 15):
    heartpics.append(g.makeSpriteImage("cards\HEARTS" + str(i) + ".jpg"))

spadepics = []
for i in range(2, 15):
    spadepics.append(g.makeSpriteImage("cards\SPADES" + str(i) + ".jpg"))

topcard = g.makeSpriteImage("cards/TOP.jpg")

#card object
class card(GameObject):
    def __init__(self, picture, value, suit):
        GameObject.__init__(self, picture)

        self.value = value
        self.suit = suit  # H, D, C, S

    def compare(self, card2):
        if self.value > card2.value:
            return self
        elif self.value < card2.value:
            return card2

    def __str__(self):
        return str(self.value) + self.suit


#deck with 52 cards
class deck(GameObject):
    def __init__(self, picture, xpos, ypos):
        GameObject.__init__(self, picture)

        self.rect.x = xpos
        self.rect.y = ypos

        self.deck = []

        for i in range(0, len(diamondpics)):
            c = card(diamondpics[i], i + 2, "D")
            self.deck.append(c)

        for i in range(0, len(clubpics)):
            c = card(clubpics[i], i + 2, "C")
            self.deck.append(c)

        for i in range(0, len(heartpics)):
            c = card(heartpics[i], i + 2, "H")
            self.deck.append(c)

        for i in range(0, len(spadepics)):
            c = card(spadepics[i], i + 2, "S")
            self.deck.append(c)

        random.shuffle(self.deck)
#function that splits the deck in 2 and distributes them
    def deal(self):
        if len(self.deck) > 0:
            c = self.deck[0]
            del self.deck[0]

        if len(self.deck) == 0:
            self.kill()

        return c

    def __str__(self):

        s = ""
        for card in self.deck:
            s = s + str(card) + " "
        return s

#player 1
class playerhand(GameObject):
    def __init__(self, picture, handsize, xpos, ypos):
        GameObject.__init__(self, picture)
        self.rect.x = xpos
        self.rect.y = ypos

        self.hand = []
        self.cardsinhand = 0

    def takecard(self, card):
        self.hand.append(card)
        self.cardsinhand = self.cardsinhand + 1
        if len(self.hand) == 0:
            g.nextRoom()
            g.nextRoom()

    def playcard(self):
        d = self.hand[0]
        del self.hand[0]
        self.cardsinhand = self.cardsinhand - 1

        return d

    def __str__(self):
        s = ""
        for card in self.hand:
            s = s + str(card) + " "
            # s = "playerhand:/n" + s + "/n"
        return s

#player 2
class playerhand2(GameObject):
    def __init__(self, picture, handsize, xpos, ypos):
        GameObject.__init__(self, picture)
        self.rect.x = xpos
        self.rect.y = ypos

        self.hand = []
        self.cardsinhand = 0

    def takecard(self, card):
        self.hand.append(card)
        self.cardsinhand = self.cardsinhand + 1
        self.cardsinhand = self.cardsinhand + 1
        if len(self.hand) == 0:
            g.nextRoom()

    def playcard(self):
        e = self.hand[0]
        del self.hand[0]
        self.cardsinhand = self.cardsinhand - 1

        return e

    def __str__(self):
        s = ""
        for card in self.hand:
            s = s + str(card) + " "
            # s = "playerhand:/n" + s + "/n"
        return s

#one time use splits the deck and distributes
class DealButton(TextRectangle):

    def __init__(self, text, xPos, yPos, font, textcolor, buttonwidth, buttonheight, buttoncolor):
        TextRectangle.__init__(self, text, xPos, yPos, font, textcolor, buttonwidth, buttonheight, buttoncolor)

    def update(self):
        self.checkMousePressedOnMe(event)
        if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
            for i in range(0, 26):
                acard = deck.deal()
                p.takecard(acard)
                bcard = deck.deal()
                p2.takecard(bcard)
            self.mouseHasPressedOnMe = False
        else:
            pass

#plays 2 cards compares them starts war etc
class PlayButton(TextRectangle):

    def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
        TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)
        self.timer = Alarm()
        self.timer2 = Alarm()

    def update(self):
        self.checkMousePressedOnMe(event)
        if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
            #card 1 image properties
            self.ccard = p.playcard()
            self.ccard.rect.x = 250
            self.ccard.rect.y = 125
            r2.addObject(self.ccard)
            #card 2 image properties
            self.dcard = p2.playcard()
            self.dcard.rect.x = 250
            self.dcard.rect.y = 250
            r2.addObject(self.dcard)
            #player 1 wins
            if self.ccard.value > self.dcard.value:
                p.takecard(self.ccard)
                p.takecard(self.dcard)
            #player 2 wins
            elif self.dcard.value > self.ccard.value:
                p2.takecard(self.ccard)
                p2.takecard(self.dcard)
                #War
            elif self.dcard.value == self.ccard.value:
                if len(p.hand) < 4 and len(deck.deck) == 0:
                    g.nextRoom()
                    g.nextRoom()
                if len(p2.hand) < 4 and len(deck.deck) == 0:
                    g.nextRoom()
                self.ecard = p.playcard()
                self.ecard.rect.x = 50
                self.ecard.rect.y = 125
                r2.addObject(self.ecard)
                self.fcard = p.playcard()
                self.fcard.rect.x = 100
                self.fcard.rect.y = 125
                r2.addObject(self.fcard)
                self.gcard = p.playcard()
                self.gcard.rect.x = 150
                self.gcard.rect.y = 125
                r2.addObject(self.gcard)
                self.hcard = p2.playcard()
                self.hcard.rect.x = 50
                self.hcard.rect.y = 250
                r2.addObject(self.hcard)
                self.icard = p2.playcard()
                self.icard.rect.x = 100
                self.icard.rect.y = 250
                r2.addObject(self.icard)
                self.jcard = p2.playcard()
                self.jcard.rect.x = 150
                self.jcard.rect.y = 250
                r2.addObject(self.jcard)
                self.kcard = p.playcard()
                self.kcard.rect.x = 200
                self.kcard.rect.y = 25
                r2.addObject(self.kcard)
                self.lcard = p2.playcard()
                self.lcard.rect.x = 200
                self.lcard.rect.y = 350
                r2.addObject(self.lcard)
                if self.kcard.value > self.lcard.value:
                    p.takecard(self.ccard)
                    p.takecard(self.dcard)
                    p.takecard(self.ecard)
                    p.takecard(self.fcard)
                    p.takecard(self.gcard)
                    p.takecard(self.hcard)
                    p.takecard(self.icard)
                    p.takecard(self.jcard)
                    p.takecard(self.kcard)
                    p.takecard(self.lcard)
                elif self.kcard.value < self.lcard.value:
                    p2.takecard(self.ccard)
                    p2.takecard(self.dcard)
                    p2.takecard(self.ecard)
                    p2.takecard(self.fcard)
                    p2.takecard(self.gcard)
                    p2.takecard(self.hcard)
                    p2.takecard(self.icard)
                    p2.takecard(self.jcard)
                    p2.takecard(self.kcard)
                    p2.takecard(self.lcard)
                elif self.kcard.value == self.lcard.value:
                    p.takecard(self.ccard)
                    p.takecard(self.dcard)
                    p.takecard(self.ecard)
                    p.takecard(self.fcard)
                    p.takecard(self.gcard)
                    p.takecard(self.hcard)
                    p.takecard(self.icard)
                    p.takecard(self.jcard)
                    p.takecard(self.kcard)
                    p.takecard(self.lcard)
                #how long war cards stay on screen for
                a = 4000
                self.timer2.setAlarm(a)
            #how long regular cards stay on screen for
            t = 1000
            self.timer.setAlarm(t)
            print(p)
            print(p2)
            self.mouseHasPressedOnMe = False
        if self.timer.finished():
            self.ccard.kill()
            self.dcard.kill()
        if self.timer2.finished():
            print("Hi")
            self.ecard.kill()
            self.fcard.kill()
            self.gcard.kill()
            self.hcard.kill()
            self.icard.kill()
            self.jcard.kill()
            self.kcard.kill()
            self.lcard.kill()
        if len(p2.hand) == 0 and len(deck.deck) == 0:
            g.nextRoom()
        if len(p.hand) == 0 and len(deck.deck) == 0:
            g.nextRoom()
            g.nextRoom()

class textbox(TextRectangle):

    def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
        TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

Warbutton = War("Start", 250, g.windowHeight - 250, gameFont, Black, 150, 40, White)
r1.addObject(Warbutton)

deck = deck(topcard, 287, 203)
r2.addObject(deck)

p = playerhand(topcard, 52, 400, 30)
r2.addObject(p)

p2 = playerhand2(topcard, 52, 400, 300)
r2.addObject(p2)

dealbutton = DealButton("Deal", 400, g.windowHeight - 250, gameFont, Black, 150, 40, White)
r2.addObject(dealbutton)

playbutton = PlayButton("Play", 400, g.windowHeight - 300, gameFont, Black, 150, 40, White)
r2.addObject(playbutton)

winbutton1 = textbox("P1 Wins", 400, g.windowHeight - 250, gameFont, Black, 150, 40, White)
r3.addObject(winbutton1)

winbutton2 = textbox("P2 Wins", 400, g.windowHeight - 250, gameFont, Black, 150, 40, White)
r4.addObject(winbutton2)

print(deck)

g.start()
while g.running:
    dt = g.clock.tick(60)
    for event in pygame.event.get():

        # Check for [x]
        if event.type == pygame.QUIT:
            g.stop()

    # Update All objects in Room
    g.currentRoom().updateObjects()

    # Render Background to the game surface
    g.currentRoom().renderBackground(g)

    # Render Objects to the game surface
    g.currentRoom().renderObjects(g)

    # Draw everything on the screen
    pygame.display.flip()

pygame.quit()
