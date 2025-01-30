#!/usr/bin/env python3

# Source: https://github.com/O-X-L/opensimplex
# Copyright: Rath Pascal
# License: MIT

# pylint: disable=R0801

from time import time
from sys import path as sys_path

from generate_map_base import BASE_PATH, _create_img, _profile

sys_path.append(str(BASE_PATH))

# pylint: disable=C0413
from opensimplex_cgo import OpenSimplexExtended, OpenSimplexConfig


map_size = 50
pos_x = 0
pos_y = 0

terrain_config = OpenSimplexConfig(
    octaves=10,
    persistence=0.7,
    lacunarity=1.5,
    exponentiation=5.0,
    height=135.0,
    scale=50,
    seed=3498230422,
)

terrain_noise = OpenSimplexExtended(terrain_config)
area = map_size * map_size
start_time = int(time())


def _generate() -> dict:
    print(f'Generating map.. {map_size}x{map_size}')
    d = []
    mx, mi, idx = 0, 10000, 0

    for x in range(0, map_size):
        for y in range(0, map_size):
            if idx != 0 and idx % 1_000 == 0:
                print(f'Status: {round((100 / area) * idx, 0)}% ({int(time())-start_time}s)')

            xa, ya = x + pos_x, y + pos_y
            h = terrain_noise.get_2d(xa, ya)
            d.extend([xa, ya, h])
            mx = max(mx, h)
            mi = min(mi, h)
            idx += 1

    return {'data': d, 'max': mx, 'min': mi}


def main():
    noise = _generate()
    _create_img(size=map_size, map_data=noise['data'], max_height=noise['max'])


if __name__ == '__main__':
    print(_profile(main)[1])
