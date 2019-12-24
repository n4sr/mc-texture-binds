#!/usr/bin/env python3
import argparse
import logging
import os
import zipfile
from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance


def get_crop(char):
    n = ord(char)  #ord() is sick!
    x, y = (n%16)*8, int(n/16)*8
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
    keylist = get_keys(args.keys, ascii_png)

    for asset in guimap:
        x = int(guimap[asset][0]) + args.offset[0]
        y = int(guimap[asset][1]) + args.offset[1]
        position = x, y
        spacing = int(guimap[asset][2])
        new = overlay_binds(
            assets[asset],
            keylist,
            position,
            spacing,
            args.opacity
            )
        save_img(new, asset)


parser = argparse.ArgumentParser()
parser.add_argument(
    'keys',
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

try:
    run(args.keys, args.opacity, args.offset, args.version)
except Exception as ex:
    logging.error(f'{type(ex).__name__}: {ex}')