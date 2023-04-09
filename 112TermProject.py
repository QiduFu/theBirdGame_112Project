#BEE GAME
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



# The BEE (main)
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Bee(object):
    def __init__(self, app):
        pass
    
    def onStep(self):
        pass

    def getTarget(Self):
        pass

    def getHeldColors(self):
        pass

    def gather(self, other):
        pass

    def redraw(self, canvas):
        pass

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# # The BEE (Player BEE)----------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Player(Bee):
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY
        self.cursorX = 400 #mid point of the canvas
        self.cursorY = 400 #mid point of the canvas
        self.playerSteps = 0
        self.playerStepsPerSecond = 4
    
    def drawPlayer(self, app):
        drawCircle(self.locX, self.locY, 30, fill='cyan')
        drawImage(app.url, 325, 200, align='center')
    
    def playerOnStep(self):
        self.makeMovement()
       
    def makeMovement(self):
        #get the drection of the bee's movement left/up - 1, right/down +1
        moveDistanceX = self.cursorX - self.locX
        moveDisctanceY = self.cursorY - self.locY
        self.locX += moveDistanceX / 10
        self.locY += moveDisctanceY / 10

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
# # The BEE (Helper BEES)---------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Helper(Bee):
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

    def __init__(self, locX, locY, color, pollinator):
        self.x = locX
        self.y = locY
        self.color = color
        # True pollinator else pollinated
        self.pollinator = pollinator
    
    def flowerOnStep(self):
        pass

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
    flagBeeWings(app)
    app.player1 = Player(400, 400)

def flagBeeWings(app):
    # The bee picture is from https://opengameart.org/content/bee-enemy
    app.url = 'beePic.png'
    picWidth, picHeight = getImageSize(app.url)
    print(f"{picWidth, picHeight = }")

def onMouseMove(app, x, y):
    app.player1.cursorX = x
    app.player1.cursorY = y

def onStep(app):
    app.player1.playerOnStep()

def redrawAll(app):
    drawTitle(app)
    app.player1.drawPlayer(app)

def drawTitle(app):
    drawLabel('A Tale of the Bee Game', 400, 30, size=30)
    
def main():
    runApp(width=800, height=800)

main()
