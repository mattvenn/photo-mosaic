from PIL import Image, ImageDraw
import os
import colorsys

image_dir = 'images/'

#the template iamge
template_file = "face.jpg"
template_img = Image.open(template_file)
template_width = template_img.size[0]
template_height = template_img.size[1]
template_aspect = float(template_height) / float(template_width)

#how big we want the mosiac to be
mos_width = 640
mos_height = int(mos_width * template_aspect)
print("mos height = %d" % mos_height)

#number of photos we want to use across x
x_tiles = 20
y_tiles = int(template_aspect * x_tiles)

#sums to work out how many and how big the tiles are
template_tile_width = template_width / x_tiles
mos_tile_width = mos_width / x_tiles

print("mos tile width = %d" % mos_tile_width)

#create a blank image
mos_image = Image.new('RGB',(mos_width,mos_height), "white")

#function that returns the average value of a region of pixels
def avg_region(image,box):
    region = image.crop(box)
    colors = region.getcolors(region.size[0]*region.size[1])
    max_occurence, most_present = 0, 0
    for c in colors:
        if c[0] > max_occurence:
            (max_occurence, most_present) = c
    return most_present

#get all the images in our image directory
all_files = os.listdir(image_dir)
num_files = len(all_files)

#new list to store analysed image
analysed = []

#analyse all those images to get the average colour
print("starting analyis")
for file in all_files:
    print("."),
    try:
        img = Image.open(image_dir + file)
        img_width = img.size[0]
        img_height = img.size[1]
        box = ( 0, 0, img_width, img_height)
        avg_colour = avg_region(img,box)
        #get the hue, divide by 255 as this function takes args from 0 to 1

        #add the image and it's main colour to the list
        analysed.append((avg_colour,file))
    except IOError:
        print("skipping %s, couldn't open" % file)

  
print("")
print("analysed %d files" % len(all_files))

#analysed = sorted(analysed,key=lambda x: x[0])

def get_close_image(target_colour):
    #start large
    closest_match = 1000
    (T_R, T_G, T_B) = target_colour
    for (avg_colour,file) in analysed:
        (R,G,B) = avg_colour 
        if abs(T_R-R) + abs(T_G-G) + abs(T_B-B) < closest_match:
            closest_match = abs(T_R-R) + abs(T_G-G) + abs(T_B-B)
            closest_colour = avg_colour
            closest_file = file

    print("closest to %s was %s" % (target_colour, closest_colour))
    return closest_file

#now for all the tiles in the template image
for x_tile in range(x_tiles):
    for y_tile in range(y_tiles):

        #find closest colour
        x = x_tile * template_tile_width
        y = y_tile * template_tile_width
        box = (x, y, x+template_tile_width, y+template_tile_width)
        avg_colour = avg_region(template_img,box)

        #find an image that matches the hue in our sorted list
        file = get_close_image(avg_colour)
        tile = Image.open(image_dir + file)

        #resize it
        tile = tile.resize((mos_tile_width,mos_tile_width))

        #and paste it in
        mx = x_tile * mos_tile_width
        my = y_tile * mos_tile_width
        box=(mx,my,mx+mos_tile_width,my+mos_tile_width)
        try:
            mos_image.paste(tile,box)
        except ValueError:
            print( box )
            print(tile.size)

#save it!
mos_image.save("mosiac.jpg")

