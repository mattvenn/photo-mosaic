"""
"""
#requires python-imaging-tk
from PIL import Image, ImageDraw
import math

#open the image to be pixelated
image_file = "face.jpg"
output_file = "pixeled.jpg"
img = Image.open(image_file)
draw = ImageDraw.Draw(img)
img_width = img.size[0]
img_height = img.size[1]
print("opened %s [%d x %d]" % (image_file,img_width,img_height))

x_tiles = 10
tile_width = img_width / x_tiles
#assume square tiles
y_tiles = img_height / tile_width


#function that returns the average value of a region of pixels
def avg_region(image,x,y,width):
    x = int(x)
    y = int(y) 
    box = ( x, y, x+width, y+width)
    region = image.crop(box)
    colors = region.getcolors(region.size[0]*region.size[1])
    max_occurence, most_present = 0, 0
    for c in colors:
        if c[0] > max_occurence:
            (max_occurence, most_present) = c
    return most_present

#split the image into squares
for x in range(0,img_width,tile_width):
    for y in range(0,img_height,tile_width):
        #and for each of those squares, 
        #find the average colour
        avg_colour = avg_region(img,x,y,tile_width)

        #replace that region with a uniform colour
        box = ( x, y, x+tile_width, y+tile_width)
        draw.rectangle(box,fill=avg_colour)

print("saved as %s" % output_file)
img.save(output_file)
img.show()
