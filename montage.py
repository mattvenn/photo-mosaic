"""
"""
#requires python-imaging-tk
from PIL import Image, ImageTk
from PIL import ImageDraw
import math


#create a new montage image
mont_width = 640
mont_height = 480
x_tiles = 10
tile_width = mont_width / x_tiles
#assume square tiles
y_tiles = mont_height / tile_width

montage_image = Image.new('RGB',(mont_width,mont_height), "white")
draw = ImageDraw.Draw(montage_image)

#for each of the source images, find the average colour and store it in a list

image_file = "face.jpg"
background_img = Image.open(image_file)
img_width = background_img.size[0]
img_height = background_img.size[1]
print("opened %s [%d x %d]" % (image_file,img_width,img_height))




#returns the average value of a region of pixels
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

#for the background image, split it into squares
for tile_x in range(0,img_width,tile_width):
    for tile_y in range(0,img_height,tile_width):
        #and for each of those squares, 
        #find the average colour
        avg_colour = avg_region(background_img,tile_x,tile_y,tile_width)
        #print(avg_colour)

        #look to see what the closest colour is in our source images

        #copy the image into the montage
        r_pix = tile_width / 2
        box = ( tile_x, tile_y, tile_x+tile_width, tile_y+tile_width)
        draw.rectangle(box,fill=avg_colour)

        #draw.ellipse((tile_x-r_pix,tile_y-r_pix,tile_x+r_pix,tile_y+r_pix), fill=avg_colour)

montage_image.show()
montage_image.save("montage.jpg")
