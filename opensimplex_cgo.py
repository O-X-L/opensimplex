from random import randint
from pathlib import Path
from ctypes import cdll, c_int64, c_float

# pylint: disable=R0801

BASE_PATH = Path(__file__).parent.resolve()

__opensimplex = cdll.LoadLibrary(f'{BASE_PATH}/noise_cgo.so')

_noise_set_seed = __opensimplex.set_seed
_noise_set_seed.argtypes = [c_int64]

_noise_2d = __opensimplex.get_2d
_noise_2d.argtypes = [c_float, c_float]
_noise_2d.restype = c_float

_noise_3d = __opensimplex.get_3d
_noise_3d.argtypes = [c_float, c_float, c_float]
_noise_3d.restype = c_float

_noise_4d = __opensimplex.get_4d
_noise_4d.argtypes = [c_float, c_float, c_float, c_float]
_noise_4d.restype = c_float


class OpenSimplex:
    def __init__(self, seed: int = None):
        if seed is None:
            self.seed = randint(0, 100_000_000)

        else:
            self.seed = seed

        _noise_set_seed(c_int64(self.seed))

    @staticmethod
    def _abs(n: float) -> float:
        if n < 0:
            return n * -1

        return n

    def get_2d(self, x: float, y: float) -> float:
        return self._abs(_noise_2d(
            c_float(x),
            c_float(y),
        ))

    def get_3d(self, x: float, y: float, z: float) -> float:
        return self._abs(_noise_3d(
            c_float(x),
            c_float(y),
            c_float(z),
        ))

    def get_4d(self, x: float, y: float, z: float, w: float) -> float:
        return self._abs(_noise_4d(
            c_float(x),
            c_float(y),
            c_float(z),
            c_float(w),
        ))


class OpenSimplexConfig:
    def __init__(
        self, seed: int = None, octaves: int = 5, persistence: float = 0.0, lacunarity: float = 0.0,
        exponentiation: float = 1.0, height: float = 1.0, scale: float = 1.0,
    ):
        self.seed = seed
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.exponentiation = exponentiation
        self.height = height
        self.scale = scale


class OpenSimplexExtended:
    A = 0.5

    def __init__(self, config: OpenSimplexConfig):
        self.cnf = config
        self._noise = OpenSimplex(seed=self.cnf.seed)

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
                noise_value = self._noise.get_4d(
                    xs * frequency,
                    ys * frequency,
                    zs * frequency,
                    ws * frequency,
                )

            elif d == 3:
                noise_value = self._noise.get_3d(
                    xs * frequency,
                    ys * frequency,
                    zs * frequency,
                )

            else:
                noise_value = self._noise.get_2d(
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
