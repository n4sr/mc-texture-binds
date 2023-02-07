#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import zipfile
import io
from string import ascii_letters, digits

from packaging.version import parse as ParseVersion
from packaging.version import Version
from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance


class HotBar:
    def __init__(self):
        self.slots = {i: None for i in range(1, 10)}

    def bind(self, slot, key):
        if not isinstance(slot, int):
            raise TypeError
        if not slot in range(1, 10):
            raise ValueError
        if not isinstance(key, str):
            raise TypeError
        if not len(key) in range(1, 3):
            raise ValueError
        for char in key:
            if not char in ascii_letters + digits:
                raise ValueError
        self.slots[slot] = key

    def slot(self, n):
        return self.slots[n]


class Asset:
    def __init__(self, obj, data):
        if not isinstance(obj['path'], str):
            raise TypeError
        if not isinstance(obj['spacing'], int):
            raise TypeError
        if not isinstance(obj['x'], int):
            raise TypeError
        if not isinstance(obj['y'], int):
            raise TypeError
        if not isinstance(data, io.BytesIO):
            raise TypeError
        self.path = obj['path']
        self.spacing = obj['spacing']
        self.x = obj['x']
        self.y = obj['y']
        self.data = data


parser = argparse.ArgumentParser(prog='texture-binds')
parser.add_argument('path', metavar='.minecraft folder', type=pathlib.Path)
parser.add_argument('--offset', nargs=2, type=int,
                    metavar=('x', 'y'), default=[1, 1])
parser.add_argument('--opacity', type=float, metavar='float', default=0.5)
args = parser.parse_args()


PACKMCMETA = json.dumps({
    "pack": {
        "pack_format": 12,
        "description": "Your keybinds embedded on inventory GUI and HUD."
    }
}, sort_keys=True, indent=4)

with pathlib.Path(__file__).with_name('assets.json').open('r') as f:
    ASSETS_JSON = json.load(f)

if not args.path.is_dir():
    raise NotADirectoryError(args.path)

OPTIONS_PATH = args.path.joinpath('options.txt')
if not OPTIONS_PATH.is_file():
    raise FileNotFoundError(OPTIONS_PATH)

RESOURCEPACK_PATH = args.path.joinpath('resourcepacks/texture-binds.zip')
if not RESOURCEPACK_PATH.parent.is_dir():
    raise NotADirectoryError(RESOURCEPACK_PATH)

# find all the jar files in versions, compare them, and use
# the latest version. this will likely break with snapshot jars.
# TODO: add exceptions for snapshot versions.
JAR_PATH = None
for jar in args.path.glob('versions/**/*.jar'):
    if (JAR_PATH is None
            or ParseVersion(jar.stem) > ParseVersion(JAR_PATH.stem)):
        JAR_PATH = jar

if JAR_PATH is None:
    raise FileNotFoundError


ASSETS = []
with zipfile.ZipFile(JAR_PATH) as jar:
    for asset in ASSETS_JSON:
        ASSETS.append(
            Asset(asset, io.BytesIO(jar.open(asset['path'], 'r').read())))

    ASCII_PNG = io.BytesIO(
        jar.open('assets/minecraft/textures/font/ascii.png', 'r').read())


hotbar = HotBar()

with OPTIONS_PATH.open('r') as f:
    pattern = re.compile(
        r'key_key\.hotbar\.([1-9]):key\.(keyboard|mouse)\.([\w])')
    for match in re.finditer(pattern, f.read()):
        slot = int(match.group(1))
        device = match.group(2)
        key = match.group(3)
        if device == 'mouse':
            key = 'm' + key
        hotbar.bind(slot, key)


# ascii sheet is 128x128, each tile is 8x8, character size is 5x8.
# sheet / tile size = 16, therefore 16 columns, 16 rows.
# most characters only take up 5x7, however the characters p and q
# render slightly lower than the others, so 5x8 is used.
ASCII_SPRITES = {}
sheet = Image.open(ASCII_PNG)
for char in ascii_letters + digits:
    n = ord(char)
    x1 = (n % 16) * 8
    y1 = (n // 16) * 8
    x2 = x1 + 5
    y2 = y1 + 8
    ASCII_SPRITES[char] = sheet.copy().crop((x1, y1, x2, y2))

RESOURCEPACK_ZIP = io.BytesIO()
with zipfile.ZipFile(RESOURCEPACK_ZIP, 'w') as zip:
    with zip.open('pack.mcmeta', 'w') as f:
        f.write(PACKMCMETA.encode())

    for asset in ASSETS:
        modified_asset = io.BytesIO()
        texture = Image.open(asset.data).convert('RGBA')
        key_overlay = Image.new('RGBA', texture.size)

        for slot, key in hotbar.slots.items():
            position = (asset.x + args.offset[0] + (slot - 1) * asset.spacing,
                        asset.y + args.offset[1])
            key_overlay.paste(ASCII_SPRITES[key], position, ASCII_SPRITES[key])

        ImageChops.screen(texture, ImageEnhance.Brightness(
            key_overlay).enhance(args.opacity)).save(modified_asset, 'png')

        with zip.open(asset.path, 'w') as f:
            f.write(modified_asset.getvalue())

with RESOURCEPACK_PATH.open('wb') as f:
    f.write(RESOURCEPACK_ZIP.getvalue())
