#!/usr/bin/env python3
import argparse
import pathlib
import re
import zipfile

from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance

from .guimap import guimap


def main():
    parser = argparse.ArgumentParser(prog='texture-binds')
    parser.add_argument(
        'jar',
        metavar='minecraft.jar',
        type=pathlib.Path,
    )
    parser.add_argument(
        'opt',
        metavar='options.txt',
        type=pathlib.Path,
    )
    parser.add_argument(
        '--offset',
        nargs=2,
        type=int,
        metavar=('x','y'),
        default=[1,1],
    )
    parser.add_argument(
        '--opacity',
        type=float,
        metavar='float',
        default=1.0,
    )
    args = parser.parse_args()

    x2, y2 = args.offset
    ascii_png = get_asset(args.jar, 'assets/minecraft/textures/font/ascii.png')
    keys = get_keys_from_file(args.opt)

    for key in keys:
        key.get_keyimg(ascii_png)

    for asset in guimap:
        gui = get_asset(args.jar, asset)
        x1, y1, spacing = guimap[asset]
        gui = overlay(gui, keys, x1+x2, y1+y2, spacing, args.opacity)
        gui.save(asset)


def overlay(gui, keys, x, y, spacing, opacity):
    screen = Image.new('RGBA', gui.size)
    for key in keys:
        pos = x+(key.slot-1)*spacing, y
        screen.paste(key.keyimg, pos, key.keyimg)
    screen = ImageEnhance.Brightness(screen).enhance(opacity)
    gui = ImageChops.screen(gui, screen)
    return gui


def get_asset(jarpath, asset):
    with zipfile.ZipFile(jarpath) as jar:
        img = jar.open(asset, 'r')
    return Image.open(img).convert('RGBA')


def get_keys_from_file(options_txt):
    keylist = list()
    pattern = r'key_key\.hotbar\.([1-9]):key\.(keyboard|mouse)\.([\w])'
    pattern = re.compile(pattern)
    with options_txt.open('r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                keylist.append(Key(int(match.group(1)),
                               match.group(2), match.group(3)))
    return sorted(keylist, key=lambda key: key.slot)


class Key:
    def __init__(self, slot, device, key):
        self.slot = slot
        self.device = device
        self.key = key
        self.keystring = self._get_keystring()
        self.keyimg = None

    def _get_crop(self, char):
        '''
        Returns the coordinates of the key on the ascii sprite sheet.
        '''
        k = ord(char)
        x = k %  16 * 8
        y = k // 16 * 8
        return x, y, x+5, y+8

    def _get_keystring(self):
        '''Returns a string of the key formatted for the hotbar.'''
        s = str()
        if not self.device == 'keyboard': s += self.device[0]
        s += self.key
        return s

    def get_keyimg(self, ascii_png):
        bg = Image.new('1', (len(self.keystring)*6-1, 8))
        for n, char in enumerate(self.keystring):
            pos = (n*6, 0)
            key = ascii_png.copy().crop(self._get_crop(char))
            bg.paste(key, pos, key)
        self.keyimg = bg


if __name__ == '__main__':
    main()