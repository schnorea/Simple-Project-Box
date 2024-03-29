# Simple Project Box
OpenSCAD project to create 3d printed end caps for small project boxes that have sides made out of cardboard or other flat stock. The idea was to have the ability to create a low cost box quickly that reused materials that are readily available.

Updates:
 * It now generates a pdf file that holds the outline of the cardboard (or what ever sides).
 * Runs in Python3
 * Has a requirements.txt doc

 Requirements:
  * Python3
  * Pycairo - "pip install pycairo"
  * Openscad installed

The cardboard output dimensions still need to be tested and might require adjustment.

To use you need to have openSCAD on path and have python 2.7.xx with pycairo module installed (seems to be installed by default on Ubuntu and Raspibian).

The command line looks like this:
```
python makebox.py  200x100x48
```

This creates a box with outside dimensions of 200 x 100 x 48 millimeters.

The tool will maximize the use of cardboard and minimize the 3D printing to be done.

If the box is to large and it can't layout the either the sides or top and bottom on two seperat pages, the program will terminate with an Error. The end caps STLs will still be created. 
```
usage: makebox.py [-h] [--ct CT] [--sd SD] [--bt BT] dimensions

Make a box. This will create the STLs and SVG required to build a box in a
minimal 3D print fashion.

positional arguments:
  dimensions  Dimensions in the form of widthxdepthxheight (i.e. 5.2x3.6x9.12)

optional arguments:
  -h, --help  show this help message and exit
  --ct CT     Cardboard thickness
  --sd SD     Slot Depth
  --bt BT     Bracket Thickness
```

There are several improvements and features planned for the future.

![Example SimpleBox(s)](https://github.com/schnorea/SimpleBox/blob/master/assets/IMG_3207.jpg?raw=true "Example SimpleBox(s)")

