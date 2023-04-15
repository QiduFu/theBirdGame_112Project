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
            bird = birdImage.crop((320*i, 0, 320*(i+1), 1232))
            imageWidth, imageHeight = bird.width, bird.height
            self.birdWidth, self.birdHeight = (imageWidth//3, imageHeight//3)
            self.birds.append(CMUImage(bird))
        self.birdCounter = 0
        self.stepCounter = 0

    def getTarget(self):
        pass

    def getHeldColors(self):
        pass

    def gatherAndPollinated(self, other):
        pass

# # --------------------------------------------------------------------------
# # --------------------------------------------------------------------------
# # # The BIRD (Player bird)----------------------------------------------------
# # --------------------------------------------------------------------------
# # --------------------------------------------------------------------------

# class Player(Bird):

#     def __init__(self, x, y):
#         super().__init__()
#         self.x, self.y = x, y
#         self.cursorX, self.cursorY= x, y
#         self.birdFeetX, self.birdFeetY = x, y
#         self.dotX, self.dotY = None, None
#         self.playerSteps = 0
#         self.playerStepsPerSecond = 4
#         self.target = None

#     def drawPlayer(self, app):
#         self.drawBird(app)
#         #draw the dots carried by the bird's feet
#         self.drawDot(app)
    
#     def drawBird(self, app):
#         bird = self.birds[self.birdCounter]
#         drawImage(bird, self.birdFeetX, self.birdFeetY, align='center', 
#                   width=self.birdWidth, height=self.birdHeight)

#     def drawDot(self, app):
#         # if the inventory not empty draw the carrying dot to the bird's feet
#         if (self.dotX != None) and len(self.inventory) > 0:
#             # latestColor = self.inventory[-1]
#             # drawCircle(self.dotX, self.dotY, 10, fill=latestColor)
#             increment = 0
#             colorsDrawn = set()
#             for color in self.inventory:
#                 #only draw  the dot with color which has not been drawn
#                 if color not in colorsDrawn:
#                     drawCircle(self.dotX + increment, self.dotY, 10, fill=color)
#                     increment += 5
#                     colorsDrawn.add(color)

#     def playerOnStep(self, app):
#         self.moveToCursor() #move locations towards the cursors
#         self.moveToTarget(app) #helper birds move towards the taget
#         self.stepCounter += 1
#         print(self.target)
#         if self.stepCounter >= 5: #update the sprite every 5 steps
#             #This line is from 112's course note
#             self.birdCounter = (1 + self.birdCounter) % len(self.birds)
#             self.stepCounter = min(0, self.stepCounter)

#     def moveToTarget(self, app):
#         if self.target != None:
#             print('entering not none')
#             if self.isLegalTarget():
#                 self.makeTargetMove()
#             else:
#                 self.target = None
#         if self.target == None:
#             print('---gettarget')
#             self.getTarget(app)

#     def makeTargetMove(self):
#         targetX, targetY = self.target.x, self.target.y
        
#         #get the movement distances between the target and current locations
#         distanceX = targetX - self.x
#         distanceY = targetY - self.y

#         #update the birds' locations with 1/8 of the current distances
#         self.x += distanceX / 8
#         self.y += distanceY / 8

#         # #make up the different between the bird's feet and cursor locations
#         # self.birdFeetX = self.x - 2
#         # self.birdFeetY = self.y + 135

#         #update the  coordinates of the dot on birds' feet
#         self.dotX = self.x
#         self.dotY = self.y
    
#     def isLegalTarget(self):
#         return (((self.target.gatheredTimes != 0) or # can be gathered 
#                 (self.target.pollinatedTimes != 0)) and # not pollinated
#                 (self.target.y <= -self.target.radius)) # on canvas

#     def getTarget(self, app):
#         shortestDist = None
#         for flower in app.flowers:
#             if (flower.gatheredTimes != 0) or (flower.pollinatedTimes != 0):
#                 print('gathered adn pollianated')
#                 if (self.dotX != None) and (self.dotY != None):
#                     print('target====', self.dotX, self.dotY, flower.x, flower.y)
#                     currentDist = flower.distance(self.dotX, self.dotY, 
#                                               flower.x, flower.y)
#                     if (shortestDist == None) or (shortestDist > currentDist):
#                         shortestDist = currentDist
#                         self.target = flower

#     def moveToCursor(self):
#         #get the movement distances between the cursor and current locations
#         distanceX = self.cursorX - self.x
#         distanceY = self.cursorY - self.y

#         #update the birds' locations with 1/8 of the current distances
#         self.x += distanceX / 8
#         self.y += distanceY / 8

#         #make up the different between the bird's feet and cursor locations
#         self.birdFeetX = self.x - 2
#         self.birdFeetY = self.y + 135

#         #update the  coordinates of the dot on birds' feet
#         self.dotX = self.x
#         self.dotY = self.y

#     def drawInventory(self, app):
#         for i in range(len(self.inventory)):
#             color = self.inventory[i]
#             drawCircle(20+i*25, 20, 20, fill=color)
#             #label the inventory colors with numbers starting from 1
#             drawLabel(f'{i+1}', 20+i*25, 20)


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
        self.drawBird(app)
        #draw the dots carried by the bird's feet
        self.drawDot(app)
    
    def drawBird(self, app):
        bird = self.birds[self.birdCounter]
        drawImage(bird, self.birdFeetX, self.birdFeetY, align='center', 
                  width=self.birdWidth, height=self.birdHeight)

    def drawDot(self, app):
        # if the inventory not empty draw the carrying dot to the bird's feet
        if (self.dotX != None) and len(self.inventory) > 0:
            latestColor = self.inventory[-1]
            drawCircle(self.dotX, self.dotY, 10, fill=latestColor)
            increment = 0 # increment of X when drawing the dot on bird's feet
            colorsDrawn = set()
            for color in self.inventory:
                #only draw  the dot with color which has not been drawn
                if color not in colorsDrawn:
                    drawCircle(self.dotX + increment, self.dotY, 10, fill=color)
                    increment += 5
                    colorsDrawn.add(color)


    def playerOnStep(self):
        self.moveToCursor() #move locations towards the cursors
        self.stepCounter += 1
        if self.stepCounter >= 5: #update the sprite every 5 steps
            #This line is from 112's course note
            self.birdCounter = (1 + self.birdCounter) % len(self.birds)
            self.stepCounter = min(0, self.stepCounter)


    def moveToCursor(self):
        #get the movement distances between the cursor and current locations
        distanceX = self.cursorX - self.x
        distanceY = self.cursorY - self.y

        #update the birds' locations with 1/6 of the current distances
        self.x += distanceX / 6
        self.y += distanceY / 6

        #make up the different between the bird's feet and cursor locations
        self.birdFeetX = self.x - 2
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
            #label the inventory colors with numbers starting from 1
            drawLabel(f'{i+1}', 20+i*25, 20)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # The BIRD (Helper BIRDS)-------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Helper(Player):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.x, self.y = x, y
        self.cursorX, self.cursorY= x, y
        self.birdFeetX, self.birdFeetY = x, y
        self.dotX, self.dotY = None, None
        self.playerSteps = 0
        self.playerStepsPerSecond = 4
        self.target = None

    def drawPlayer(self, app):
        self.drawBird(app)
        #draw the dots carried by the bird's feet
        self.drawDot(app)
    
    def drawBird(self, app):
        bird = self.birds[self.birdCounter]
        drawImage(bird, self.birdFeetX, self.birdFeetY, align='center', 
                  width=self.birdWidth, height=self.birdHeight)

    def drawDot(self, app):
        # if the inventory not empty draw the carrying dot to the bird's feet
        if (self.dotX != None) and len(self.inventory) > 0:
            # latestColor = self.inventory[-1]
            # drawCircle(self.dotX, self.dotY, 10, fill=latestColor)
            increment = 0
            colorsDrawn = set()
            for color in self.inventory:
                #only draw  the dot with color which has not been drawn
                if color not in colorsDrawn:
                    drawCircle(self.dotX + increment, self.dotY, 10, fill=color)
                    increment += 5
                    colorsDrawn.add(color)

    def helperOnStep(self, app):
        self.moveToCursor() #move locations towards the cursors
        self.moveToTarget(app) #helper birds move towards the taget
        self.stepCounter += 1
        print(self.target)
        if self.stepCounter >= 5: #update the sprite every 5 steps
            #This line is from 112's course note
            self.birdCounter = (1 + self.birdCounter) % len(self.birds)
            self.stepCounter = min(0, self.stepCounter)

    def moveToTarget(self, app):
        if self.target != None:
            print('entering not none')
            #check legality of the target
            if self.isLegalTarget():
                self.makeTargetMove()
            else:
                self.target = None
        if self.target == None:
            print('---gettarget')
            self.getTarget(app)

    def makeTargetMove(self):
        targetX, targetY = self.target.x, self.target.y
        
        #get the movement distances between the target and current locations
        distanceX = targetX - self.x
        distanceY = targetY - self.y

        #update the birds' locations with 1/8 of the current distances
        self.x += distanceX / 8
        self.y += distanceY / 8

        # #make up the different between the bird's feet and cursor locations
        # self.birdFeetX = self.x - 2
        # self.birdFeetY = self.y + 135

        #update the  coordinates of the dot on birds' feet
        self.dotX = self.x
        self.dotY = self.y
    
    def isLegalTarget(self):
        return (((self.target.gatheredTimes != 0) or # can be gathered 
                (self.target.pollinatedTimes != 0)) and # not pollinated
                (self.target.y <= -self.target.radius)) # on canvas

    def getTarget(self, app):
        shortestDist = None
        for flower in app.flowers:
            if (flower.gatheredTimes != 0) or (flower.pollinatedTimes != 0):
                print('gathered adn pollianated')
                if (self.dotX != None) and (self.dotY != None):
                    print('target====', self.dotX, self.dotY, flower.x, flower.y)
                    currentDist = flower.distance(self.dotX, self.dotY, 
                                              flower.x, flower.y)
                    if (shortestDist == None) or (shortestDist > currentDist):
                        shortestDist = currentDist
                        self.target = flower

    def moveToCursor(self):
        #get the movement distances between the cursor and current locations
        distanceX = self.cursorX - self.x
        distanceY = self.cursorY - self.y

        #update the birds' locations with 1/8 of the current distances
        self.x += distanceX / 8
        self.y += distanceY / 8

        #make up the different between the bird's feet and cursor locations
        self.birdFeetX = self.x - 2
        self.birdFeetY = self.y + 135

        #update the  coordinates of the dot on birds' feet
        self.dotX = self.x
        self.dotY = self.y

    def drawInventory(self, app):
        for i in range(len(self.inventory)):
            color = self.inventory[i]
            drawCircle(20+i*25, 20, 20, fill=color)
            #label the inventory colors with numbers starting from 1
            drawLabel(f'{i+1}', 20+i*25, 20)

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
        self.y = app.height + self.radius

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
        #check if a flower is growing
        self.isGrowing = False

        #initia dx offset, I think 8 is the best for my game
        self.dx = math.sin(8 * self.y) 

    
    def flowerOnStep(self, app):
        movingSpeed = 5
        self.y -= movingSpeed

        #set the max radius of the flowers to 30
        maxFlowerRadius = 30  
        if (self.isGrowing == True) and (self.radius <= maxFlowerRadius):
            self.radius += 2 # radius grows by 2 per call

        # update position through the offset
        if (self.x > self.radius) and (self.x < app.height):
            self.x -= self.dx        

    def drawFlower(self, app):
        if self.isPollinator:    
            self.drawPollinator(app)
        else:
            self.drawPollinated(app)

    def drawPollinator(self, app):
            #solid circles for pollinator when they have not been gathered
            if self.gatheredTimes == 2:
                drawCircle(self.x, self.y, self.radius, fill=self.color)

            # gathered the first time: ringed circles
            if self.gatheredTimes == 1:
                drawCircle(self.x, self.y, self.radius, fill='lightGreen',
                        border=self.color, borderWidth=4)
                drawCircle(self.x, self.y, 10, fill=self.color)
            
            # # second gathered pollnation: hollow circles
            if self.gatheredTimes == 0:
                drawCircle(self.x, self.y, self.radius, fill='lightGreen',
                                border=self.color, borderWidth=4)
    
    def drawPollinated(self, app):
            # hollow circles for being pollinated
            drawCircle(self.x, self.y, self.radius, fill='lightGreen',
                           border=self.color, borderWidth=4)
            if self.toBePollinated: 
                drawCircle(self.x, self.y, self.radius, fill=self.color)

    def gatherAndPollinated(self, app):
        #checked if the dot on bird's feet interacts with the flower
        isInteracted = False
        if (app.player.dotX != None) and (app.player.dotY != None):
            isInteracted = Flower.distance(self.x, self.y, 
                            app.player.dotX, app.player.dotY) <= self.radius 
        
        if isInteracted:
            self.gather(app)
            self.pollinated(app)

    def gather(self, app):
        # gather the flowers/pollination from pollinators
        if ((self.isPollinator) and 
            (self.gatheredTimes > 0) and 
            #each gather takes 1 sec. Fully gathering takes 2s per flower.
            (app.stepCounter % app.flowerPerSecond == 0)): 

            self.gatheredTimes -= 1
            self.isGathered = True
            
            #flowers grows when it is gathered
            self.isGrowing = True

    def pollinated(self, app):
        inventory = app.player.inventory
        #pollinate when the inventory has the correct colors
        if ((len(inventory) >= 0) and (self.color in inventory) and 
            (not self.isPollinator) and (self.pollinatedTimes == 1)): 
            self.toBePollinated = True 
            self.pollinatedTimes -= 1

            # when pollinated, flowers grow
            self.isGrowing = True

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
    app.background = 'lightGreen'
    app.player = Player(400, 400)
    app.flowers = []
    app.flowerPerSecond = 4
    app.stepCounter = 0
    app.paused = False
    app.textPerSecond = 4
    app.textSize = 30 #initiate the size instruciton text   
    app.helper1 = None
    app.helper2 = None

def onKeyPress(app, key):
    if key == 'r':
        reset(app)
    elif key == 'p':
        app.paused = not app.paused
    elif key == 'h':
        app.helper1 = Helper(500, 500)
        app.helper2 = Helper(600, 600)

def onMouseMove(app, x, y):
    app.player.cursorX = x
    app.player.cursorY = y

def onStep(app):
    if app.paused == False:
        takeStep(app)

def takeStep(app):
    app.player.playerOnStep()
    #update helper birds' calls if the birds exist
    if app.helper1 != None:
        app.helper1.helperOnStep(app)
        app.helper2.helperOnStep(app)
        
    # update the text size per call
    updateInstuctionTextSize(app)
    #remove flowers when they are outside the canvas
    removeFlowers(app)
    #generate flowers periodically
    generateFlowers(app)
    # update inventory every step
    updateInventory(app)
    app.stepCounter += 1

def updateInstuctionTextSize(app):
    #reset the instruction text size when it is below 0
    if app.textSize < 0:
        app.textSize = 30
    else:
        #text size decreases 0.2 per call
        app.textSize -= .2

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
    index = 0
    while index < len(app.flowers):
        flower = app.flowers[index]
        #remove the flower moving outside of the cavas
        if flower.y < (-flower.radius):
            app.flowers.pop(index)
        else:
            index += 1

def generateFlowers(app):
    #generate 4 flowers per second with a total of 30 flowers on the screen
    totalFlowerNumber = 30
    if ((app.stepCounter % app.flowerPerSecond == 0) and 
        (len(app.flowers) <= totalFlowerNumber)):
        #randomly generate pollinator or pollinated
        isPollinator = random.choice([True, False])
        app.flowers.append(Flower(isPollinator, app))

def redrawAll(app):
    drawTitle(app)
    drawInstructionText(app)
    app.player.drawPlayer(app)
    app.player.drawInventory(app)   

    #draw helpers when they are called
    if app.helper1 != None: 
        app.helper1.drawPlayer(app)
        app.helper2.drawPlayer(app)

    #draw flowers
    for flower in app.flowers:
        flower.drawFlower(app)

def drawInstructionText(app):
    # print(app.stepCounter)
    counter = app.stepCounter % 5000
    if app.paused == True:
        drawUnpause(app)
    elif 0 < counter < 50:
        drawGoodLuck(app)
    elif 200 < counter < 250:
        drawEnjoy(app)
    elif 400 < counter < 450:
        drawPause(app)
    elif 600 < counter < 650:
        drawGetHelperText(app)
    elif 800 < counter < 850:
        drawReset(app)

def drawReset(app):
    drawLabel('Press r to restart the game!', app.width//2, app.height//2, 
            size=app.textSize if app.textSize > 0 else 0)

def drawGetHelperText(app):
    drawLabel('Press h to get helper birds', app.width//2, app.height//2, 
                size=app.textSize if app.textSize > 0 else 0)    

def drawUnpause(app):
    drawLabel('Press p to unpause the game', app.width//2, app.height//2, 
                   size=30)

def drawEnjoy(app):
    drawLabel('Enjoy the game!', app.width//2, app.height//2, 
                size=app.textSize if app.textSize > 0 else 0)

def drawGoodLuck(app):
    drawLabel('Good luck with playing', app.width//2, app.height//2, 
                size=app.textSize if app.textSize > 0 else 0)

def drawPause(app):
    drawLabel('Press p to pause the game', app.width//2, app.height//2, 
                size=app.textSize if app.textSize > 0 else 0)

def drawTitle(app):
    drawLabel('A Game of Flying Birds', app.width // 2, 30, size=30)

def main():
    runApp(width=1400, height=700)

main()
