from cmu_graphics import *
from PIL import Image, ImageDraw

def onAppStart(app):
    app.margin = 5
    imageWidth, imageHeight = app.width//3, app.height//2
    app.imageWidth, app.imageHeight = imageWidth, imageHeight
    backgroundColor = (0, 255, 255) # cyan
    app.image = Image.new('RGB', (imageWidth, imageHeight), backgroundColor)
    # Now that we created the image, let's use ImageDraw to draw in it
    # See https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
    # This creates an object that can be used to draw in the given image.
    # Note that the image will be modified mutatingly (in place)
    
    app.draw = ImageDraw.Draw(app.image)
    
    # And now we will create a scaled copy to show this is a normal image
    newWidth, newHeight = (app.image.width // 2, app.image.height // 2)
    app.imageScaled = app.image.resize((newWidth,newHeight))


def onMousePress(app, mouseX, mouseY):
    print('Drawing lines...')
    # We use the Drawable object (app.draw) to draw lines onto app.image
    app.draw.line((0, 0, app.imageWidth, app.imageHeight), width=10, fill=(255, 0, 0))
    app.draw.line((0, app.imageHeight, app.imageWidth, 0), width=10, fill=(0, 0, 255))
    
    # We also update app.imageScaled
    newWidth, newHeight = (app.image.width // 2, app.image.height // 2)
    app.imageScaled = app.image.resize((newWidth,newHeight))

def drawCaptions(app):
    drawLabel('Original',100,100 - app.margin,align='left-bottom',size=24)
    drawLabel('Scaled',400,100 - app.margin,align='left-bottom',size=24)

def redrawAll(app):
    # Note that app.image is a PIL Image, so we need to cast it to a CMU Image
    # before being able to draw it.
    # Why did we not do this in onAppStart, like in basicPILMethods.py?
    # Because now we are modifying app.image mutatingly,
    # and we need to be able to draw the changes made to app.image
    # in real time, not just in onAppStart.
    drawImage(CMUImage(app.image),100,100)
    drawImage(CMUImage(app.imageScaled),400,100)
    drawCaptions(app)

def main():
    runApp(width=700, height=600)

if __name__ == '__main__':
    main()