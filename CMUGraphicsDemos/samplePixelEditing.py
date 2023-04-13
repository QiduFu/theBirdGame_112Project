from cmu_graphics import *
from PIL import Image
import os, pathlib

# For more information on image modes in PIL,
# See: https://pillow.readthedocs.io/en/stable/handbook/concepts.html

def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onAppStart(app):
    app.margin = 5
    
    app.image = Image.open('images/greatPitch.gif')
    
    # Alternatively, if this throw an error,
    # as shown in basicPILMethods.py,
    # comment out the above line and use the following:
    
    app.image = openImage('images/greatPitch.gif')
    
    # now let's make a copy that only uses the red part of each rgb pixel:
    # Convert image to 'RGB' mode to access values for r,g,b from each pixel
    app.image = app.image.convert('RGB')

    # Create a new image in the 'RGB' mode with same dimensions as app.image
    app.image2 = Image.new(mode='RGB', size=app.image.size)
    for x in range(app.image2.width):
        for y in range(app.image2.height):
            r,g,b = app.image.getpixel((x,y))
            app.image2.putpixel((x,y),(r,0,0))

    # Convert images to CMUImage type
    app.image = CMUImage(app.image)
    app.image2 = CMUImage(app.image2)

def redrawAll(app):
    drawImage(app.image,100,100)
    drawImage(app.image2,400,100)
    drawCaptions(app)

def drawCaptions(app):
    drawLabel('Original',100,100 - app.margin,align='left-bottom',size=24)
    drawLabel('Red Cat!',400,100 - app.margin,align='left-bottom',size=24)

def main():
    runApp(width=700, height=600)

if __name__ == '__main__':
    main()