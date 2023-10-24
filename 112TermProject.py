#title: A Game of Flying Birds
#time: Apr 2023
#spring23 15112 term project
#name: Qidu(Quentin) Fu

# --------------------------------------------------------------------------

# inspired by the Google's Earth Day Doodle 
# and Mike's (15112 instructor) scaffolded project
# https://www.google.com/doodles/earth-day-2020

#import necessary modules
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
    #Generate docstring for the class
    """
    This class is the parent class of the Player and Helper classes.
    It contains the common attributes and methods of the Player and Helper
    classes.
    """

    def __init__(self):
        self.inventory = []
        self.birdCounter = 0
        self.stepCounter = 0
        self.birdsImages = []
        self.birdsImagesLeft = []
        self.birdsImagesRight = []
        # initiate bird's image width and height
        self.birdWidth, self.birdHeight = None, None 

        # loading bird images
        self.loadBirdImage()

    def loadBirdImage(self):
        """ Initiate the bird images and their sizes
        """
        # The bird picture is from 
        # URL: https://www.pngitem.com/middle/ihbJiib_transparent-bird-bird-sprite-sheet-png-png-download/
        originalPic = 'images/birdPic.png'
        birdImage = Image.open(originalPic)
        birdImageNum = 3 

        #crop the bird picture and store the sprite bird pic into the birds list
        # The next 3 lines are adaptations of 112's course note
        # URL: http://www.cs.cmu.edu/~112-f22/notes
        # /notes-animations-part4.html#spritesheetsWithCropping
        for index in range(birdImageNum):
            bird = birdImage.crop((320*index, 0, 320*(index+1), 1232))
            imageWidth, imageHeight = bird.width, bird.height

            #bird images facing the right
            self.birdsImagesRight.append(CMUImage(bird))

            #bird images facing the left 
            bird = bird.transpose(Image.FLIP_LEFT_RIGHT)
            self.birdsImagesLeft.append(CMUImage(bird))

            #decrease the image size
            self.birdWidth, self.birdHeight = (imageWidth//4, imageHeight//3)
    
# # --------------------------------------------------------------------------
# # --------------------------------------------------------------------------
# # # The Player bird --------------------------------------------------------
# # --------------------------------------------------------------------------
# # --------------------------------------------------------------------------

class Player(Bird):
    """
    This class is the child class of the Bird class.
    It contains the attributes and methods of the Player class.
    """

    def __init__(self, x, y):
        """Initiate the Player class

        Args:
            x(int/float): x coordinate of the bird
            y(int/float): y coordinate of the bird
        """
        super().__init__()
        self.x, self.y = x, y #bird location

        #initiate cursor position to be the same as the bird position
        self.cursorX, self.cursorY= x, y

        #initiate the positions for birds' feet
        self.birdFeetX, self.birdFeetY = x, y
        #initiate the positions for the dots' on bird feet, which are different
        #from the birds' feet due to the image issues
        self.dotX, self.dotY = x, y

        #indicate the bird's heading direction: right or left
        self.birdDirection = 0 

        self.playerSteps = 0
        self.playerStepsPerSecond = 4

    def playerOnStep(self, app):
        """Update the player's attributes per call
        Args:
            app(object): the app object
        """
        # get the birds' heading direction
        self.getBirdDirection()
        #change brids facing direciton
        self.changeDirection()        
        #update birds' wings flapping speed
        self.updateWingFlapping()
        #move locations towards the cursors
        self.moveToCursor() 
        #gather/pollinate flowers
        self.gatherAndPollinateFlower(app)
        #update the inventory per step
        self.updateInventory(app)

        self.stepCounter += 1

    def getBirdDirection(self):
        """Get the bird's heading direction
        """
        if self.cursorX - self.x < 0:
            self.birdDirection = -1
        else:
            self.birdDirection = 1

    def changeDirection(self):
        """Change the bird's facing direction
        """
        # when it is less than 0, bird is flying towards left
        if self.birdDirection < 0:
            self.birdsImages = self.birdsImagesLeft
        # when it is no less than 0, bird is flying towards right
        else:
            self.birdsImages = self.birdsImagesRight

    def updateWingFlapping(self):
        """Update the bird's wings flapping speed
        """
        dist = Player.distance(self.x, self.y, self.cursorX, self.cursorY)
        newStepCounter = dist // 10  

        #The next 3 lines are adaptations of 112's course note
        # URL: http://www.cs.cmu.edu/~112-f22/notes
        # /notes-animations-part4.html#spritesheetsWithCropping
        if (self.stepCounter >= (10 - newStepCounter)): 
            self.birdCounter = (1 + self.birdCounter) % len(self.birdsImages)
            self.stepCounter = 0

    def moveToCursor(self):
        """Move the bird towards the cursor
        """
        #get the movement distances between the cursor and current locations
        distanceX = self.cursorX - self.x
        distanceY = self.cursorY - self.y

        #update the birds' locations with 1/8 of the current distances
        updatingRatio =  1/8
        if (distanceX != 0 ) and (distanceY != 0):
            self.x += distanceX * updatingRatio
            self.y += distanceY * updatingRatio

        #make up the misplacement between the bird's feet and cursor locations
        self.birdFeetX = self.x - 2
        self.birdFeetY = self.y + 135

        #update the  coordinates of the dot on birds' feet
        self.dotX = self.x
        self.dotY = self.y

    def gatherAndPollinateFlower(self, app):
        """Gather and pollinate flowers
        
        Args:
            app(object): the app object
        """
        for flower in app.flowers:
            #checked if the dots interact with the flower
            isInteracted = Player.distance(self.dotX, self.dotY, 
                            flower.x, flower.y) <= (flower.radius + 15)
                                                    #dot's radius is 15

            if isInteracted == True:
                self.gatherFlowers(app, flower)
                self.pollinateFlowers(app, flower)

    def gatherFlowers(self, app, flower):
        """Gather flowers
        Args:
            app(object): the app object
            flower(object): the flower object
        """
        # gather the flowers/pollination from pollinators
        if ((flower.isPollinator) and 
            (flower.gatheredTimes > 0) and 
            #each gather takes 1 sec. Full gathering takes 2s per flower.
            (app.stepCounter % app.flowerPerSecond == 0)): 
            flower.gatheredTimes -= 1
            flower.isGathered = True
            
            #flowers grows when it is gathered
            flower.growing = True

    def pollinateFlowers(self, app, flower):
        """Pollinate flowers

        Args:
            app (object): the app object
            flower (object): the flower object
        """
        inventory = self.inventory
        #pollinate when the inventory has the correct colors
        #it is not a pollinator and has not been pollinated
        if ((len(inventory) >= 0) and (flower.color in inventory) and 
            (not flower.isPollinator) and (flower.pollinatedTimes == 1)): 
            flower.isPollinated = True 
            flower.pollinatedTimes -= 1

            # when pollinated, flowers grow
            flower.growing = True

            # when pollinated, update the inventory
            inventory.remove(flower.color)

            # score + 1 when a flower is pollinated
            app.score += 1

    def updateInventory(self, app):
        """Update the flower inventory

        Args:
            app (object): the app object
        """
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
        """Draw the bird, inventory and the dots on the bird's feet

        Args:
            app (object): the app object
        """
        self.drawBird(app)
        self.drawInventory(app)
        #draw the dots carried by the bird's feet
        self.drawDot(app)
    
    def drawBird(self, app):
        """draw the bird

        Args:
            app (object): the app object
        """
        if len(self.birdsImages) > 0:
            bird = self.birdsImages[self.birdCounter]
            # due to the image issues, the bird is drawn the its feet
            drawImage(bird, self.birdFeetX, self.birdFeetY, align='center', 
                        width=self.birdWidth, height=self.birdHeight)

    def drawDot(self, app):
        """Draw the dots on the bird's feet

        Args:
            app (object): the app object
        """
        # if the inventory not empty draw the carrying dot to the bird's feet
        if len(self.inventory) > 0:
            increment = 0 # increment of X when drawing the dot on bird's feet
            colorsDrawn = set()
            for color in self.inventory:
                #only draw  the dot with color which has not been drawn
                if color not in colorsDrawn:
                    drawCircle(self.dotX + increment, self.dotY, 15, fill=color)
                    increment += 10
                    colorsDrawn.add(color)

    def drawInventory(self, app):
        """Draw the inventory
        Args:
            app (object): the app object
        """
        for i in range(len(self.inventory)):
            color = self.inventory[i]
            drawCircle(20+i*25, 20, 20, fill=color)
            #label the inventory colors with numbers starting from 1
            drawLabel(f'{i+1}', 20+i*25, 20)
    
    @staticmethod
    def distance(x0, y0, x1, y1):
        """Calculate the distance between two points
        Args:
            x0(int/float): x coordinate of the first point
            y0(int/float): y coordinate of the first point
            x1(int/float): x coordinate of the second point
            y1(int/float): y coordinate of the second point
        """
        return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # The Helper birds -------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Helper(Player):
    """This is the child class of the Player class.
    It contains the attributes and methods of the Helper class.
    """

    def __init__(self, x, y):
        """Initiate the Helper class
        Args:
            x(int/float): x coordinate of the bird
            y(int/float): y coordinate of the bird
        """
        super().__init__(x, y)
        self.target = None
        self.normalFlapping = True # birds' wing flapping speed
        self.inventory = []

    def helperOnStep(self, app):
        """Update the helper birds' attributes per call
        Args:
            app(object): the app object
        """
        # get the birds' heading direction
        self.getBirdDirection()
        # update birds facing direction
        self.changeDirection()
        #helper birds move towards the taget
        self.getTargetAndMakeMove(app) 
        #gather/pollinate flowers
        self.gatherAndPollinateFlower(app)
        #update the inventory per step
        self.updateInventory(app)
        #update birds' wings flapping speed
        self.updateWingFlapping()
        
        self.stepCounter += 1

    def getBirdDirection(self):
        """Get the bird's heading direction
        """
        if self.target != None: 
            if self.target.x - self.x < 0:
                self.birdDirection = -1
            else:
                self.birdDirection = 1
    
    def getTargetAndMakeMove(self, app):
        """Get the target and make the helper birds move towards the target
        Args:
            app(object): the app object
        """
        if self.target != None:
            #check the legality of the target
            if self.isValidTarget():
                # if target is valid, bird flapping speed will increase
                self.normalFlapping = False
                self.makeTargetMove(app)                
            else:
                self.target = None
                # if target is None, bird flapping speed is normal
                self.normalFlapping = True
        else:
            self.getTarget(app)

    def isValidTarget(self):
        """Check if the target is valid
        """
        result = (  (self.target.growing == False) and # ungathered/unpollinated
                    (self.target.y > 0)) # on canvas
        return result

    def makeTargetMove(self, app):
        """Make the helper birds move towards the target
        Args:
            app(object): the app object
        """
        targetX, targetY = self.target.x, self.target.y
        canvasMidLine = app.width // 2
        
        #get the movement distances between the target and current locations
        distanceX = targetX - self.x
        distanceY = targetY - self.y

        #update the birds' locations with 1/10 of the current distances
        updatingRatio =  1/10
        self.newX = distanceX * updatingRatio + self.x

        #make sure the bird on the right side of canvas stays on the right 
        if (self.x > canvasMidLine) and (self.newX > canvasMidLine):
            self.x = self.newX
        #make sure the bird on the left side  stays on the left
        elif (self.x <= canvasMidLine) and (self.newX <= canvasMidLine):
            self.x = self.newX

        self.y += distanceY * updatingRatio

        #make up the different between the bird's feet and cursor locations
        self.birdFeetX = self.x - 2
        self.birdFeetY = self.y + 105

        #update the  coordinates of the dots on birds' feet and 
        #make up the differences between the cursors and the dots
        self.dotX = self.x - 9
        self.dotY = self.y - 38

    def getTarget(self, app):
        """Get the target
        Args:
            app(object): the app object
        """
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
        """Get the target flower
        Args:
            flower(object): the flower object
            shortestDist(int/float): the shortest distance between the bird and
            the flower
            app(object): the app object
        """
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
        """Get the closest flower
        Args:
            flower(object): the flower object
            shortestDist(int/float): the shortest distance between the bird and
            the flower
        """
        #not fully gathered or unpollinated flowers
        if (flower.gatheredTimes != 0) or (flower.pollinatedTimes != 0):
            currentDist = Player.distance(self.dotX, self.dotY, 
                                            flower.x, flower.y)
            if (shortestDist == None) or (shortestDist > currentDist):
                shortestDist = currentDist
                self.target = flower

    def updateWingFlapping(self):
        """Update the bird's wings flapping speed
        """
        #when target is none, birds wings flap normally
        if self.normalFlapping:
            if self.stepCounter >= 5:
                #The next 2 lines are adaptation of 112's course note
                # URL: http://www.cs.cmu.edu/~112-f22/notes
                # /notes-animations-part4.html#spritesheetsWithCropping
                self.birdCounter = (1+self.birdCounter) % len(self.birdsImages)
                self.stepCounter = 0
        else:
            #when target is not none, birds wings flap  increase accordingly
            dist = Player.distance(self.x, self.y, self.target.x, self.target.y)
            newStepCounter = dist // 10 
            if self.stepCounter >= (10 - newStepCounter): 
                #The next 2 lines are adaptation of 112's course note
                # URL: http://www.cs.cmu.edu/~112-f22/notes
                # /notes-animations-part4.html#spritesheetsWithCropping
                self.birdCounter = (1+self.birdCounter) % len(self.birdsImages)
                self.stepCounter = 0

    def redrawBirdAll(self, app):
        """Draw the bird, inventory and the dots on the bird's feet
        Args:
            app (object): the app object
        """
        self.drawBird(app) 
        self.drawInventory(app) 
        self.drawDot(app) 

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # FLOWER------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Flower(object):
    """This class contains the attributes and methods of the Flower class.
    """

    def __init__(self, isPollinator, app):
        """Initiate the Flower class
        Args:
            isPollinator(bool): True if it is a pollinator, False if it is 
            pollinated
            app(object): the app object
        """
        self.radius = 20 # initiate flower radius to be 20
        self.x = random.randint(self.radius, app.width - self.radius)
        self.y = app.height + self.radius

        # True pollinator else pollinated
        self.isPollinator = isPollinator 

        # initiate the times that a flower can be gathered
        self.gatheredTimes = 2
        #initiate the time that a flower can be pollinated
        self.pollinatedTimes = 1

        #initiate flower colors
        self.color = random.choice(['cyan', 'pink', 'yellow'])
        
        #indicator for flowers are pollinated
        self.isPollinated = False
        #check if a flower is gathered
        self.isGathered = False
        #check if a flower is growing
        self.growing = False

        #initiate dx/dy/ddx velocities and acceleration. 
        # I think 6 for dx and 5 for dy the best for my game 
        self.dx = math.sin(6 * self.y) 
        self.dy = 5
        self.ddx = 0.01

    def __repr__(self):
        """Return the flower's location
        """
        return f"Flower: ({self.x}, {self.y})"
    
    def flowerOnStep(self, app):
        """Update the flower's attributes per call
        Args:
            app(object): the app object
        """
        # update position through the offset
        self.updateFlowerLocation(app)

        #update radius per call when it is growing
        if self.growing == True:
            self.updateFlowerRadius()
    
    def updateFlowerRadius(self):
        """Update the flower's radius
        """
        #set the max radius of the flowers to 30
        maxRadius = 30
        #set the medium radius to 25
        midRadius = 25
        #radius grows by 2 per call
        growingSpeed = 2
        if self.gatheredTimes == 1:
            #when the pollinator is not fulled gathered
            self.radius = min(self.radius + growingSpeed, midRadius)
        else:
            # if its pollinated/fully gathered
            self.radius = min(self.radius + growingSpeed, maxRadius)

    def updateFlowerLocation(self, app):
        """Update the flower's location
        Args:
            app(object): the app object
        """
        self.y -= self.dy #update y
        if (self.x > self.radius) and (self.x < app.height):
            self.x -= self.dx #update x through dx/velocity
            self.dx += self.ddx #update dx through ddx/acceleration
    
    def redrawFlower(self, app):
        """Draw the flower
        Args:
            app(object): the app object
        """
        self.drawFlower(app)

    def drawFlower(self, app):
        """Draw the flower
        Args:
            app(object): the app object 
        """
        if self.isPollinator:    
            self.drawPollinator(app)
        else:
            self.drawPollinated(app)

    def drawPollinator(self, app):
        """draw the pollinator

        Args:
            app (object): the app object
        """
        #solid circles for pollinator when they have not been gathered
        if self.gatheredTimes == 2:
            drawCircle(self.x, self.y, self.radius, fill=self.color)

        # gathered the first time: ringed circles
        elif self.gatheredTimes == 1:
            drawCircle(self.x, self.y, self.radius, fill=app.background,
                            border=self.color, borderWidth=4)
            drawCircle(self.x, self.y, 10, fill=self.color)
        
        # second gathered pollination: hollow circles
        elif self.gatheredTimes == 0:
            drawCircle(self.x, self.y, self.radius, fill=app.background,
                            border=self.color, borderWidth=4)
    
    def drawPollinated(self, app):
            # hollow circles for being pollinated
            drawCircle(self.x, self.y, self.radius, fill=app.background,
                            border=self.color, borderWidth=4)
            if self.isPollinated: 
                #after it is pollinated, it becomes a solid circle
                drawCircle(self.x, self.y, self.radius, fill=self.color)
    
    @staticmethod
    def removeAndGenerateFlowers(app):
        """Remove and generate flowers
        Args:
            app(object): the app object
        """
        #remove flowers when they are outside the canvas
        Flower.removeOffCanvasFlowers(app)
        #generate flowers periodically
        Flower.generateFlowers(app)

    @staticmethod
    def removeOffCanvasFlowers(app):
        """Remove flowers when they are outside the canvas
        Args:
            app(object): the app object
        """
        index = 0
        while index < len(app.flowers):
            flower = app.flowers[index]
            #remove the flower moving outside of the cavas
            if flower.y < 0:
                app.flowers.pop(index)
            else:
                index += 1

    @staticmethod           
    def generateFlowers(app):
        """Generate flowers periodically
        Args:
            app(object): the app object
        """
        #generate 4 flowers per second with a total of 20 flowers on the screen
        totalFlowerNumber = 20
        if ((app.stepCounter % app.flowerPerSecond == 0) and 
            (len(app.flowers) < totalFlowerNumber)):
            #randomly generate pollinator or pollinated
            isPollinator = random.choice([True, False])
            app.flowers.append(Flower(isPollinator, app))


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # TEXT---------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
class Text(object):
    """This class contains the attributes and methods of the Text class.
    """

    def __init__(self):
        """Initiate the Text class
        """
        self.textSize = 30 #initiate the size instruction text 
        self.textStepCounter = 0

    def textOnStep(self):
        """Update the text's attributes per call
        """
        #update the text size per call
        self.updateInstructionText()
        self.textStepCounter += 1

    def updateInstructionText(self):
        """Update the instruction text size per call
        """
        #reset the instruction text size when it is <= 0
        initialTextSize = 30 
        if self.textSize <= 0:
            self.textSize = initialTextSize
        else:
            #text size decreases 0.2 per call
            shrinkingSpeedPerCall = 0.2
            self.textSize -= shrinkingSpeedPerCall
    
    def redrawAllInstructionText(self, app):
        """Draw all the instruction text
        Args:
            app(object): the app object
        """
        #draw the below instructions once every 1050 calls
        counter = self.textStepCounter % 1050

        #while the game is paused, show instruction for unpausing the game
        if app.paused == True:
            Text.drawToContinueText(app)

        #while the game playing, to enhance user experience, 
        #show  text when the remainder/counter satifies the below periodically
        elif 0 <= counter < 150:  # textSize / shrinkingSpeed = 30/0.2 = 150
            text = 'Having fun :)'
            self.drawInstructionText(app, text)
        elif 150 <= counter < 300:
            text = "Move your cursor/bird's feet to gather/pollinate flowers"
            self.drawInstructionText(app, text)
        elif 300 <= counter < 450:
            text = 'Enjoy the game :)'
            self.drawInstructionText(app, text)
        elif 450 <= counter < 600:
            text = 'Press p to pause the game'
            self.drawInstructionText(app, text)
        elif 600 <= counter < 750:
            text = 'Press h to get helper birds'
            self.drawInstructionText(app, text)
        elif 750 <= counter < 900:
            text = 'Press r to restart the game'
            self.drawInstructionText(app, text)
        elif 900<= counter < 1050:
            text = f"Your current score is: {app.score}"
            self.drawInstructionText(app, text)

    def drawInstructionText(self, app, text):
        """Draw the instruction text
        Args:
            app(object): the app object
            text(str): the instruction text
        """
        if self.textSize > 0:
            drawLabel(f'{text}', app.width//2, app.height//2, 
                                size=self.textSize, bold=True)
    
    @staticmethod
    def drawToContinueText(app):
        """Draw the instruction text for unpausing the game
        Args:
            app(object): the app object
        """
        drawLabel('Press p to unpause and continue the game', 
                                app.width//2, app.height//2, size=30, bold=True)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # APP---------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

def onAppStart(app):
    """Initiate the app
    Args:
        app(object): the app object
    """
    reset(app)

def reset(app):
    """Reset the app
    Args:
        app(object): the app object
    """
    app.background = 'lightGreen'
    app.player = Player(400, 400)
    app.text = Text()
    app.flowers = []
    app.flowerPerSecond = 5
    
    app.stepCounter = 0 
    app.paused = False
    app.helper1 = None
    app.helper2 = None
    app.score = 0 

def onKeyPress(app, key):
    """Respond to the key press
    Args:
        app(object): the app object
        key(str): the key pressed
    """
    if key == 'r':
        reset(app)
    elif key == 'p':
        app.paused = not app.paused
    elif key == 'h':
        app.helper1 = Helper(0, 0)
        app.helper2 = Helper(app.width, app.height)

def onMouseMove(app, x, y):
    """Respond to the mouse move
    Args:
        app(object): the app object
        x(int/float): x coordinate of the mouse
        y(int/float): y coordinate of the mouse
    """
    app.player.cursorX = x
    app.player.cursorY = y

def onStep(app):
    """Respond to the step
    Args:
        app(object): the app object
    """
    if app.paused == False:
        takeStep(app)

def takeStep(app):
    """Take a step
    Args:
        app(object): the app object
    """
    app.player.playerOnStep(app)
    app.text.textOnStep()

    #update helper birds' calls if the birds exist
    if app.helper1 != None:
        app.helper1.helperOnStep(app)
        app.helper2.helperOnStep(app)

    for flower in app.flowers:
        flower.flowerOnStep(app)
        
    #remove and generate flowers off/on vcanvas
    Flower.removeAndGenerateFlowers(app)
    
    app.stepCounter += 1

def redrawAll(app):
    """Redraw all the objects
    Args:
        app(object): the app object
    """
    #draw instruction text
    app.text.redrawAllInstructionText(app)

    #draw player
    app.player.redrawBirdAll(app)

    #draw helpers when they are called
    if app.helper1 != None: 
        app.helper1.redrawBirdAll(app)
        app.helper2.redrawBirdAll(app)

    #draw flowers
    for flower in app.flowers:
        flower.redrawFlower(app)

def main():
    """Run the app
    """
    runApp(width=800, height=600)

if __name__=='__main__':
    main()
