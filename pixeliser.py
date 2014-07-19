from PIL import Image, ImageDraw

#open the image to be pixelated
image_file = "face.jpg"
output_file = "pixeled.jpg"
img = Image.open(image_file)
img_width = img.size[0]
img_height = img.size[1]
print("opened %s [%d x %d]" % (image_file,img_width,img_height))

pix_img = Image.new("RGB",(img_width,img_height))
draw = ImageDraw.Draw(pix_img)

#sums to work out how many and how big the tiles are
x_tiles = 20
tile_width = img_width / x_tiles
#assume square tiles
y_tiles = img_height / tile_width

#function that returns the average value of a region of pixels
def avg_region(image,box):
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
        box = (x, y, x+tile_width, y+tile_width)
        avg_colour = avg_region(img,box)

        #replace that region with a uniform colour
        draw.rectangle(box,fill=avg_colour)

#save it!
print("saved as %s" % output_file)
pix_img.save(output_file)
