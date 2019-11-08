#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
from PIL import Image, ImageDraw

to_dir = 'material'
os.makedirs(to_dir, exist_ok=True)

# Input RDS's size, caring be dividable
size = 100

# Input the disparity at pixel units.
disparity = 4

# Input target size, which is quarter of RDS’s　size in default
inner = int(size / 4)

# Input the quantity you need
q = 5

# Input a number you like to initiate
s = 0

# Input luminance of background
lb = 215 # 215, 84%

# Input luminance of dots
based_l = 205 # Contrast with background is about 4%
# Here, the another luminance would vary
#ld = [250, 240, 229, 219, 209, 199] * q # Consequently, about 2, 6, 10, 14, 18, 22%
#ld = [245, 235, 224, 214, 204]
ld = [185, 165] # Consequently, about 4, 8, 12, 16, 20, 32%
#ld = [205, 185, 135]


ld.sort(reverse=True)

# Generate RDSs
for k in ld:

    # Two images prepair
    img = Image.new("L", (size, size), lb)
    draw = ImageDraw.Draw(img)

    img2 = Image.new("L", (size, size), lb)
    draw2 = ImageDraw.Draw(img2)

    # Draw the planes of RDSs
    for i in range(0, size):
        for j in range(1, size + 1):
            x = np.round(np.random.binomial(1, 0.5, 1)) * (j)
            draw.point((x - 1, i), fill=(based_l))
            draw2.point((x - 1, i), fill=(k))

    # Fill the targets area
    draw.rectangle((int(size / 2) - int(inner / 2) - disparity / 2, int(size / 2) + int(inner / 2),
                    int(size / 2) + int(inner / 2) - disparity / 2, int(size / 2) - int(inner / 2)), fill=lb,
                   outline=None)
    draw2.rectangle((int(size / 2) - int(inner / 2) + disparity / 2, int(size / 2) + int(inner / 2),
                     int(size / 2) + int(inner / 2) + disparity / 2, int(size / 2) - int(inner / 2)), fill=lb,
                    outline=None)

    # Drawing the targets
    for i in range(0, inner + 1):
        for j in range(0, inner + 1):
            x = np.round(np.random.binomial(1, 0.5, 1)) * (1 + j)
            if x != 0:
                draw.point((x + ((size / 2) - (inner / 2)) - 1 - disparity / 2, i + (size / 2) - (inner / 2)), fill=based_l)
                draw2.point((x + (size / 2) - (inner / 2) - 1 + disparity / 2, i + (size / 2) - (inner / 2)), fill = k)

    img_resize = img.resize((int(img.width*2), int(img.height*2)))
    img2_resize = img2.resize((int(img2.width*2), int(img2.height*2)))

    # Write images
    basenameR = os.path.basename('rds' + str(s) + 'R.jpg')
    basenameL = os.path.basename('rds' + str(s) + 'L.jpg')
    img_resize.save(os.path.join(to_dir, basenameR), quality=100)
    img2_resize.save(os.path.join(to_dir, basenameL), quality=100)
    s += 1