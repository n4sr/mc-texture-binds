# mc-texture-binds
`texture-binds` is a script that generates a resourcepack which
overlays your onto the various inventory textures in Minecraft. This
could be useful for players who have non-standard keybinds for their
hotbar. Just clone the repo folder into your
`.minecraft/resourcepacks/` folder and run the script.

![](screenshots/example1.png)

# Usage
```
usage: texture-binds [-h] [--offset x y] [--opacity float]
                     minecraft.jar options.txt

positional arguments:
  minecraft.jar
  options.txt

optional arguments:
  -h, --help       show this help message and exit
  --offset x y
  --opacity float
```
```
$ python3 -m texture-binds --offset 1 1 --opacity .5 ~/.minecraft/versions/1.15.1/1.15.1.jar ~/.minecraft/options.txt
```

# Requirements
* Python 3.6 or greater
* [Pillow](https://python-pillow.org/) from `pip`
