#!/usr/bin/env python3

# Source: https://github.com/O-X-L/python-opensimplex
# Copyright: Rath Pascal
# License: MIT

from sys import path as sys_path

from generate_map_base import BASE_PATH, _create_img, _profile

sys_path.append(str(BASE_PATH))

# pylint: disable=C0413
from opensimplex_cli import OpenSimplexConfig, OpenSimplexCLI

map_size = 1000
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

terrain_noise = OpenSimplexCLI(terrain_config)


def _generate(pos_x: float = 0, pos_y: float = 0) -> tuple[list[float], float]:
    print(f'Generating map.. {map_size}x{map_size}')
    return terrain_noise.get_2d_array(size=map_size, pos_x=pos_x, pos_y=pos_y)


def main():
    map_data, max_height = _generate()
    _create_img(size=map_size, map_data=map_data, max_height=max_height)


if __name__ == '__main__':
    print(_profile(main)[1])
