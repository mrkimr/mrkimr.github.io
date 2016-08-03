import os.path
import matplotlib.pyplot as plt
import PIL
import PIL.ImageDraw
import numpy as np
import math

def avg(pixel):
    return (pixel[0] + pixel[1] + pixel[2])/3

def gray(filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(directory, filename)
    img = plt.imread(filepath)

    height = len(img)
    width = len(img[0])
    
    for r in range(height):
        for c in range(width):
            a = avg(img[r][c])
            img[r][c][0]= a
            img[r][c][1]= a
            img[r][c][2]= a
     
    return img


def mask(image):
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'cateyes.png')
    orig = PIL.Image.open(filename)    
    filename = os.path.join(directory, 'cateyes_grayscale.png')
    img = PIL.Image.open(filename)
    
    #img = PIL.Image.fromarray(image)
    width, height = img.size
    radius = int(0.53 * min(width, height))
    # Create mask
    rounded_mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
    drawing_layer = PIL.ImageDraw.Draw(rounded_mask)
    drawing_layer.polygon([(radius,0),(width-radius,0),
                          (width-radius,height),(radius,height)],
                          fill=(127,0,127,255))
    drawing_layer.polygon([(0,radius),(width,radius),
                          (width,height-radius),(0,height-radius)],
                          fill=(127,0,127,255))
    drawing_layer.ellipse((0,0, 2*radius, 2*radius), 
                          fill=(0,127,127,255)) #top left
    drawing_layer.ellipse((width-2*radius, 0, width,2*radius), 
                          fill=(0,127,127,255)) #top right
    drawing_layer.ellipse((0, height-2*radius, 2*radius,height), 
                          fill=(0,127,127,255)) #bottom left
    drawing_layer.ellipse((width-2*radius, height-2*radius, width, height), 
                       fill=(0,127,127,255)) #bottom right
    # Apply rounded_mask to img                    
    result = PIL.Image.new('RGBA', (width, height))
    result.paste(img, (0,0), mask=rounded_mask)
    

    fig, axes = plt.subplots(1, 3)
    axes[0].axis("off")
    axes[0].imshow(orig, interpolation="none")
    axes[0].set_title("original")
    axes[1].axis("off")
    axes[1].imshow(image, interpolation="none")
    axes[1].set_title("grayscale")
    axes[2].axis("off")
    axes[2].imshow(result, interpolation='none')
    axes[2].set_title('result')
    fig.show()
    
    result.save("final.png", "PNG")

mask(gray("cateyes.png"))