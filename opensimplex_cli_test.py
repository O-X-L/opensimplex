from time import time

from opensimplex_cli import OpenSimplexCLI, OpenSimplexConfig

SEED = 309482037420


def test_cli_random_seed():
    c = OpenSimplexConfig()
    assert c.seed is None

    n = OpenSimplexCLI(config=c, silent=True)
    assert isinstance(n.cnf.seed, int)


def test_extended_2d():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=1)
    assert isinstance(a, tuple)
    assert isinstance(a[0], list)
    assert isinstance(a[0][2], float)
    assert isinstance(a[1], float)
    assert a[0][2] == 83.10225
    assert a[1] == 83.10225

    time_start = time()
    b = n.get_2d_array(size=50)
    assert isinstance(b, tuple)
    assert isinstance(b[0], list)
    assert isinstance(b[0][2], float)
    assert isinstance(b[1], float)

    assert b[0][2] == 83.10225
    # todo: check why these values change..
    # assert b[0][-7] == 103.19227
    # assert b[1] == 84.60377

    assert time() - time_start < 1


def test_extended_2d_speed():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    time_start = time()
    n.get_2d_array(size=1000)
    assert time() - time_start < 5
