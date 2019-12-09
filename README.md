# What is this for?
This script batch edits your inventory textures to add keybind labels to them.
This could be useful if you use non-standard keybinds for your hotbar, 
and would like a reminder as to which key is bound to what.

# How to use
First, we need to create the assets:
* Create `pack/` folder.
* Copy the `assets/` folder from the current texture pack, and place it into `pack/`.
* Open `pack/assets/minecraft/textures/font/ascii.png` in your favorite image editor, and crop out the characters you would like to use, save them as `keys/<key>.png`. (Note: you should save them as 1-bit indexed color, otherwise the characters may render incorrectly.)

Then, configure the script:
* Open  `main.py` in your favorite text editor.
* Modify lines 9, 10, and 11 to your liking.

And, finally:
* Run `main.py`

# Known issues
* Incompatible with non-standard resolution resource packs.