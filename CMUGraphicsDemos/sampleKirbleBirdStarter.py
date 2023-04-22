#----------------------------------------
# KirbleBird starter demo v.1.1
#    4/11/2023
#    Ping me at mdtaylor@andrew.cmu.edu
#    Kirb gif from https://kirby.fandom.com/f/p/4400000000000066147
#----------------------------------------

from cmu_graphics import *
from PIL import Image
import random, time

class Kirb:
    def __init__(self):
        #Load the kirb gif
        myGif = Image.open('kirb.gif')
        self.spriteList = []
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
            fr = fr.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            self.spriteList.append(fr)

        ##Fix for broken transparency on frame 0
        self.spriteList.pop(0)

        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0

        #Set initial position, velocity, acceleration
        self.x, self.y = 100, 100
        self.dy = 0
        self.ddy = .1

    def draw(self):
        #Draw current kirb sprite
        drawImage(self.spriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        
    def doStep(self):
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

        #Update position and velocity
        self.y += self.dy
        self.dy += self.ddy

        #Don't let your pal down
        if self.y >= 550:
            self.y = 550
            self.dy = 0

    def flap(self):
        self.dy = -3

#-------------------------------------------------------------------
class Orb:
    def __init__(self, app):
        self.x = app.width + 20
        self.y = random.randrange(app.height)
        self.dx = -random.randrange(2, 5)
        self.r = random.randrange(30, 100)

    def doStep(self):
        self.x += self.dx

    def draw(self):
        drawCircle(self.x, self.y, self.r, fill = 'white', opacity = 75)

#-------------------------------------------------------------------
def onAppStart(app):
    app.stepsPerSecond = 50         #Adjust the onStep frequency
    app.kirb = Kirb()               #Make a kirb
    app.orbs = []                   #Make an empty orb list
    app.lastOrbTime = time.time()   #Set an initial orb timer
    
def onStep(app):
    #Update the kirb
    app.kirb.doStep()

    #Update the orbs
    for orb in app.orbs:
        orb.doStep()

    #Add another orb each second
    #Note: This will slow down over time as the orb list gets long! 
    #Can you figure out how to remove orbs that have left the screen?
    if (time.time() - app.lastOrbTime > 1):
        app.orbs.append(Orb(app))
        app.lastOrbTime = time.time()

def onKeyPress(app, key):
    #Flappy kirb!
    app.kirb.flap()

def redrawAll(app):
    #Background
    drawRect(0, 0, app.width, app.height, fill='lightskyblue')

    #Call kirb's draw method
    app.kirb.draw()

    #Call each orb's draw method
    for orb in app.orbs:
        orb.draw()
    
#Change width and height to suit your needs    
runApp(width=600, height=600)