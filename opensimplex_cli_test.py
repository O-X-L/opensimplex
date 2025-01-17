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
    assert isinstance(a[2], float)
    assert a[1] == 83.10225 == a[2] == a[0][2]

    time_start = time()
    b = n.get_2d_array(size=50)
    assert isinstance(b, tuple)
    assert isinstance(b[0], list)
    assert isinstance(b[0][2], float)
    assert isinstance(b[1], float)
    assert isinstance(b[2], float)

    assert b[0][2] == 83.10225
    assert b[0][-7] == 80.59629
    assert b[1] == 84.60377
    assert b[2] == 46.347794

    assert time() - time_start < 1


def test_extended_2d_speed():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    time_start = time()
    n.get_2d_array(size=1000)
    assert time() - time_start < 5


def test_cli_seed():
    n =  OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=20)
    b = n.get_2d_array(size=20)
    assert a[0][2] == b[0][2]
    assert a[0][-7] == b[0][-7]


def test_extended_2d_sink():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=100)
    assert a[0][2] == 83.10225
    assert a[0][-7] == 80.478264
    assert a[1] == 101.29977
    assert a[2] == 46.347794

    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True, sink_down=True)
    b = n.get_2d_array(size=100)
    assert b[0][2] == 36.754456
    assert b[0][-7] == 34.13047
    assert b[1] == 54.951973
    assert b[2] == 0
