#!/usr/bin/env python3
import csv
import os
from PIL import Image
from PIL import ImageChops


keys = ('q','e','r','f','x','c','v','mouse4','mouse5')
opacity = 0.5
offset = (1,1)


def set_pixel_level(pixel, m):
    r, g, b, a = pixel

    if a == 0:
        return (0, 0, 0, 0)
    else:
        return (round(r*m), round(g*m), round(b*m), a)


def set_image_brightness(img, multiplier):
    img_w, img_h = img.size

    for x in range(img_w):
        for y in range(img_h):
            pos = (x,y)
            img.putpixel(pos, set_pixel_level(img.getpixel(pos), multiplier))


def construct_binds(keys, opacity=1):
    spacing = 18  #spacing between inventory slots
    keys_enum = enumerate(keys)
    width = len(keys) * spacing
    background = Image.new('RGBA', (width, 7))  #char height

    for n, key in keys_enum:
        img = Image.open(f'data/keys/{key.lower()}.png')
        background.paste(img, (n * spacing, 0))

    set_image_brightness(background, opacity)
    return background


def overlay_binds(binds, offset=(0,0)):
    offset_x, offset_y = offset

    with open('config.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for line in reader:
            filename, x, y = line
            pos = (int(x) + offset_x, int(y) + offset_y)
            gui = Image.open(f'data/{filename}').convert(mode='RGBA')
            overlay = Image.new('RGBA', gui.size)
            overlay.paste(binds, pos)
            output = ImageChops.screen(gui, overlay)
            save_img(output, filename)


def save_img(img, dest):
    folder = os.path.split(dest)[0]
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)
    img.save(dest)


#binds_img = construct_binds(keys, opacity=opacity)
overlay_binds(construct_binds(keys, opacity=opacity), offset=offset)
