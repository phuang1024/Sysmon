from colorsys import hsv_to_rgb
from random import Random

import numpy as np

random = Random(71)
colors = []
for i in range(100):
    h = random.uniform(0, 1)
    s = random.uniform(0.5, 1)
    color = np.array(hsv_to_rgb(h, s, 1)) * 255
    colors.append(color)


def random_color(i):
    """
    Stable random color generator
    """
    return colors[i % len(colors)]
