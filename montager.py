from PIL import Image, ImageDraw
import os
import random

image_dir = 'images/'

#how big we want the montage to be
mont_width = 500
mont_height = 500

#number of tiles
tiles = 10

#sums to work out how many and how big the tiles are
x_tiles = mont_width / tiles
y_tiles = mont_height / tiles
tile_width = mont_width / tiles

#create a blank image
montage_image = Image.new('RGB',(mont_width,mont_height), "white")

#get all the images in our image directory
all_files = os.listdir(image_dir)
num_files = len(all_files)

#now for all the tiles in the image
for x in range(0,mont_width,tile_width):
    for y in range(0,mont_height,tile_width):

        #pick a random image from the directory
        file = all_files[random.randint(0,num_files-1)]
        tile = Image.open(image_dir + file)

        #thumbnail it
        tile.thumbnail((tile_width,tile_width))

        #and paste it in
        box=(x,y,x+tile_width,y+tile_width)
        montage_image.paste(tile,box)

#save it!
montage_image.save("montage.jpg")
