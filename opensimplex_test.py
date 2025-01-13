from opensimplex import OpenSimplex, OpenSimplexExtended, OpenSimplexConfig

SEED = 309482037420


def test_random_seed():
    assert isinstance(OpenSimplex().seed, int)


def test_simple_2d():
    n = OpenSimplex(SEED)
    assert isinstance(n.get_2d(1, 2), float)
    assert n.get_2d(1, 2) != 0.0
    assert n.get_2d(20, 40) == -0.32619595527648926


def test_simple_3d():
    n = OpenSimplex(SEED)
    assert isinstance(n.get_3d(1, 2, 3), float)
    assert n.get_3d(20, 30, 60) == -0.1572575867176056


def test_simple_4d():
    n = OpenSimplex(SEED)
    assert isinstance(n.get_4d(1, 2, 3, 4), float)
    assert n.get_4d(20, 40, 60, 80) == 0.03823479264974594


def test_extended_random_seed():
    c = OpenSimplexConfig()
    assert c.seed is None

    n = OpenSimplexExtended(c)
    assert n.cnf.seed is None
    assert isinstance(n._noise.seed, int)


def test_extended_2d():
    n = OpenSimplexExtended(OpenSimplexConfig(seed=SEED))
    assert isinstance(n.get_2d(1, 2), float)
    assert n._noise.get_2d(20, 40) == -0.32619595527648926
    assert n.get_2d(20, 40) == 0.4673804044723511


def test_extended_3d():
    n = OpenSimplexExtended(OpenSimplexConfig(seed=SEED))
    assert isinstance(n.get_3d(1, 2, 3), float)
    assert n._noise.get_3d(20, 30, 60) == -0.1572575867176056
    assert n.get_3d(20, 30, 60) == 0.48427424132823943


def test_extended_4d():
    n = OpenSimplexExtended(OpenSimplexConfig(seed=SEED))
    assert isinstance(n.get_4d(1, 2, 3, 4), float)
    assert n._noise.get_4d(20, 40, 60, 80) == 0.03823479264974594
    assert n.get_4d(20, 40, 60, 80) == 0.5038234792649746
