# mc-texture-binds
`texture-binds.py` is a script that generates a resourcepack which
overlays your onto the various inventory textures in Minecraft. This
could be useful for players who have non-standard keybinds for their
hotbar.

![](screenshots/example1.png)

# Usage
```
usage: texture-binds.py [-h] [--offset x y] [--opacity float]
                     /.minecraft

positional arguments:
  .minecraft directory

optional arguments:
  -h, --help       show this help message and exit
  --offset x y
  --opacity float
```
```
$ python texture-binds.py --offset 1 1 --opacity .5 ~/.minecraft
```
