#!/usr/bin/env python3

# Source: https://github.com/O-X-L/python-opensimplex
# Copyright: Rath Pascal
# License: MIT

from pathlib import Path
from cProfile import Profile
from io import StringIO
from pstats import Stats
from typing import Callable, Any

import numpy as np
from PIL import Image

EXAMPLE_PATH = Path(__file__).parent.resolve()
BASE_PATH = EXAMPLE_PATH.parent.resolve()

COLOR_DEEPWATER = (0, 62, 178)
COLOR_WATER = (9, 82, 198)
COLOR_SAND = (254, 224, 179)
COLOR_GRASS = (9, 120, 93)
COLOR_DARKGRASS = (10, 107, 72)
COLOR_DARKESTGRASS = (11, 94, 51)
COLOR_DARKROCKS = (140, 142, 123)
COLOR_ROCKS = (160, 162, 143)
COLOR_BLACKROCKS = (53, 54, 68)
COLOR_SNOW = (255, 255, 255)


# pylint: disable=R0911
def _get_color(height: float, max_height: float):
    factor = 255 / max_height
    h = height * factor

    h = min(max(h, 0), 255)

    if h <= 0.5:
        return COLOR_DEEPWATER
    if h <= 1.2:
        return COLOR_WATER
    if h <= 2:
        return COLOR_SAND
    if h <= 18:
        return COLOR_GRASS
    if h <= 30:
        return COLOR_DARKGRASS
    if h <= 60:
        return COLOR_DARKESTGRASS
    if h <= 125:
        return COLOR_DARKROCKS
    if h <= 145:
        return COLOR_ROCKS
    if h <= 220:
        return COLOR_BLACKROCKS

    return COLOR_SNOW


def _create_img(size: int, map_data: list[float], max_height: float):
    out_img = f"{EXAMPLE_PATH}/map.png"
    print(f'Saving to image: {out_img}')
    colour_map = np.zeros((size, size, 3), dtype=np.uint8)

    for i in range(size * size):
        xi, yi, hi = i * 3, i * 3 + 1, i * 3 + 2
        colour_map[map_data[xi], map_data[yi]] = _get_color(map_data[hi], max_height)

    image = Image.fromarray(colour_map, 'RGB')
    image.save(out_img)
    return image


def _profile(
        target: Callable, args: list = None, kwargs: dict = None,
        lines: int = 20, sort: str = 'tottime'
) -> tuple[Any, str]:
    if args is None or not isinstance(args, list):
        args = []

    if kwargs is None or not isinstance(kwargs, dict):
        kwargs = {}

    p = Profile()
    p.enable()

    output = target(*args, **kwargs)

    p.disable()

    s = StringIO()
    ps = Stats(p, stream=s).sort_stats(sort)
    ps.print_stats(lines)
    return output, s.getvalue()
