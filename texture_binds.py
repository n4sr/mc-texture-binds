#!/usr/bin/env python3
import argparse
import logging
import os
import re
import zipfile
from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance


def get_crop(char):
    n = ord(char)  #ord() is sick!
    x = (n%16)*8
    y = int(n/16)*8
    return x, y, x+5, y+7


def get_guimap():
    d = {}
    with open('guimap', 'r') as f:
        for line in f:
            line = line.rstrip('\n').split(' ')
            d[line[0]] = line[1:]
    return d


def get_assets(filelist, jarpath):
    d = {}
    with zipfile.ZipFile(jarpath, 'r') as jar:
        for asset in filelist:
            i = jar.open(asset)
            d[asset] = Image.open(i).convert('RGBA')
    return d


def get_keys(keybinds, sheet):
    a = []
    for key in keybinds:
        key_img = Image.new('1', (len(key)*6-1, 7))
        for n, char in enumerate(key):
            char_img = sheet.copy().crop(get_crop(char))
            key_img.paste(char_img, (n*6,0))
        a.append(key_img.copy())
    return a


def get_keybinds_from_file(file):
    a = []
    pattern = r'key_key\.hotbar\.([1-9]):key\.(keyboard|mouse)\.([\w])'
    pattern = re.compile(pattern)
    with open(file) as f:
        for row in f:
            row = row.rstrip('\n')
            match = pattern.match(row)
            if not match == None:
                n = int(match.group(1))
                device = match.group(2)
                key = match.group(3)
                a.insert(n, format_key(device, key))
    return a


def format_key(dev, key):
    if dev == 'mouse':
        return 'm' + key
    else:
        return key.upper()


def overlay_binds(gui, keylist, position, spacing, opacity):
    bg = Image.new('RGBA', gui.size)
    x, y = position
    for n, key in enumerate(keylist):
        bg.paste(key, (x+n*spacing, y), key)
    brightness = ImageEnhance.Brightness(bg).enhance(opacity)
    return ImageChops.screen(gui, brightness)


def save_img(img, dest):
    folder = os.path.split(dest)[0]
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)
    img.save(dest)


def get_jar(ver):
    jar = os.path.expanduser(f'~/.minecraft/versions/{ver}/{ver}.jar')
    if os.path.exists(jar):
        return jar
    else:
        raise FileNotFoundError(jar)


def run(keybinds, opacity, offset, version):
    jar = get_jar(version[0])
    guimap = get_guimap()
    filelist = [f for f in guimap]
    filelist += ['assets/minecraft/textures/font/ascii.png']
    assets = get_assets(filelist, jar)
    ascii_png = assets['assets/minecraft/textures/font/ascii.png']
    keylist = get_keys(keybinds, ascii_png)

    for asset in guimap:
        x = int(guimap[asset][0]) + offset[0]
        y = int(guimap[asset][1]) + offset[1]
        position = x, y
        spacing = int(guimap[asset][2])
        new = overlay_binds(
            assets[asset],
            keylist,
            position,
            spacing,
            opacity[0]
            )
        save_img(new, asset)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-f',
    dest='file',
    metavar='options.txt'
)
group.add_argument(
    '-k',
    dest='keys',
    nargs=9,
    type=str,
    metavar='KEY'
)
parser.add_argument(
    '--opacity',
    nargs=1,
    type=float,
    default=1,
    help='set the opacity of the labels',
    metavar='float'
)
parser.add_argument(
    '--offset',
    nargs=2,
    type=int,
    default=[1,1],
    help='how offset the labels are from the corner',
    metavar='int'
)
parser.add_argument(
    '--version',
    nargs=1,
    type=str,
    default='1.15.1',
    metavar='MINECRAFT_VERSION'
)
args = parser.parse_args()

if args.file:
    keys = get_keybinds_from_file(args.file)
else:
    keys = args.keys

run(keys, args.opacity, args.offset, args.version)
