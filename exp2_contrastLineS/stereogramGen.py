#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
from PIL import Image, ImageDraw

to_dir = 'material'
os.makedirs(to_dir, exist_ok=True)

# Input RDS's size, caring be dividable
size = 200

# Input line size
line_height = 30 # 30pix is 42 min of arc on 57cm distance
line_width = 2

# Input the disparity at pixel units.
disparity = 4

# Input target size, which is quarter of RDS’s　size in default
#inner = int(size / 4)

# Input the quantity you need
#q = 5

# Input a number you like to initiate
s = 1

# Input luminance of background
lb = 215 # 215, 84%

# Input luminance of dots
based_l = 205 # Contrast with background is about 4%
# Here, the another luminance would vary
ld = [205, 195, 185, 165, 135] # Consequently, about 4, 8, 12, 16, 20, 32%


#ld.sort(reverse=True)

# Generate stereograms
for k in ld:

    # Two images prepair
    img = Image.new("L", (size, size), lb)
    draw = ImageDraw.Draw(img)

    img2 = Image.new("L", (size, size), lb)
    draw2 = ImageDraw.Draw(img2)

    # Fill the targets are
    draw.rectangle((int(size / 2) - int(line_width / 2) - disparity / 2, int(size / 2) + int(line_height / 2),
                    int(size / 2) + int(line_width / 2) - disparity / 2, int(size / 2) - int(line_height / 2)),
                   fill=based_l, outline=None)
    draw2.rectangle((int(size / 2) - int(line_width / 2) + disparity / 2, int(size / 2) + int(line_height / 2),
                     int(size / 2) + int(line_width / 2) + disparity / 2, int(size / 2) - int(line_height / 2)),
                    fill=k, outline=None)

#    img_resize = img.resize((int(img.width*2), int(img.height*2)))
#    img2_resize = img2.resize((int(img2.width*2), int(img2.height*2)))

    # Write images
    basenameR = os.path.basename('rds' + str(s) + 'R.jpg')
    basenameL = os.path.basename('rds' + str(s) + 'L.jpg')
    img.save(os.path.join(to_dir, basenameR), quality=100)
    img2.save(os.path.join(to_dir, basenameL), quality=100)
    s += 1