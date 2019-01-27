import os.path
import numpy as np
import imageio

from PIL import Image, ImageDraw, ImageFont
from math import trunc

def convertImage(in_file, out_file):
    # default size 1000x500
    base_width = 1000
    base_size = 500
    # open the image and grey scale it
    img = Image.open(in_file).convert('L')
    # resize the image
    img = img.resize((base_width, base_size), Image.ANTIALIAS)
    # get the pixel array
    pixel_Arr = np.array(img)
    # ASCII art
    ASCII = ['.', ',', '*', '^', '!', '|', '+', '-', ':', ';', 'o', 'x', '%', '?', '$', '#', '@']
    # assign each character to it corresponding pixel value
    f = open(out_file, 'w')
    for x in pixel_Arr:
        for y in x:
            f.write(ASCII[trunc(y/255*17) - 1])
        f.write('\n')
    # close file
    f.close()
    return True


def getFrame(in_file):
    # get each frame from the gif file
    try:
        i = 0
        img = Image.open(in_file)
        while 1:
            img.seek(i)
            imframe = img.copy()
            if i == 0:
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe.convert('L')
            i = i + 1
    except EOFError:
        pass


def convertGif(in_file, out_file):
    # default size 256x256
    base_width = 256
    base_size = 256
    # open the image and grey scale it
    img = Image.open(in_file).convert('L')
    # resize the image
    img = img.resize((base_width, base_size), Image.ANTIALIAS)
    # get the pixel array
    pixel_Arr = np.array(img)
    # ASCII art
    ASCII = ['.', ',', '*', '^', '!', '|', '+', '-', ':', ';', 'o', 'x', '%', '?', '$', '#', '@']
    # assign each character to it corresponding pixel value
    f = open(out_file, 'w')
    for x in pixel_Arr:
        for y in x:
            f.write(ASCII[trunc(y/255*17) - 1])
        f.write('\n')
    # close file
    f.close()
    return True


def textToImage(input_file, output_file):
    font = ImageFont.truetype('cour.ttf', 3)
    img = Image.new('L', (500, 256), color=255)
    draw = ImageDraw.Draw(img)
    vertical_scale = 5
    with open(input_file) as f:
        lines = f.readlines()

    for line in lines:
        draw.text((0, vertical_scale), line, fill=0, font=font)
        vertical_scale = vertical_scale + 1
    img.save(output_file)


def imagesToGif(input_dir, output_file):
    images = []
    list_file = os.listdir(input_dir)
    for filename in list_file:
        images.append(imageio.imread(input_dir + filename))
    imageio.mimsave(output_file, images)
    return True
