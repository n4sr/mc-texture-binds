#!/usr/bin/env python3
import os
import re
import zipfile

from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance

from .guimap import guimap

def get_assets(jarpath):
    d = {}
    filelist = [f for f in guimap]
    filelist += ['assets/minecraft/textures/font/ascii.png']
    with zipfile.ZipFile(jarpath, 'r') as jar:
        for file in filelist:
            x = jar.open(file, 'r')
            d[file] = Image.open(x).convert('RGBA')
    return d

def get_keys_from_file(options_txt):
    a = []
    pattern = r'key_key\.hotbar\.([1-9]):key\.(keyboard|mouse)\.([\w])'
    pattern = re.compile(pattern)
    with open(options_txt, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                n = int(match.group(1))
                device = match.group(2)
                key = match.group(3)
                a.append((n-1, format_key(device, key)))
    return a

def format_key(dev, key):
    if dev == 'mouse':
        return 'm' + key
    else:
        return key.upper()

def get_keys_from_list(keys):
    return [x for x in enumerate(keys)]

def get_crop(char):
    n = ord(char)
    x = n%16*8
    y = int(n/16)*8
    return x, y, x+5, y+7

def get_key_imgs(keys, sheet):
    a = []
    for n, key in keys:
        keysize = (len(key) * 6 - 1, 7)
        key_img = Image.new('1', keysize)
        for i, char in enumerate(key):
            pos = (i * 6, 0)
            char_img = sheet.copy().crop(get_crop(char))
            key_img.paste(char_img, pos)
        a.append((n, key_img.copy()))
    return a

def overlay_binds(gui, key_imgs, position, spacing, opacity):
    bg = Image.new('RGBA', gui.size)
    x, y = position
    for n, key in key_imgs:
        pos = (x + n * spacing, y)
        bg.paste(key, pos, key)
    brightness = ImageEnhance.Brightness(bg).enhance(opacity)
    return ImageChops.screen(gui, brightness)

def save_img(img, dest):
    folder = os.path.split(dest)[0]
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)
    img.save(dest)

def run(args):
    assets = get_assets(args.jar[0])
    ascii_png = assets['assets/minecraft/textures/font/ascii.png']
    offsetx, offsety = args.offset

    if args.file:
        keys = get_keys_from_file(args.file[0])
    else:
        keys = get_keys_from_list(args.keys)

    key_imgs = get_key_imgs(keys, ascii_png)

    for f in guimap:
        x, y, spacing = guimap[f]
        pos = x + offsetx, y + offsety
        gui = assets[f]
        overlay = overlay_binds(
            gui,
            key_imgs,
            pos,
            spacing,
            args.opacity[0]
        )
        save_img(overlay, f)
