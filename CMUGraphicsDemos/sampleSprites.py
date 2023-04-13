from cmu_graphics import *
from PIL import Image
import os, pathlib

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onAppStart(app):
    #Sprite Strip: 'http://www.cs.cmu.edu/~112/notes/sample-spritestrip.png'
    
    spritestrip = Image.open('images/spritestrip.png')
    
    # Alternatively, if this throw an error,
    # as shown in basicPILMethods.py,
    # comment out the above line and use the following:
    
    spritestrip = openImage('images/spritestrip.png')
    
    app.sprites = [ ]
    for i in range(6):
        # Split up the spritestrip into its separate sprites
        # then save them in a list
        sprite = CMUImage(spritestrip.crop((30+260*i, 30, 230+260*i, 250)))
        app.sprites.append(sprite)
        
    # app.spriteCounter shows which sprite (of the list) 
    # we should currently display
    app.spriteCounter = 0
    app.stepsPerSecond = 10

def onStep(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)

def redrawAll(app):
    sprite = app.sprites[app.spriteCounter]
    drawImage(sprite,200, 200)

def main():
    runApp(width=400, height=400)

if __name__ == '__main__':
    main()