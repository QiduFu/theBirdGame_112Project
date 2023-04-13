from cmu_graphics import *
from PIL import Image
import os, pathlib

#See: https://pillow.readthedocs.io/en/stable/reference/Image.html 

def onAppStart(app):
    app.margin = 5

    # Open image from local directory
    app.image = Image.open("images/Caaaaat.jpg")
    
    # If the above line displays the error
    # FileNotFoundError: [Errno 2] No such file or directory: 'images/Caaaaat.jpg'
    # it is because PIL is looking for the file
    # in the directory Python is installed in.
    # Instead, either use absolute file path 
    # or comment out the line above and use the line below.
    
    app.image = Image.open(os.path.join(pathlib.Path(__file__).parent,"images/Caaaaat.jpg"))
    
    # Note that you need to "import os, pathlib" for this to work!
    # If this is the solution that works on your operating system,
    # I recommend defining a custom function to open images as such:
    
    def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
    
    app.image = openImage("images/Caaaaat.jpg")
    
    
    # Moving on...
    # Access attributes like width and height
    app.imageWidth,app.imageHeight = app.image.width,app.image.height

    # Use 'transpose' to flip images
    app.imageFlipped = app.image.transpose(Image.FLIP_LEFT_RIGHT)

    # Cast image type to CMUImage to allow for faster drawing
    app.image = CMUImage(app.image)
    app.imageFlipped = CMUImage(app.imageFlipped)

def redrawAll(app):
    # drawPILImage takes in a PIL image object and the left-top coordinates
    drawImage(app.image,100,100)

    # Scale image by defining new dimensions 
    newWidth, newHeight = (app.imageWidth//2,app.imageHeight//2)
    drawImage(app.image,500,100,width=newWidth,height=newHeight)

    drawImage(app.imageFlipped,100,500)
    # Rotate image by a given angle (in degrees :/)
    drawImage(app.image,500,500,rotateAngle=-60)
    drawCaptions(app)

def drawCaptions(app):
    drawLabel('Original',100,100 - app.margin,align='left-bottom',size=24)
    drawLabel('Scaled',500,100 - app.margin,align='left-bottom',size=24)
    drawLabel('Flipped',100,450 - app.margin,align='left-bottom',size=24)
    drawLabel('Rotated',500,450 - app.margin,align='left-bottom',size=24)

def main():
    runApp(width=800,height=800)

if __name__ == '__main__':
    main()