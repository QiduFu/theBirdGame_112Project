#title: A Game of Flying Birds
#date: 04/03/2023
#spring23 15112 term project
#name: Qidu Fu
#andrewId: qiduf
#email: qiduf@andrew.cmu.edu
# --------------------------------------------------------------------------

# inspired by the Google's Earth Day Doodle 
# and Mike's (15112 instuctor) scaffolded project
# https://www.google.com/doodles/earth-day-2020

from cmu_graphics import *
import random
import math, time
from PIL import Image



# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# The BIRD (main)-----------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Bird:
    def __init__(self):
        #self.flagBirdWings()
        self.birdCounter = 0
    
    def flagBirdWings(self):
        # The bird picture is from 
        # https://www.pngitem.com/middle/
        # ihbJiib_transparent-bird-bird-sprite-sheet-png-png-download/
        url = 'birdPic.png'
        picWidth, picHeight = getImageSize(url)
        birdImage = Image.open(url)
        print(f"{picWidth, picHeight = }")
        birdImageNum = 3 
        birds = []
        for i in range(birdImageNum):
            bird = birdImage.crop((308*i, 0, 308*(i + 1), 1232))
            birds.append(CMUImage(bird))
            #print(getImageSize(CMUImage(bird)))
        self.birdCounter = 0
        return birds

    def onStep(self):
        pass

    def getTarget(self):
        pass

    def getHeldColors(self):
        pass

    def gather(self, other):
        pass

    def redraw(self, app):
        pass

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # The BIRD (Player bird)----------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Player(Bird):
    def __init__(self, locX, locY):
        super().__init__()
        self.locX = locX
        self.locY = locY
        self.cursorX = locX 
        self.cursorY = locY 
        self.playerSteps = 0
        self.playerStepsPerSecond = 4
        self.birds = self.flagBirdWings()
        self.pollens = []
    
    def drawPlayer(self, app):
        drawCircle(self.locX, self.locY, 30, fill='cyan')
        # birdImage = self.birds[self.birdCounter]
        # drawImage(birdImage, self.locX, self.locY, align='center')

    def playerOnStep(self):
        self.makeMovement() #move locations to the cursors
        self.birdCounter = (1 + self.birdCounter) % len(self.birds)
       
    def makeMovement(self):
        #get the movement distance between the cursor and current locations
        moveDistanceX = self.cursorX - self.locX
        moveDisctanceY = self.cursorY - self.locY
        #update the locations
        self.locX += moveDistanceX / 8
        self.locY += moveDisctanceY / 8

    def getTarget(self):
        pass

    def getHeldColors(self):
        pass

    def gather(self, other):
        pass

    def redraw(self, canvas):
        pass


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # The BIRD (Helper BIRDS)-------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Helper(Bird):
    def __init__(self, app):
        pass
    
    def onAppstep(self, x,):
        pass

    def redrawll(self, canvas):
        super().redraw(canvas)
        pass

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # FLOWER------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Flower(object):

    # @staticmethod
    # def update():
    #     pass

    def __init__(self, isPollinator, app):
        self.radius = 10
        self.x = random.randint(self.radius, app.width - self.radius)
        self.y = app.height - self.radius
        # True pollinator else pollinated
        self.isPollinator = isPollinator 
        self.color = {'isPollinator': 'purple', 'pollinated': 'pink'}
    
    def __repr__(self):
        return f"{self.isPollinator}"

    def drawFlower(self, app):
        if self.isPollinator:
            drawCircle(self.x, self.y, self.radius, fill='white',
                           border='red', borderWidth=4)
        else:
            drawCircle(self.x, self.y, self.radius, fill='purple')
                #    fill=self.color['isPollinator'] 
                #    if self.isPollinator else self.color['pollinated'])

    def flowerOnStep(self):
        self.y -= 8

    def inView(self):
        pass

    def gather(self, got):
        pass

    def redraw(self, x=None, y=None):
        pass



# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # APP---------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

def onAppStart(app):
    app.player1 = Player(400, 400)
    flower1 = Flower(True, app)
    flower2 = Flower(False, app)
    app.flowers = [flower1, flower2]
    app.flowerPerSecond = 4
    app.flowerSteps = 0

def onMouseMove(app, x, y):
    app.player1.cursorX = x
    app.player1.cursorY = y

def onStep(app):
    app.player1.playerOnStep()
    app.flowerSteps += 1
    removeFlowers(app)
    generateFlowers(app)
    for flower in app.flowers:
        flower.flowerOnStep()
    
def removeFlowers(app):
    i = 0
    while i < len(app.flowers):
        flower = app.flowers[i]
        if flower.y < - flower.radius:
            app.flowers.pop(i)
        else:
            i += 1

def generateFlowers(app):
    if (app.flowerSteps % app.flowerPerSecond == 0) and (len(app.flowers) < 15):
        isPollinator = random.choice([True, False])
        app.flowers.append(Flower(isPollinator, app))

def redrawAll(app):
    drawTitle(app)
    app.player1.drawPlayer(app)
    for flower in app.flowers:
        flower.drawFlower(app)

def drawTitle(app):
    drawLabel('A Game of Flying Birds', 700, 30, size=30)

def main():
    runApp(width=1400, height=700)

main()
