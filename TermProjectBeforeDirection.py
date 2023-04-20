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
import math
from PIL import Image

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# The BIRD (main)-----------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Bird(object):
    
    def __init__(self, app):
    # def __init__(self):
        self.inventory = []
        self.birdCounter = 0
        self.stepCounter = 0
        self.birds = []
        # initiate the resized bird's image width and height
        self.birdWidth, self.birdHeight = None, None 
        self.loadBirdImage(app)

        # # load the bird picture
        #         # The bird picture is from 
        #         # URL: https://www.pngitem.com/middle/
        #         # ihbJiib_transparent-bird-bird-sprite-sheet-png-png-download/
        # url = 'birdPic.png'
        # birdImage = Image.open(url)
        # birdImageNum = 3 
        # #crop the bird picture and store the sprite bird pic into the birds list
        # #the next 5 lines are adaptations of 15112's course note: 
        #     #URL: http://www.cs.cmu.edu/~112-f22/notes
        #     #/notes-animations-part4.html#spritesheetsWithCropping
        # for index in range(birdImageNum):
        #     bird = birdImage.crop((320*index, 0, 320*(index+1), 1232))
        #     imageWidth, imageHeight = bird.width, bird.height
        #     self.birdWidth, self.birdHeight = (imageWidth//3, imageHeight//3)
        #     self.birds.append(CMUImage(bird))

    def loadBirdImage(self, app):
        # load the bird picture
            # The bird picture is from 
            # URL: https://www.pngitem.com/middle/
            # ihbJiib_transparent-bird-bird-sprite-sheet-png-png-download/
        url = 'birdPic.png'
        birdImage = Image.open(url)
        birdImageNum = 3 

        #crop the bird picture and store the sprite bird pic into the birds list
        #the next 2 lines are adaptations of 15112's course note: 
            # URL: http://www.cs.cmu.edu/~112-f22/notes
            # /notes-animations-part4.html#spritesheetsWithCropping
        for index in range(birdImageNum):
            bird = birdImage.crop((320*index, 0, 320*(index+1), 1232))
            # if self.birdDirection < 0:
            #         bird = bird.transpose(Image.FLIP_LEFT_RIGHT)
            imageWidth, imageHeight = bird.width, bird.height
            #the next 2 lines are adaptations of 15112's course note: 
                # URL: http://www.cs.cmu.edu/~112-f22/notes
                # /notes-animations-part4.html#spritesheetsWithCropping
            self.birdWidth, self.birdHeight = (imageWidth//3, imageHeight//3)
            self.birds.append(CMUImage(bird))
        
    

# # --------------------------------------------------------------------------
# # --------------------------------------------------------------------------
# # # The BIRD (Player bird)----------------------------------------------------
# # --------------------------------------------------------------------------
# # --------------------------------------------------------------------------

class Player(Bird):

    def __init__(self, x, y, app):
        super().__init__(app)

    # def __init__(self, x, y):
        # super().__init__()
        self.x, self.y = x, y
        
        #initiate cursor position to be the same as the bird position
        self.cursorX, self.cursorY= x, y

        #initiate the positions for birds' feet
        self.birdFeetX, self.birdFeetY = x, y
        #initiate the positions for the dots' on bird feet, which are different
        #from the birds' feet due to the image issues
        self.dotX, self.dotY = x, y

        #indicate if the bird's heading direction is changed or not
        self.changingDirection = False

        self.playerSteps = 0
        self.playerStepsPerSecond = 4

    def birdOnStep(self, app):
        #move locations towards the cursors
        self.moveToCursor() 
        #gather/pollinate flowers
        self.gatherAndPollinateFlower(app)
        #update the inventory per step
        self.updateInventory(app)

        self.stepCounter += 1
        #The next 2 lines are adaptation of 112's course note
        # URL: http://www.cs.cmu.edu/~112-f22/notes
        # /notes-animations-part4.html#spritesheetsWithCropping
        if self.stepCounter >= 5: #update the sprite every 5 steps
            self.birdCounter = (1 + self.birdCounter) % len(self.birds)
            self.stepCounter = min(0, self.stepCounter)

    def moveToCursor(self):
        #get the movement distances between the cursor and current locations
        distanceX = self.cursorX - self.x
        distanceY = self.cursorY - self.y

        #update the birds' locations with 1/5 of the current distances
        updatingRatio =  1/5
        self.x += distanceX * updatingRatio
        self.y += distanceY * updatingRatio

        #make up the misplacement between the bird's feet and cursor locations
        self.birdFeetX = self.x - 2
        self.birdFeetY = self.y + 135

        #update the  coordinates of the dot on birds' feet
        self.dotX = self.x
        self.dotY = self.y

    def gatherAndPollinateFlower(self, app):
        for flower in app.flowers:
            #checked if the dots interact with the flower
            isInteracted = Player.distance(self.dotX, self.dotY, 
                                        flower.x, flower.y) <= flower.radius

            if isInteracted == True:
                self.gatherFlowers(app, flower)
                self.pollinateFlowers(flower)

    def gatherFlowers(self, app, flower):
        # gather the flowers/pollination from pollinators
        if ((flower.isPollinator) and 
            (flower.gatheredTimes > 0) and 
            #each gather takes 1 sec. Full gathering takes 2s per flower.
            (app.stepCounter % app.flowerPerSecond == 0)): 
            flower.gatheredTimes -= 1
            flower.isGathered = True
            
            #flowers grows when it is gathered
            flower.growing = True

    def pollinateFlowers(self, flower):
        inventory = self.inventory
        #pollinate when the inventory has the correct colors
        if ((len(inventory) >= 0) and (flower.color in inventory) and 
            (not flower.isPollinator) and (flower.pollinatedTimes == 1)): 
            flower.isPollinated = True 
            flower.pollinatedTimes -= 1

            # when pollinated, flowers grow
            flower.growing = True

            # when pollinated, update the inventory
            inventory.remove(flower.color)

    def updateInventory(self, app):
        for flower in app.flowers:
            if ((flower.isPollinator) and (flower.isGathered)):
                inventory = self.inventory
                # pollen inventory hold up to 6 flowers
                inventoryCapacity = 6
                if len(inventory) >= inventoryCapacity:
                    # remove the oldest from inventory before adding
                    inventory.pop(0) 
                inventory.append(flower.color)
                flower.isGathered = False

    def redrawBirdAll(self, app):
        self.drawBird(app)
        self.drawInventory(app)
        #draw the dots carried by the bird's feet
        self.drawDot(app)
    
    def drawBird(self, app):
        bird = self.birds[self.birdCounter]
        # due to the image issues, the bird is drawn the its feet
        drawImage(bird, self.birdFeetX, self.birdFeetY, align='center', 
                  width=self.birdWidth, height=self.birdHeight)

    def drawDot(self, app):
        # if the inventory not empty draw the carrying dot to the bird's feet
        if len(self.inventory) > 0:
            increment = 0 # increment of X when drawing the dot on bird's feet
            colorsDrawn = set()
            for color in self.inventory:
                #only draw  the dot with color which has not been drawn
                if color not in colorsDrawn:
                    drawCircle(self.dotX + increment, self.dotY, 10, fill=color)
                    increment += 5
                    colorsDrawn.add(color)

    def drawInventory(self, app):
        for i in range(len(self.inventory)):
            color = self.inventory[i]
            drawCircle(20+i*25, 20, 20, fill=color)
            # #label the inventory colors with numbers starting from 1
            # drawLabel(f'{i+1}', 20+i*25, 20)
    
    @staticmethod
    def distance(x0, y0, x1, y1):
        return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # The BIRD (Helper BIRDS)-------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Helper(Player):

    def __init__(self, x, y, app):
        super().__init__(x, y, app)
    # def __init__(self, x, y):
        # super().__init__(x, y)
        self.target = None

    def birdOnStep(self, app):
        #helper birds move towards the taget
        self.getTargetAndMakeMove(app) 
        #gather/pollinate flowers
        self.gatherAndPollinateFlower(app)
        #update the inventory per step
        self.updateInventory(app)

        self.stepCounter += 1
        if self.stepCounter >= 5: #update the sprite every 5 steps
            #This line is from 112's course note
            self.birdCounter = (1 + self.birdCounter) % len(self.birds)
            self.stepCounter = min(0, self.stepCounter)

    def getTargetAndMakeMove(self, app):
        if self.target != None:
            #check legality of the target
            if self.isLegalTarget():
                self.makeTargetMove(app)                
            else:
                self.target = None
        if self.target == None:
            self.getTarget(app)

    def makeTargetMove(self, app):
        targetX, targetY = self.target.x, self.target.y
        canvasMidLine = app.width // 2
        
        #get the movement distances between the target and current locations
        distanceX = targetX - self.x
        distanceY = targetY - self.y

        #update the birds' locations with 1/8 of the current distances
        updatingRatio =  1/8
        self.newX = distanceX * updatingRatio + self.x
        self.newY = distanceY * updatingRatio + self.y

        #make sure the bird on the right side of canvas stays on the right 
        if self.x > canvasMidLine:
            if self.newX > canvasMidLine:
                self.x = self.newX
        #make sure the bird on the left side  stays on the left
        else:
            if self.newX <= canvasMidLine:
                self.x = self.newX
        self.y = self.newY

        #make up the different between the bird's feet and cursor locations
        self.birdFeetX = self.x - 2
        self.birdFeetY = self.y + 105

        #update the  coordinates of the dots on birds' feet and 
        #make up the differences between the cursors and the dots
        self.dotX = self.x + 2
        self.dotY = self.y - 30

    
    def isLegalTarget(self):
        result = ((self.target.growing == False) and # ungathred/unpollinated
                  (self.target.y > 0)) # on canvas
        return result

    def getTarget(self, app):
        shortestDist = None
        for flower in app.flowers:
            if flower.isPollinator:
                self.getTargetFlower(flower, shortestDist, app)
            else:
                # if it is pollinated, make the inventory has the correct color
                # before make it into our target
                if flower.color in self.inventory:
                    self.getTargetFlower(flower, shortestDist, app)

    def getTargetFlower(self, flower, shortestDist, app):
        canvasMidLine = app.width // 2
        #make sure the bird of the right side of the canvas only look for 
        #flowers on the right
        if (self.x > canvasMidLine) and (flower.x > canvasMidLine):
            self.getClosestFlower(flower, shortestDist)

        #make sure the bird of the right side of the canvas only look for 
        #flowers on the right
        elif (self.x <= canvasMidLine) and (flower.x <= canvasMidLine):
            self.getClosestFlower(flower, shortestDist)
    
    def getClosestFlower(self, flower, shortestDist):
        #not fully gathered or unpollinated flowers
        if (flower.gatheredTimes != 0) or (flower.pollinatedTimes != 0):
            currentDist = Player.distance(self.dotX, self.dotY, 
                                          flower.x, flower.y)
            if (shortestDist == None) or (shortestDist > currentDist):
                shortestDist = currentDist
                self.target = flower

    def redrawBirdAll(self, app):
        self.drawBird(app) # draw the flying bird
        self.drawInventory(app) # draw the inventory 
        self.drawDot(app) # draw the dot on the bird feet

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # FLOWER------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Flower(object):

    def __init__(self, isPollinator, app):
        self.radius = 20 # initiate flower radius to be 20
        self.x = random.randint(self.radius, app.width - self.radius)
        self.y = app.height + self.radius

        # True pollinator else pollinated
        self.isPollinator = isPollinator 

        # initia the times that a flower can be gathered
        self.gatheredTimes = 2
        #initia the time that a flower can be pollinated
        self.pollinatedTimes = 1

        #initiate flower colors
        self.color = random.choice(['cyan', 'pink', 'yellow', 'red'])
        
        #indicator for flowers are pollinated
        self.isPollinated = False
        #check if a flower is gathered
        self.isGathered = False
        #check if a flower is growing
        self.growing = False

        #initia dx/dy/ddx offset, I think 6 for dx is the best for my game
        self.dx = math.sin(6 * self.y) 
        self.dy = 5
        self.ddx = 0.02
    
    def flowerOnStep(self, app):
        # update position through the offset
        self.updateFlowerLocation(app)

        #update radius per call when it is growing
        if (self.growing == True):
            self.updateFlowerRadius()
    
    def updateFlowerRadius(self):
        #set the max radius of the flowers to 30
        maxRadius = 30
        #set the medium raidus to 25
        midRadius = 25
        #radius grows by 2 per call
        growingSpeed = 2
        if self.gatheredTimes == 1:
            #when the pollinator is not fulled gathered
            self.radius = min(self.radius + growingSpeed, midRadius)
        else:
            # if its pollinated/fullly gathered
            self.radius = min(self.radius + growingSpeed, maxRadius)

    def updateFlowerLocation(self, app):
        self.y -= self.dy #update y
        if (self.x > self.radius) and (self.x < app.height):
            self.x -= self.dx #update x
            self.dx += self.ddx
    
    def redrawFlower(self, app):
        self.drawFlower(app)

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
                drawCircle(self.x, self.y, self.radius, fill=app.background,
                        border=self.color, borderWidth=4)
                drawCircle(self.x, self.y, 10, fill=self.color)
            
            # second gathered pollination: hollow circles
            if self.gatheredTimes == 0:
                drawCircle(self.x, self.y, self.radius, fill=app.background,
                                border=self.color, borderWidth=4)
    
    def drawPollinated(self, app):
            # hollow circles for being pollinated
            drawCircle(self.x, self.y, self.radius, fill=app.background,
                           border=self.color, borderWidth=4)
            if self.isPollinated: 
                drawCircle(self.x, self.y, self.radius, fill=self.color)

    # @staticmethod
    # def removeOffCanvasFlowers(app):
    #     index = 0
    #     while index < len(app.flowers):
    #         flower = app.flowers[index]
    #         #remove the flower moving outside of the cavas
    #         if flower.y < 0:
    #             app.flowers.pop(index)
    #         else:
    #             index += 1
                
    # @staticmethod
    # def generateFlowers(app):
    #     #generate 4 flowers per second with a total of 25 flowers on the screen
    #     totalFlowerNumber = 25
    #     if ((app.stepCounter % app.flowerPerSecond == 0) and 
    #         (len(app.flowers) <= totalFlowerNumber)):
    #         #randomly generate pollinator or pollinated
    #         isPollinator = random.choice([True, False])
    #         app.flowers.append(Flower(isPollinator, app))


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # APP---------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

def onAppStart(app):
    reset(app)

def reset(app):
    app.background = 'lightGreen'
    app.player = Player(400, 400, app)
    # app.player = Player(400, 400)
    app.flowers = []
    app.flowerPerSecond = 5
    app.stepCounter = 0
    app.textSize = 30 #initiate the size instruciton text   
    app.textShrikingSpeed = 0.2
    app.paused = False
    app.helper1 = None
    app.helper2 = None

def onKeyPress(app, key):
    if key == 'r':
        reset(app)
    elif key == 'p':
        app.paused = not app.paused
    elif key == 'h':
        app.helper1 = Helper(0, 0, app)
        app.helper2 = Helper(app.width, app.height, app)

def onMouseMove(app, x, y):
    app.player.cursorX = x
    app.player.cursorY = y

def onStep(app):
    if app.paused == False:
        takeStep(app)

def takeStep(app):
    app.player.birdOnStep(app)

    #update helper birds' calls if the birds exist
    if app.helper1 != None:
        app.helper1.birdOnStep(app)
        app.helper2.birdOnStep(app)

    for flower in app.flowers:
        flower.flowerOnStep(app)
        
    #remove and generate flowers off/on vcanvas
    removeAndGenerateFlowers(app)

    #update the text size per call
    updateInstuctionTextSize(app)
    
    app.stepCounter += 1

def removeAndGenerateFlowers(app):
    #remove flowers when they are outside the canvas
    # Flower.removeOffCanvasFlowers(app)
    removeOffCanvasFlowers(app)
    #generate flowers periodically
    # Flower.generateFlowers(app)
    generateFlowers(app)

def removeOffCanvasFlowers(app):
    index = 0
    while index < len(app.flowers):
        flower = app.flowers[index]
        #remove the flower moving outside of the cavas
        if flower.y < 0:
            app.flowers.pop(index)
        else:
            index += 1
            
def generateFlowers(app):
    #generate 4 flowers per second with a total of 20 flowers on the screen
    totalFlowerNumber = 20
    if ((app.stepCounter % app.flowerPerSecond == 0) and 
        (len(app.flowers) < totalFlowerNumber)):
        #randomly generate pollinator or pollinated
        isPollinator = random.choice([True, False])
        app.flowers.append(Flower(isPollinator, app))

def updateInstuctionTextSize(app):
    #reset the instruction text size when it is <= 0
    maxTextSize = 30
    if app.textSize <= 0:
        app.textSize = maxTextSize
    else:
        #text size decreases 0.2 per call
        shrinkingSpeedPerCall = 0.2
        app.textSize -= shrinkingSpeedPerCall

def redrawAll(app):
    redrawAllInstructionText(app)
    app.player.redrawBirdAll(app)

    #draw helpers when they are called
    if app.helper1 != None: 
        app.helper1.redrawBirdAll(app)
        app.helper2.redrawBirdAll(app)

    #draw flowers
    for flower in app.flowers:
        flower.redrawFlower(app)

def redrawAllInstructionText(app):
    #draw the below instructions once every 900 calls
    counter = app.stepCounter % 900

    #while the game is paused, show instruction to unpause the game
    if app.paused == True:
        drawToContinueText(app)

    #while the game playing, to enhance user experience, 
    #show  text when the remainder/counter satifies the below periodically
    elif 0 <= counter < 150:  # textSize / shrinkingSpeed = 30/0.2 = 150
        text = 'Having fun :)'
        drawInstructionText(app, text)
    elif 150 <= counter < 300:
        text = "Move your cursor/bird's feet to gather/pollinate flowers"
        drawInstructionText(app, text)
    elif 300 <= counter < 450:
        text = 'Enjoy the game :)'
        drawInstructionText(app, text)
    elif 450 <= counter < 600:
        text = 'Press p to pause the game'
        drawInstructionText(app, text)
    elif 600 <= counter < 750:
        text = 'Press h to get helper birds'
        drawInstructionText(app, text)
    elif 750 <= counter < 900:
        text = 'Press r to restart the game'
        drawInstructionText(app, text)

def drawToContinueText(app):
    drawLabel('Press p to unpause and continue the game', 
              app.width//2, app.height//2, size=30, bold=True)

def drawInstructionText(app, text):
    if app.textSize > 0:
        drawLabel(f'{text}', app.width//2, app.height//2, 
                             size=app.textSize, bold=True)


def main():
    runApp(width=800, height=600)

main()
