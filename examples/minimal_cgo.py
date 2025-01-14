from pathlib import Path
from sys import path as sys_path

BASE_PATH = Path(__file__).parent.parent.resolve()
sys_path.append(str(BASE_PATH))

# pylint: disable=C0413
from opensimplex_cgo import OpenSimplex

print('2D Noise Sample:', OpenSimplex().get_2d(20, 40))
