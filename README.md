# mc-texture-binds
`texture-binds` is a script for overlaying keybinds onto the various 
inventory textures in Minecraft. This could be useful for players who have 
non-standard keybinds for their hotbar. Just clone the repo folder into 
your `.minecraft/resourcepacks/` folder and run the script.

![](screenshots/example1.png)


# Usage
```
usage: __main__.py [-h]
                   [-f options.txt | -k KEYS KEYS KEYS KEYS KEYS KEYS KEYS KEYS KEYS]
                   [--offset int int] [--opacity float]
                   jar

```
An example:
```
$ python3 -m texture-binds -f ~/.minecraft/options.txt --offset 1 1 --opacity 0.5 ~/.minecraft/version/1.15.1/1.15.1.jar
```
# Requirements
* Python>=3.6
* [Pillow](https://python-pillow.org/) from `pip`
