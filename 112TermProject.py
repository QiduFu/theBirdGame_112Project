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
    inventory = []
    def __init__(self):
        #self.flagBirdWings()
        self.birdCounter = 0
        self.maxInventory = 6 #pollen inventory can hold up to 6 colors
    
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

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.cursorX = x 
        self.cursorY = y 
        self.playerSteps = 0
        self.playerStepsPerSecond = 4
        self.birds = self.flagBirdWings()
    
    def drawPlayer(self, app):
        drawCircle(self.x, self.y, 30, fill='cyan')
        # birdImage = self.birds[self.birdCounter]
        # drawImage(birdImage, self.x, self.y, align='center')

    def playerOnStep(self):
        self.makeMovement() #move locations to the cursors
        #self.birdCounter = (1 + self.birdCounter) % len(self.birds)
       
    def makeMovement(self):
        #get the movement distance between the cursor and current locations
        moveDistanceX = self.cursorX - self.x
        moveDisctanceY = self.cursorY - self.y
        #update the locations
        self.x += moveDistanceX / 8
        self.y += moveDisctanceY / 8

    def getTarget(self):
        pass

    def getHeldColors(self):
        pass

    def gather(self, other):
        pass

    def drawInventory(self, app):
        for i in range(len(Player.inventory)):
            color = Player.inventory[i]
            drawCircle(10+i*15, 10, 10, fill=color)


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
        self.radius = 20
        self.x = random.randint(self.radius, app.width - self.radius)
        self.y = app.height - self.radius
        # True pollinator else pollinated
        self.isPollinator = isPollinator 
        self.color = random.choice(['green', 'pink', 'yellow'])
        self.isGathered = False
        self.toBePollinated = False

    def drawFlower(self, app):
        if self.isPollinator:    
            #solid color for pollinator
            drawCircle(self.x, self.y, self.radius, fill=self.color)
            if self.isGathered:
                drawCircle(self.x, self.y, self.radius, fill = 'white',
                            border=self.color, borderWidth=4)
        else:
            # hollow circle for pollinated
            drawCircle(self.x, self.y, self.radius, fill='white',
                           border=self.color, borderWidth=4)
            if self.toBePollinated: 
                drawCircle(self.x, self.y, self.radius, fill=self.color)

    def flowerOnStep(self):
        movingSpeed = 5
        self.y -= movingSpeed

    def inView(self):
        pass

    def gather(self, app):
        #checked if player interacts with the flower
        withinRange = Flower.distance(self.x, self.y, 
                        app.player.cursorX, app.player.cursorY) <= self.radius 
        if withinRange:
            inventory = app.player.inventory
            max = app.player.maxInventory
            if (len(inventory) <= max) and (self.isPollinator):
                self.isGathered = True #not self.isGathered
                if self.radius <= 30: #set the max radius of the flowers to 30
                    self.radius += 1 
            if ((len(inventory) >= 0) and (self.color in inventory) and 
                (not self.isPollinator)): 
                self.toBePollinated = True 
                if self.radius <= 30:
                    self.radius += 1 
                inventory.remove(self.color)

    def redraw(self, x=None, y=None):
        pass

    @staticmethod
    def distance(x0, y0, x1, y1):
        return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # APP---------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

def onAppStart(app):
    reset(app)

def reset(app):
    app.player = Player(400, 400)
    app.flowers = []
    app.flowerPerSecond = 4
    app.flowerSteps = 0

def onKeyPress(app, key):
    if key == 'r':
        reset(app)

def onMouseMove(app, x, y):
    app.player.cursorX = x
    app.player.cursorY = y

def onStep(app):
    app.player.playerOnStep()
    app.flowerSteps += 1
    removeFlowers(app)
    generateFlowers(app)
    for flower in app.flowers:
        flower.flowerOnStep()
        inventory = app.player.inventory
        max = app.player.maxInventory
        if ((flower.isGathered) and (flower.isPollinator) and 
            (len(inventory) <= max)):
            inventory.append(flower.color)
        flower.gather(app)
        
def removeFlowers(app):
    i = 0
    while i < len(app.flowers):
        flower = app.flowers[i]
        if flower.y < - flower.radius:
            app.flowers.pop(i)
        else:
            i += 1

def generateFlowers(app):
    #generate 4 flowers per second with a total of 30 flowers on the screen
    if (app.flowerSteps % app.flowerPerSecond == 0) and (len(app.flowers) < 30):
        #randomly generate pollinator or pollinated
        isPollinator = random.choice([True, False])
        app.flowers.append(Flower(isPollinator, app))

def redrawAll(app):
    drawTitle(app)
    app.player.drawPlayer(app)
    app.player.drawInventory(app)
    for flower in app.flowers:
        flower.drawFlower(app)

def drawTitle(app):
    drawLabel('A Game of Flying Birds', 700, 30, size=30)

def main():
    runApp(width=1400, height=700)

main()
