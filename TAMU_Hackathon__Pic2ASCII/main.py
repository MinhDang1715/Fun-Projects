import os.path
import numpy as np
import imageio

from PIL import Image, ImageDraw, ImageFont
from math import trunc

def convertImage(in_file, out_file):
    # default size 1000x284
    base_width = 1000
    base_size = 284
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

# note for ratio
# the width of the output gif will be the base_width of the frame * 2
# the size(height) of the output gif will be the same as the base_size of the frame
# however be careful with the size of the text and the vertical + horizontal scale

# detail mode
def convertGifDetail(in_file, out_file):
    # default size 256x256
    base_width = 250
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


def textToImageDetail(input_file, output_file):
    font = ImageFont.truetype('cour.ttf', 3)
    img = Image.new('L', (500, 500), color=255)
    draw = ImageDraw.Draw(img)
    vertical_scale = 0
    with open(input_file) as f:
        lines = f.readlines()

    for line in lines:
        draw.text((0, vertical_scale), line, fill=0, font=font)
        vertical_scale = vertical_scale + 1
    img.save(output_file)


# simple mode
def convertGifSimple(in_file, out_file):
    # default size 100x80
    base_width = 50
    base_size = 30
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


def textToImageSimple(input_file, output_file):
    font = ImageFont.truetype('cour.ttf', 10)
    # img = Image.new('L', (800, 800), color=255)
    img = Image.new('L', (300, 300), color=255)
    draw = ImageDraw.Draw(img)
    vertical_scale = 0
    horizontal_scale = 0
    with open(input_file) as f:
        lines = f.readlines()

    for line in lines:
        draw.text((horizontal_scale, vertical_scale), line, fill=0, font=font)
        vertical_scale = vertical_scale + 10
    img.save(output_file)


def imagesToGif(input_dir, output_file):
    images = []
    list_file = os.listdir(input_dir)
    for filename in list_file:
        images.append(imageio.imread(input_dir + filename))
    imageio.mimsave(output_file, images)
    removeFiles()
    return True


def removeFiles():
    list_file = os.listdir('gif_frame/')
    for file in list_file:
        os.remove('gif_frame/' + file)
    list_file = os.listdir('gif_frame_text/')
    for file in list_file:
        os.remove('gif_frame_text/' + file)
    list_file = os.listdir('to_image/')
    for file in list_file:
        os.remove('to_image/' + file)
