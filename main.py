#!/usr/bin/env python3
import csv
import os
from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance


keys = ('q','e','r','f','c','v','b','mouse4','mouse5')
opacity = 0.5
offset = (1,1)


def construct_binds(keys, opacity=1, spacing=18):
    keys_enum = enumerate(keys)
    width = len(keys) * spacing
    background = Image.new('RGBA', (width, 7))  #char height

    for n, key in keys_enum:
        pos = n * spacing, 0
        key_img = Image.open(f'keys/{key.lower()}.png').convert('1')
        background.paste(key_img, pos)

    return ImageEnhance.Brightness(background).enhance(opacity)


def overlay_binds(gui, binds, position):
    overlay = Image.new('RGBA', gui.size)
    overlay.paste(binds, position)
    return ImageChops.screen(gui, overlay)


def save_img(img, dest):
    folder = os.path.split(dest)[0]
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)
    img.save(dest)


with open('offsets.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)

    for filename, x, y, spacing in reader:
        offset_x, offset_y = offset
        position = (int(x) + offset_x, int(y) + offset_y)
        gui = Image.open(f'pack/{filename}').convert(mode='RGBA')
        binds = construct_binds(keys, opacity=opacity, spacing=int(spacing))
        new_gui = overlay_binds(gui, binds, position)
        save_img(new_gui, filename)
