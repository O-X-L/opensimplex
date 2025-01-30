#!/usr/bin/env python3

# Source: https://github.com/O-X-L/opensimplex
# Copyright: Rath Pascal
# License: MIT

# pylint: disable=R0801

# this script is used to compare performance to the full python3 implementation: https://pypi.org/project/opensimplex/
# requirements: pip install opensimplex

from time import time
from sys import path as sys_path

import opensimplex

from generate_map_base import BASE_PATH, _create_img, _profile

sys_path.append(str(BASE_PATH))

# pylint: disable=C0413
from opensimplex_cgo import OpenSimplexConfig


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


class OpenSimplexExtended:
    A = 0.5

    def __init__(self, config: OpenSimplexConfig):
        self.cnf = config
        opensimplex.seed(config.seed)

    def get_2d(self, x: float, y: float) -> float:
        return self._get(x, y)

    def get_3d(self, x: float, y: float, z: float) -> float:
        return self._get(x, y, z)

    def get_4d(self, x: float, y: float, z: float, w: float) -> float:
        return self._get(x, y, z, w)

    # based on: https://github.com/simondevyoutube/ProceduralTerrain_Part10/blob/main/src/noise.js#L15
    def _get(self, x: float, y: float, z: float = None, w: float = None) -> float:
        d = 2
        xs = x / self.cnf.scale
        ys = y / self.cnf.scale
        zs = 0
        ws = 0
        if z is not None:
            d = 3
            zs = z / self.cnf.scale

        if w is not None:
            d = 4
            ws = w / self.cnf.scale

        g = 2.0 ** (-self.cnf.persistence)
        amplitude = 1.0
        frequency = 1.0
        normalization = 0
        total = 0

        for _ in range(self.cnf.octaves):
            if d == 4:
                noise_value = opensimplex.noise4(
                    xs * frequency,
                    ys * frequency,
                    zs * frequency,
                    ws * frequency,
                )

            elif d == 3:
                noise_value = opensimplex.noise3(
                    xs * frequency,
                    ys * frequency,
                    zs * frequency,
                )

            else:
                noise_value = opensimplex.noise2(
                    xs * frequency,
                    ys * frequency,
                )

            noise_value = noise_value * self.A + self.A

            total += noise_value * amplitude
            normalization += amplitude
            amplitude *= g
            frequency *= self.cnf.lacunarity

        total /= normalization
        if total < 0:
            total *= -1

        return float(total ** self.cnf.exponentiation) * self.cnf.height


terrain_noise = OpenSimplexExtended(terrain_config)
area = map_size * map_size
start_time = int(time())


def _generate() -> dict:
    print(f'Generating map.. {map_size}x{map_size}')
    d = []
    mx, mi, idx = 0, 10000, 0

    for x in range(0, map_size):
        for y in range(0, map_size):
            if idx != 0 and idx % 10_000 == 0:
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
