import os.path
import sys
import time
import numpy as np
import imageio
import cv2
import pygame

from PIL import Image, ImageDraw, ImageFont
from math import trunc
from pygame.locals import *
from natsort import natsorted


# convert the image to a txt file
def convertImage(in_file, out_file):
    # default size 1000 x 300
    base_width = 1000
    base_size = 300
    # open the image and grey scale it
    img = Image.open(in_file).convert('L')
    # resize the image
    img = img.resize((base_width, base_size), Image.ANTIALIAS)
    # get the pixel array
    pixel_Arr = np.array(img)
    # ASCII art
    ASCII = ['!', '|', '$', '%', '*', '+', ',', '-', '.', ':', ';', '?', '@', '^', 'o', 'x', '#']

    # assign each character to it corresponding pixel value
    f = open(out_file, 'w')
    for x in pixel_Arr:
        for y in x:
            f.write(ASCII[trunc(y/255*17) - 1])
        f.write('\n')
    # close file
    f.close()
    return True


# for convert picture to ASCII picture
def picToImage(in_file, out_file):
    # default size 167 x 100
    base_width = 167
    base_size = 100
    # open the image and grey scale it
    img = Image.open(in_file).convert('L')
    # resize the image
    img = img.resize((base_width, base_size), Image.ANTIALIAS)
    # get the pixel array
    pixel_Arr = np.array(img)
    # ASCII art
    ASCII = ['!', '|', '$', '%', '*', '+', ',', '-', '.', ':', ';', '?', '@', '^', 'o', 'x', '#']

    # create a temp txt file to strore the ASCII char
    temp = 'temp.txt'
    # assign each character to it corresponding pixel value
    f = open(temp, 'w')
    for x in pixel_Arr:
        for y in x:
            f.write(ASCII[trunc(y / 255 * 17) - 1])
        f.write('\n')
    # text size 3
    font = ImageFont.truetype('cour.ttf', 15)
    # default size 1280 x 1280
    img = Image.new('L', (1500, 1500), color=255)
    draw = ImageDraw.Draw(img)
    vertical_scale = 0
    with open(temp) as f:
        lines = f.readlines()

    for line in lines:
        draw.text((0, vertical_scale), line, fill=0, font=font)
        vertical_scale = vertical_scale + 15
    img.save(out_file)

    # close file
    f.close()
    os.remove(temp)
    return True


# note for ratio
# the width of the output gif will be the base_width of the frame * 2
# the size(height) of the output gif will be the same as the base_size of the frame
# however be careful with the size of the text and the vertical + horizontal scale

# detail mode
def getFrameDetail(in_file):
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
            yield imframe.convert('L').resize((500, 500), Image.ANTIALIAS)
            i = i + 1
    except EOFError:
        pass


def convertGifDetail(in_file, out_file):
    # default size 190 x 115
    base_width = 190
    base_size = 115
    # open the image and grey scale it
    img = Image.open(in_file).convert('L')
    # resize the image
    img = img.resize((base_width, base_size), Image.ANTIALIAS)
    # get the pixel array
    pixel_Arr = np.array(img)
    # ASCII art
    ASCII = ['!', '|', '$', '%', '*', '+', ',', '-', '.', ':', ';', '?', '@', '^', 'o', 'x', '#']

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
    # text size 3
    font = ImageFont.truetype('cour.ttf', 15)
    # default size 1700 x 1700
    img = Image.new('L', (1700, 1700), color=255)
    draw = ImageDraw.Draw(img)
    vertical_scale = 0
    with open(input_file) as f:
        lines = f.readlines()

    for line in lines:
        draw.text((0, vertical_scale), line, fill=0, font=font)
        vertical_scale = vertical_scale + 15
    img.save(output_file)


# simple mode
def getFrameSimple(in_file):
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
            yield imframe.convert('L').resize((300, 300), Image.ANTIALIAS)
            i = i + 1
    except EOFError:
        pass


def convertGifSimple(in_file, out_file):
    # default size 50 x 30
    base_width = 50
    base_size = 30
    # open the image and grey scale it
    img = Image.open(in_file).convert('L')
    # resize the image
    img = img.resize((base_width, base_size), Image.ANTIALIAS)
    # get the pixel array
    pixel_Arr = np.array(img)
    # ASCII art
    ASCII = ['!', '|', '$', '%', '*', '+', ',', '-', '.', ':', ';', '?', '@', '^', 'o', 'x', '#']

    # assign each character to it corresponding pixel value
    f = open(out_file, 'w')
    for x in pixel_Arr:
        for y in x:
            f.write(ASCII[trunc(y/255*8) - 1])
        f.write('\n')
    # close file
    f.close()
    return True


def textToImageSimple(input_file, output_file):
    # text size 10
    font = ImageFont.truetype('cour.ttf', 10)
    # default size 300 x 300
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
    list_file = natsorted(os.listdir(input_dir))
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


def webcamConvert():
    # for showing the ASCII
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('monospace', 15)
    size = (1000, 1000)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Output")

    # webcam input
    name = 'Input'
    cv2.namedWindow("Input", cv2.WINDOW_AUTOSIZE)
    vc = cv2.VideoCapture(0)

    cv2.startWindowThread()

    # get the first frame
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    # when we click x on the window, getWindowProperty will returns -1
    # use this so we could close the window after clicking x
    while cv2.getWindowProperty(name, 0) >= 0:
        # gray scale and how the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        arr = np.array(gray)
        # show the raw input
        cv2.imshow(name, gray)
        rval, frame = vc.read()

        output = ''
        # put the ASCII on screen
        text = font.render(output, False, BLACK)
        screen.fill(WHITE)
        # quit the pygame when the webcam is closed
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        screen.blit(text, (0, 0))
        pygame.display.flip()

        # press escape to quit the webcam
        key = cv2.waitKey(20)
        if key == 27:
            break

    vc.release()
    cv2.destroyWindow(name)


# webcamConvert()