# OpenSimplex Noise

[![Lint](https://github.com/O-X-L/python-opensimplex/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/python-opensimplex/actions/workflows/lint.yml)
[![Test](https://github.com/O-X-L/python-opensimplex/actions/workflows/test.yml/badge.svg)](https://github.com/O-X-L/python-opensimplex/actions/workflows/test.yml)

This repository contains a simple Python3-wrapper around the [opensimplex-go](https://github.com/ojrac/opensimplex-go) module.

It should be an alternative to the full [Python3-implementation of opensimplex](https://pypi.org/project/opensimplex/).

## Usage

You first need to install Go to compile the C-library: [Golang download/install](https://go.dev/doc/install)

### CLI Implementation

1. Compile: `bash src/cmd/build.sh`

2. Install example requirements: `pip install -r examples/requirements.txt`

3. Test it: `python3 examples/generate_map_cli.py`

4. How to use it: [Example](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cli.py)

This way it basically calls the standalone golang binary in a subprocess and loads the resulting data from a temporary file.

It currently only supports generating whole 2D noise-maps.

Data example:

```json
{
  "data": [0, 0, 0.43935, 0, 1, 0.3984343],  // x, y, height
  "max": 0.43935,
  "min": 0.3984343
}
```

Usage:

```bash
Usage of noise_cli:
  -size int
        Map size (default 1000)
  -x float
        Map offset dimension-X
  -y float
        Map offset dimension-Y
  -out string
        Map output file (default "/tmp/map.json")
  -dimensions int
        Dimensions (default 2)
  -seed int
        Seed (default -1)
  -exponentiation float
        Exponentiation (default 5)
  -height float
        Height (default 135)
  -lacunarity float
        Lacunarity (default 1.5)
  -octaves int
        Octaves (default 10)
  -persistence float
        Persistence (default 0.7)
  -scale float
        Scale (default 50)
  -silent
        Do not show output
  -sink
        If the whole noise-map should be sunk-down so the lowest point is 0
```

----

### CGO Implementation

1. Compile: `bash src/lib/build.sh`

2. Install example requirements: `pip install -r examples/requirements.txt`

3. Test it: `python3 examples/minimal_cgo.py` or `python3 examples/generate_map_cgo.py`

4. How to use it: [Example](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cgo.py)

The CGO implementation is very slow. Not yet sure why that is..

----

## Credits

Thanks to [@ojrac for the golang module](https://github.com/ojrac/opensimplex-go) and of course to [@KdotJPG for the original OpenSimplex](https://github.com/KdotJPG).

## License

MIT
