#!/usr/bin/env python3
import csv
import logging
import os
import zipfile
from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance


minecraftjar = os.path.expanduser('~/.minecraft/versions/1.15/1.15.jar')
keybinds = ('Q','E','R','F','C','V','B','m4','m5')
opacity = 0.5
offset = (1,1)


def get_crop(p):
    return p[0], p[1], p[0]+5, p[1]+7


def get_map(file):
    d = {}

    with open(file, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split(' ')
            d[line[0]] = line[1:]

    return d


def get_assets(filelist, jarpath):
    d = {}

    with zipfile.ZipFile(jarpath, 'r') as jar:
        for i in filelist:
            asset = jar.open(i)
            d[i] = Image.open(asset).convert('RGBA')

    return d


def get_charset(sheet):
    a = []
    sheet = sheet.copy().convert('1')

    for y in range(int(128/8)):
        for x in range(int(128/8)):
            pos = x*8, y*8
            char = sheet.copy().crop(get_crop(pos))
            a.append(char)

    return a


def get_keys(keybinds, charset):
    a = []

    for key in keybinds:
        key_img = Image.new('1', (len(key)*6-1, 7))

        for n, char in enumerate(key):
            key_img.paste(charset[ord(char)], (n*6,0))  #ord() is sick!

        a.append(key_img.copy())

    return a


def overlay_binds(gui, keylist, position, spacing, opacity):
    bg = Image.new('RGBA', gui.size)
    x, y = position

    for n, key in enumerate(keylist):
        bg.paste(key, (x+n*spacing, y), key)

    opa = ImageEnhance.Brightness(bg).enhance(opacity)
    return ImageChops.screen(gui, opa)


def save_img(img, dest):
    folder = os.path.split(dest)[0]

    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    img.save(dest)


guimap = get_map('guimap')

filelist = [f for f in guimap]
filelist.append('assets/minecraft/textures/font/ascii.png')

assets = get_assets(filelist, minecraftjar)

ascii_png = assets['assets/minecraft/textures/font/ascii.png']

charset = get_charset(ascii_png)

keylist = get_keys(keybinds, charset)

for asset in guimap:
    x = int(guimap[asset][0]) + offset[0]
    y = int(guimap[asset][1]) + offset[1]
    position = x, y
    spacing = int(guimap[asset][2])
    new = overlay_binds(assets[asset], keylist, position, spacing, opacity)
    save_img(new, asset)