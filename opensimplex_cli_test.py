from time import time

from opensimplex_cli import OpenSimplexCLI, OpenSimplexConfig

SEED = 309482037420


def test_cli_random_seed():
    c = OpenSimplexConfig()
    assert c.seed is None

    n = OpenSimplexCLI(config=c, silent=True)
    assert isinstance(n.cnf.seed, int)


def test_2d():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=1)
    assert isinstance(a, dict)
    assert isinstance(a['data'], list)
    assert isinstance(a['data'][2], float)
    assert isinstance(a['max'], float)
    assert isinstance(a['min'], float)
    assert a['max'] == 83.10225 == a['min'] == a['data'][2]

    time_start = time()
    b = n.get_2d_array(size=50)
    assert isinstance(b, dict)
    assert isinstance(b['data'], list)
    assert isinstance(b['data'][2], float)
    assert isinstance(b['max'], float)
    assert isinstance(b['min'], float)

    assert b['data'][2] == 83.10225
    assert b['data'][-7] == 80.59629
    assert b['max'] == 84.60377
    assert b['min'] == 46.347794

    assert time() - time_start < 1


def test_2d_speed():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    time_start = time()
    n.get_2d_array(size=1000)
    assert time() - time_start < 5


def test_2d_no_coords():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=10)
    b = n.get_2d_array(size=10, no_coords=True)
    assert a['data'][2] == b['data'][0]
    assert len(a['data']) == 10 * 10 * 3
    assert len(b['data']) == 10 * 10


def test_seed():
    n =  OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=20, no_coords=True)
    b = n.get_2d_array(size=20, no_coords=True)
    assert a['data'][0] == b['data'][0]
    assert a['data'][-2] == b['data'][-2]


def test_2d_sink():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=100, no_coords=True)
    assert a['data'][0] == 83.10225
    assert a['data'][-3] == 80.478264
    assert a['max'] == 101.29977
    assert a['min'] == 46.347794

    b = n.get_2d_array(size=100, sink_down=True, no_coords=True)
    assert b['data'][0] == 36.754456
    assert b['data'][-3] == 34.13047
    assert b['max'] == 54.951973
    assert b['min'] == 0


def test_2d_lower():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=100, no_coords=True)
    assert a['data'][0] == 83.10225
    assert a['data'][-3] == 80.478264
    assert a['max'] == 101.29977
    assert a['min'] == 46.347794

    lower_by = 40
    rel = 0.001  # floating-points..
    b = n.get_2d_array(size=100, lower_by=lower_by, no_coords=True)
    assert -rel < b['data'][0] - (a['data'][0] - lower_by) < rel
    assert -rel < b['data'][-3] - (a['data'][-3] - lower_by) < rel
    assert -rel < b['max'] - (a['max'] - lower_by) < rel
    assert -rel < b['min'] - (a['min'] - lower_by) < rel


def test_2d_mirror_x():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=3, no_coords=True)
    b = n.get_2d_array(size=3, mirror='x', no_coords=True)
    assert a['data'][3 * 2 + 1] == b['data'][1]
    assert a['data'][1] == b['data'][3 * 2 + 1]


def test_2d_mirror_y():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=3, no_coords=True)
    b = n.get_2d_array(size=3, mirror='y', no_coords=True)
    assert a['data'][0] == b['data'][2]
    assert a['data'][6] == b['data'][-1]


def test_2d_mirror_reverse():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=3, no_coords=True)
    b = n.get_2d_array(size=3, no_coords=True, mirror='reverse')
    assert a['data'][0] == b['data'][-1]
    assert a['data'][4] == b['data'][4]


def test_2d_rotate_90cw():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=3, no_coords=True)
    b = n.get_2d_array(size=3, rotate='90cw', no_coords=True)
    assert a['data'][0] == b['data'][2]
    assert a['data'][-3] == b['data'][0]
    assert a['data'][-1] == b['data'][-3]


def test_2d_rotate_90ccw():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=3, no_coords=True)
    b = n.get_2d_array(size=3, rotate='90ccw', no_coords=True)
    assert a['data'][0] == b['data'][-3]
    assert a['data'][2] == b['data'][0]


def test_2d_rotate_180():
    n = OpenSimplexCLI(config=OpenSimplexConfig(seed=SEED), silent=True)
    a = n.get_2d_array(size=3, no_coords=True)
    b = n.get_2d_array(size=3, rotate='180', no_coords=True)
    assert a['data'][0] == b['data'][-1]
    assert a['data'][2] == b['data'][-3]
