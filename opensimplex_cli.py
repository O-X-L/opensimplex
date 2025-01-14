from time import time
from pathlib import Path
from random import randint
from os import system as shell
from os import remove as remove_file
from json import loads as json_loads

# pylint: disable=R0801

BASE_PATH = Path(__file__).parent.resolve()


class OpenSimplexConfig:
    def __init__(
        self, seed: int = None, octaves: int = 10, persistence: float = 0.7, lacunarity: float = 1.5,
        exponentiation: float = 0.7, height: float = 135.0, scale: float = 50.0,
    ):
        self.seed = seed
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.exponentiation = exponentiation
        self.height = height
        self.scale = scale


class OpenSimplexCLI:
    cli = f"{BASE_PATH}/noise_cli"

    def __init__(self, config: OpenSimplexConfig, silent: bool = False):
        self.cnf = config
        self.silent = silent
        if config.seed is None:
            self.cnf.seed = randint(0, 100_000_000)

        if not Path(self.cli).is_file():
            raise FileNotFoundError(f"OpenSimplex CLI not found at: {self.cli}")

    def get_2d_array(
            self, size: int, pos_x: float = 0, pos_y: float = 0,
    ) -> tuple[list[float], float]:
        return self._cli(dimensions=2, size=size, pos_x=pos_x, pos_y=pos_y)

    # todo: implement 3Darray
    def get_3d_array(
            self, size: int, pos_x: float = 0, pos_y: float = 0, pos_z: float = 0,
    ) -> tuple[list[float], float]:
        del pos_z
        return self._cli(dimensions=2, size=size, pos_x=pos_x, pos_y=pos_y)

    # todo: implement 4Darray
    def get_4d_array(
            self, size: int, pos_x: float = 0, pos_y: float = 0, pos_z: float = 0, pos_w: float = 0,
    ) -> tuple[list[float], float]:
        del pos_z, pos_w
        return self._cli(dimensions=2, size=size, pos_x=pos_x, pos_y=pos_y)

    @staticmethod
    def _tmp_file() -> str:
        return f'/tmp/map_{int(time())}.json'

    def _cli(self, size: int, pos_x: float = 0, pos_y: float = 0, dimensions: int = 2) -> tuple[list[float], float]:
        t = self._tmp_file()
        c = f"""{self.cli} \
-seed {self.cnf.seed} -dimensions {dimensions} -persistence {self.cnf.persistence} -scale {self.cnf.scale} \
-octaves {self.cnf.octaves} -lacunarity {self.cnf.lacunarity} -exponentiation {self.cnf.exponentiation} \
-height {self.cnf.height} -size {size} -x {pos_x} -y {pos_y} -out {t} \
"""

        if self.silent:
            c += ' -silent'

        shell(c)
        if not Path(t).is_file():
            raise SystemError("OpenSimplex CLI execution failed!")

        with open(t, 'r', encoding='utf-8') as f:
            noise_map = json_loads(f.read())

        remove_file(t)
        return noise_map['data'], noise_map['max']
