import pygame
import random
import time
from settings import *
from sprites import *
from spriteScaling import *

pygame.init()

winWidth = 1200
winHeight = 900

win = pygame.display.set_mode([winWidth, winHeight])
pygame.display.set_caption('Chicken Farmer')

white_color = (255, 255, 255)


dead = False


clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.walkCount = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.lastDir = sprite_R0
        self.walkRight = [sprite_R0, sprite_R1, sprite_R2]
        self.walkLeft = [sprite_L0, sprite_L1, sprite_L2]
        self.walkUp = [sprite_U0, sprite_U1, sprite_U2]
        self.walkDown = [sprite_D0, sprite_D1, sprite_D2]
        self.lastDir = sprite_R0
        self.hitbox = self.x, self.y, width, height
        self.collideable = True

    def draw(self, win):
        if self.walkCount + 1 >= 9:
            self.walkCount = 0
        if man.left:
            win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            self.lastDir = self.walkLeft[0]
        elif man.right:
            win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            self.lastDir = self.walkRight[0]
        elif man.up:
            win.blit(self.walkUp[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            self.lastDir = self.walkUp[0]
        elif man.down:
            win.blit(self.walkDown[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            self.lastDir = self.walkDown[0]
        else:
            win.blit(self.lastDir, (self.x,self.y))

        #self.hitbox = self.x, self.y, self.width, self.height #hitbox moves with player
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #hitbox

class chicken:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.vel = 0.08
        self.walkCount = 0
        self.lastDir = chkn_R1
        self.walkRight = [chkn_R1, chkn_R2, chkn_R3, chkn_R4, chkn_R5, chkn_R6]
        self.walkLeft = [chkn_L1, chkn_L2, chkn_L3, chkn_L4, chkn_L5, chkn_L6]
        self.walkUp = [chkn_U1, chkn_U2, chkn_U3, chkn_U4, chkn_U5, chkn_U6, chkn_U7]
        self.walkDown = [chkn_D1, chkn_D2, chkn_D3, chkn_D4, chkn_D5, chkn_D6, chkn_D7]
        self.hitbox = self.x, self.y, self.width, self.height
        self.isInside = False
        self.readyX = False
        self.readyY = False

    def drawChknCont(self):
        if self.walkCount > 4:
            self.walkCount == 0
        else:
            if self.left:
                win.blit(self.walkLeft[int(self.walkCount//3)], (self.x ,self.y))
                self.walkCount += self.vel
                self.lastDir = self.walkLeft[0]
            elif self.right:
                win.blit(self.walkRight[int(self.walkCount//3)], (self.x,self.y))
                self.walkCount += self.vel
                self.lastDir = self.walkRight[0]
            elif self.up:
                win.blit(self.walkUp[int(self.walkCount//3)], (self.x,self.y))
                self.walkCount += self.vel
                self.lastDir = self.walkUp[0]
            elif self.down:
                win.blit(self.walkDown[int(self.walkCount//3)], (self.x,self.y))
                self.walkCount += self.vel
                self.lastDir = self.walkDown[0]
            else:
                win.blit(self.lastDir, (self.x,self.y))
            #self.hitbox = self.x, self.y, self.width, self.height #hitbox moves with player
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #hitbox for chicken

    def goInside(self):   
        def convergeOnY(c):
            for c in chickenList:
                if c.readyY == False:
                    if 459 <= int(c.y) <= 461:
                        c.readyY = True
                        c.up = True
                    elif c.y < 460:
                        c.y += c.vel
                        c.down = True
                    elif c.y > 460:
                        c.y -= c.vel
                        c.up = True

        def convergeOnX(c):
            for c in chickenList:
                if c.readyX == False:
                    if 829 <= int(c.x) <= 831:
                        c.readyX = True
                        c.up = True
                    elif c.x < 830:
                        c.x += c.vel
                        c.right = True
                    elif c.x > 830:
                        c.x -= c.vel
                        c.left = True

            for c in chickenList:
                if c.readyX and c.readyY:
                    if c.y > 200:
                        c.x = 830
                        c.y -= c.vel
                        c.up = True
                    elif 199 <= int(c.y) <= 201:
                        c.isInside = True
                        
        if bellClass.checkIfNear(bell, man):
            for c in chickenList:
                if coop.opened:
                    convergeOnY(c)
                    convergeOnX(c)
                    chicken.drawChknCont(c)
                    
    
    def goOutside(self):
        self.readyX = False
        self.readyY = False
        self.isInside = False
        self.x = 830
        self.y = 200

    def drawChkn(self, win):
        if self.isInside == False:
            self.walkCount = 0
            steps = random.randint(1, 3)
            directionInt = random.randint(0, 151) #chicken has 4/152 chance of moving in a direction
            pixels = random.randint(5, 20)

            self.collideable = True
            self.left = False
            self.right = False
            self.up = False
            self.down = False

            oldX = self.x
            oldY = self.y

            if directionInt == 0 and self.x < winWidth - self.width - (self.vel + self.width):
                self.x += pixels
                self.right = True
            elif directionInt == 1 and self.x  > (self.vel + self.width):
                self.x -= pixels
                self.left = True
            elif directionInt == 2 and self.y > (self.vel + self.width):
                self.y -= pixels
                self.up = True
            elif directionInt == 3 and self.y < winHeight - self.height - (self.vel + self.width):
                self.y += pixels
                self.down = True
            else:
                pass

            newX = self.x
            newY = self.y

            for gameObject in gameObjList:  #collision check for chicken
                for c in chickenList:
                    if gameObj.checkCollision(gameObject, c):
                        c.x = oldX
                        c.y = oldY
                    else:
                        pass
                    next
                next
    
        chicken.drawChknCont(self)


class gameObj(object):
    def __init__(self, sprite, x, y, height, width):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.height = height
        self.width = width
        self.hitbox = self.x, self.y, self.width, self.height
        self.collideable = True
        self.interactable = False

    def checkCollision(self, collideableObj): #collideableObj such as chicken, player
        if collideableObj.x > self.x - collideableObj.width and \
            collideableObj.x < self.x + self.width and \
            collideableObj.y > self.y - collideableObj.height and \
            collideableObj.y < self.y + self.height:
            return True
        else:
            return False

    def drawObj(self, win):
        #self.hitbox = self.x, self.y, self.width, self.height
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #hitbox for obj

        win.blit((self.sprite), (self.x, self.y))

class coop(gameObj):
    def __init__(self, sprite, x, y, height, width, opened, step):
        self.opened = opened
        self.step = step
        self.x = x
        self.y = y
        self.sprite = sprite
        self.height = height
        self.width = width
        self.hitbox = self.x, self.y, self.width, self.height
        self.collideable = True
        self.interactable = True
        self.opening = False
        self.closing = True

    def checkIfNear(self, collideableObj):
        if collideableObj.x > self.x - collideableObj.width // 2 and \
            collideableObj.x < self.x + self.width // 2 and \
            collideableObj.y > self.y - collideableObj.height and \
            collideableObj.y < self.y + 5 + self.height:
            return True
        else:
            return False

    def open(self):
        if self.checkIfNear(man):
            coop.opened = True
            coop.sprite = coop_o
            time.sleep(0.25)
            for c in chickenList:
                if c.isInside:
                    c.goOutside()

    def close(self):
        if self.checkIfNear(man):
            coop.opened = False
            coop.sprite = coop_c
            time.sleep(0.25)
            for c in chickenList:
                c.goInside()
            
class bellClass(coop):
    def __init__(self, sprite, x, y, height, width):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.collideable = True

    def checkIfNear(self, collideableObj):
        if collideableObj.x > self.x - collideableObj.width and \
            collideableObj.x < self.x + self.width and \
            collideableObj.y > self.y - collideableObj.height and \
            collideableObj.y < self.y + 10 + self.height:
            return True
        else:
            return False

class marketClass(gameObj):
    def __init__(self, sprite, x, y, height, width):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.collideable = True

    def checkIfNear(self, collideableObj):
        if collideableObj.x > self.x - collideableObj.width and \
            collideableObj.x < self.x + self.width and \
            collideableObj.y > self.y - collideableObj.height and \
            collideableObj.y < self.y + 10 + self.height:
            return True
        else:
            return False

def sortByY(allObj):
    allObj.sort(key=lambda x: x.y + x.height, reverse=False)
    return allObj

def text_objects(text, font):
    textSurface = font.render(text, True, 'black')
    return textSurface, textSurface.get_rect()

def message_display(text, x, y):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    win.blit(TextSurf, TextRect)

def gui():
    message_display('cash: ', 1050, 50)
    message_display(' day: ', 1050, 70)
     
man = player(1000, 50, 40, 40)

gameObjList = []
rock = gameObj(rockSprite, 1000, 750, 100, 150)
gameObjList.append(rock)
rock2 = gameObj(rockSprite, 400, 50, 100, 150)
gameObjList.append(rock2)

coop = coop(coop_o, 750, 50, 150, 200, True, 0)
gameObjList.append(coop)

bell = bellClass(bellSprite, 950, 125, 30, 50)
gameObjList.append(bell)

market = marketClass(marketSprite, 50, 0, 50, 75)
gameObjList.append(market)

chickenList = []
c1 = chicken(100,100)
chickenList.append(c1)
c2 = chicken(200,200)
chickenList.append(c2)
c3 = chicken(300,300)
chickenList.append(c3)
c4 = chicken(400,400)
chickenList.append(c4)
c5 = chicken(500,500)
chickenList.append(c5)
c6 = chicken(600,100)
chickenList.append(c6)
c7 = chicken(700,200)
chickenList.append(c7)
c8 = chicken(800,300)
chickenList.append(c8)
c9 = chicken(900,400)
chickenList.append(c9)
c10 = chicken(952,500)
chickenList.append(c10)
c11 = chicken(100,100)
chickenList.append(c11)
c12 = chicken(200,200)
chickenList.append(c12)
c13 = chicken(300,300)
chickenList.append(c13)
c14 = chicken(400,400)
chickenList.append(c14)
c15 = chicken(500,500)
chickenList.append(c15)

def redrawGameWindow():
    win.blit((bg), (0, 0))
    allObj = []
    for obj in gameObjList:
        allObj.append(obj)
    for chkn in chickenList:
        if chkn.isInside == False:
            allObj.append(chkn)
    allObj.append(man)

    objInOrder = sortByY(allObj)

    for x in objInOrder:
        if isinstance(x, chicken):
            x.drawChkn(win)
        if isinstance(x, gameObj):
            x.drawObj(win)
        if isinstance(x, player):
            x.draw(win)

    gui()

    pygame.display.update()

def allowMove(prevX, prevY, nextX, nextY):
    for gameObject in gameObjList:                  #if collision, reset x, y to previous x, y on "man"
        if gameObj.checkCollision(gameObject, man):
            man.x = prevX
            man.y = prevY
        else:
            pass
        next      
    
#mainloop

while not dead:

    clock.tick(60) #FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
    keys = pygame.key.get_pressed()
    pygame.key.set_repeat(10000, 10000)

    prevX = man.x
    prevY = man.y

    if keys[pygame.K_a] and keys[pygame.K_w] and \
        man.x  > (man.vel + man.width) \
        and man.y > (man.vel + man.width):
        man.x -= man.vel
        man.y -= man.vel
        man.right = False
        man.left = True
        man.up = False
        man.down = False
    elif keys[pygame.K_w] and \
        keys[pygame.K_d] and \
        man.y > (man.vel + man.width) and \
        man.x < winWidth - man.width - (man.vel + man.width):
        man.x += man.vel
        man.y -= man.vel
        man.right = True
        man.left = False
        man.up = False
        man.down = False
    elif keys[pygame.K_a] and \
        keys[pygame.K_s] and man.x  > (man.vel + man.width) \
        and man.y < winHeight - man.height - (man.vel + man.width):
        man.x -= man.vel
        man.y += man.vel
        man.right = False
        man.left = True
        man.up = False
        man.down = False
    elif keys[pygame.K_s] and \
        keys[pygame.K_d] and \
        man.y < winHeight - man.height - (man.vel + man.width) and \
        man.x < winWidth - man.width - (man.vel + man.width):
        man.x += man.vel
        man.y += man.vel
        man.right = True
        man.left = False
        man.up = False
        man.down = False      
    elif keys[pygame.K_a] and man.x  > (man.vel + man.width) :
        man.x -= man.vel
        man.right = False
        man.left = True
        man.up = False
        man.down = False
    elif keys[pygame.K_d] and \
        man.x < winWidth - man.width - (man.vel + man.width):
        man.x += man.vel
        man.right = True
        man.left = False
        man.up = False
        man.down = False
    elif keys[pygame.K_w] and man.y > (man.vel + man.width):
        man.y -= man.vel
        man.up = True
        man.down = False
        man.right = False
        man.left = False
    elif keys[pygame.K_s] and \
        man.y < winHeight - man.height - (man.vel + man.width):
        man.y += man.vel
        man.up = False
        man.down = True
        man.right = False
        man.left = False

    elif keys[pygame.K_e]:
        if coop.opened:
            coop.close()
        elif coop.opened == False:
            coop.open()
        for c in chickenList:
            if c.isInside == False:
                chicken.goInside(c)

    elif keys[pygame.K_q]:
        if coop.opened == False:
            coop.open()

    else:
        man.up = False
        man.down = False
        man.right = False
        man.left = False
        man.walkCount = 0

    nextX = man.x
    nextY = man.y

    allowMove(prevX, prevY, nextX, nextY)
    
    redrawGameWindow()
    
pygame.quit()
