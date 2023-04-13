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

class Bird(object):
    
    def __init__(self):
        self.inventory = []
        self.birdCounter = 0
        self.inventoryCapacity = 6 #pollen inventory can hold up to 6 colors
        self.birds = []

        # initiate the resized bird's image width and height
        self.birdWidth, self.birdHeight = None, None 

        # load the bird picture
                # The bird picture is from 
                # https://www.pngitem.com/middle/
                # ihbJiib_transparent-bird-bird-sprite-sheet-png-png-download/
        url = 'birdPic.png'
        birdImage = Image.open(url)
        birdImageNum = 3 
        for i in range(birdImageNum):
            bird = birdImage.crop((320*i, 0, 320*(i + 1), 1232))
            imageWidth, imageHeight = bird.width, bird.height
            self.birdWidth, self.birdHeight = (imageWidth // 3, imageHeight // 3)
            self.birds.append(CMUImage(bird))
        self.birdCounter = 0
        self.stepCounter = 0

    def getTarget(self):
        pass

    def getHeldColors(self):
        pass

    def gatherAndPollinated(self, other):
        pass

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # The BIRD (Player bird)----------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Player(Bird):

    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.cursorX, self.cursorY= x, y
        self.birdFeetX, self.birdFeetY = x, y
        self.dotX, self.dotY = None, None
        self.playerSteps = 0
        self.playerStepsPerSecond = 4

    def drawPlayer(self, app):
        bird = self.birds[self.birdCounter]
        drawImage(bird, self.birdFeetX, self.birdFeetY, align='center', 
                  width=self.birdWidth, height=self.birdHeight)
        # if the inventory not empty draw the carrying dot to the bird's feet
        if (self.dotX != None) and len(self.inventory) > 0:
            latestColor = self.inventory[-1]
            drawCircle(self.dotX, self.dotY, 10, fill=latestColor)

    def playerOnStep(self):
        self.makeMovement() #move locations towards the cursors
        self.stepCounter += 1
        if self.stepCounter >= 5: #update the sprite every 5 steps
            #This line is from 112's course note
            self.birdCounter = (1 + self.birdCounter) % len(self.birds)
            self.stepCounter = min(0, self.stepCounter)
       
    def makeMovement(self):
        #get the movement distances between the cursor and current locations
        moveDistanceX = self.cursorX - self.x
        moveDisctanceY = self.cursorY - self.y

        #update the locations with 1/8 of the current distances
        self.x += moveDistanceX / 8
        self.y += moveDisctanceY / 8

        #make up the different between the bird's feet and cursor locations
        self.birdFeetX = self.x - 3
        self.birdFeetY = self.y + 135

        #update the  coordinates of the dot on birds' feet
        self.dotX = self.x
        self.dotY = self.y

    def getTarget(self):
        pass

    def getHeldColors(self):
        pass

    def gatherAndPollinated(self, other):
        pass

    def drawInventory(self, app):
        for i in range(len(self.inventory)):
            color = self.inventory[i]
            drawCircle(20+i*25, 20, 20, fill=color)


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

    def __init__(self, isPollinator, app):
        # initiate flower radius to be 20
        self.radius = 20
        self.x = random.randint(self.radius, app.width - self.radius)
        self.y = app.height - self.radius

        # True pollinator else pollinated
        self.isPollinator = isPollinator 

        # initia the times that a flower can be gathered
        self.gatheredTimes = 2
        #initia the time that a flower can be pollinated
        self.pollinatedTimes = 1

        #initia flower colors
        self.color = random.choice(['cyan', 'pink', 'yellow'])
        
        #indicator for flowers ready to be pollinated
        self.toBePollinated = False
        #check if a flower is gathered
        self.isGathered = False

        #initia dx offset, I think 8 is the best for my game
        self.dx = math.sin(8 * self.y) 

    
    def flowerOnStep(self, app):
        movingSpeed = 5
        self.y -= movingSpeed

        # update position through the offset
        if (self.x > self.radius) and (self.x < app.height):
            self.x -= self.dx        

    def drawFlower(self, app):
        if self.isPollinator:    
            self.drawPollinator(app)
        else:
            self.drawPollinated(app)

    def drawPollinator(self, app):
            #solid circles for pollinator when it has not been gathered
            if self.gatheredTimes == 2:
                drawCircle(self.x, self.y, self.radius, fill=self.color)

            # gathered the first time
            if self.gatheredTimes == 1:
                drawCircle(self.x, self.y, self.radius, fill='white',
                        border=self.color, borderWidth=4)
                drawCircle(self.x, self.y, 10, fill=self.color)
            
            # # second gathered pollnation
            if self.gatheredTimes == 0:
                drawCircle(self.x, self.y, self.radius, fill='white',
                                border=self.color, borderWidth=4)
    
    def drawPollinated(self, app):
            # hollow circles for being pollinated
            drawCircle(self.x, self.y, self.radius, fill='white',
                           border=self.color, borderWidth=4)
            if self.toBePollinated: 
                drawCircle(self.x, self.y, self.radius, fill=self.color)

    def gatherAndPollinated(self, app):
        #checked if the dot on bird's feet interacts with the flower
        isInteracted = Flower.distance(self.x, self.y, 
                        app.player.dotX, app.player.dotY) <= self.radius 
        
        #set the max radius of the flowers to 30
        maxFlowerRadius = 30  
        if isInteracted:
            self.gather(app, maxFlowerRadius)
            self.pollinated(app, maxFlowerRadius)

    def gather(self, app, maxFlowerRadius):
        # gather the flowers/pollination from pollinators
        if ((self.isPollinator) and 
            (self.gatheredTimes > 0) and 
            (app.flowerSteps % 5 == 0)):

            self.gatheredTimes -= 1
            self.isGathered = True
            
            #increment of the radius when gathered and radius <= 30
            if self.radius <= maxFlowerRadius: 
                self.radius += 5 

    def pollinated(self, app, maxFlowerRadius):
        inventory = app.player.inventory
        #pollinate when the inventory has the correct colors
        if ((len(inventory) >= 0) and (self.color in inventory) and 
            (not self.isPollinator) and (self.pollinatedTimes == 1)): 
            self.toBePollinated = True 
            self.pollinatedTimes -= 1

            #increment of the radius
            if self.radius <= maxFlowerRadius:
                self.radius += 5

            #update the inventory
            inventory.remove(self.color)

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

    #remove flowers when they are outside the canvas
    removeFlowers(app)
    #generate flowers periodically
    generateFlowers(app)
    # update inventory every step
    updateInventory(app)

def updateInventory(app):
    inventory = app.player.inventory
    maxCapacity = app.player.inventoryCapacity 
    for flower in app.flowers:
        flower.flowerOnStep(app)
        if ((flower.isGathered) and (flower.isPollinator)):
            if len(inventory) == maxCapacity:
                # remove the oldest from inventory before adding
                inventory.pop(0) 
            inventory.append(flower.color)
            flower.isGathered = False
        flower.gatherAndPollinated(app)
        
def removeFlowers(app):
    i = 0
    while i < len(app.flowers):
        flower = app.flowers[i]
        #remove the flower moving outside of the cavas
        if flower.y < (-flower.radius):
            app.flowers.pop(i)
        else:
            i += 1

def generateFlowers(app):
    #generate 4 flowers per second with a total of 30 flowers on the screen
    totalFlowerNumber = 30
    if ((app.flowerSteps % app.flowerPerSecond == 0) and 
        (len(app.flowers) <= totalFlowerNumber)):
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
    drawLabel('A Game of Flying Birds', app.width // 2, 30, size=30)

def main():
    runApp(width=1400, height=700)

main()
