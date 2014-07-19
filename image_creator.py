from PIL import Image, ImageDraw
size = 50
colour_step = 20
for R in range(0,255,colour_step):
    for G in range(0,255,colour_step):
        for B in range(0,255,colour_step):
            image = Image.new('RGB',(size,size), (R,G,B))
            filename = "%03d%03d%03d.jpg" % (R,G,B)
            image.save(filename)

