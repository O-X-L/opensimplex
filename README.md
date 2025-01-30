# OpenSimplex Noise

[![Lint](https://github.com/O-X-L/opensimplex/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/opensimplex/actions/workflows/lint.yml)
[![Test](https://github.com/O-X-L/opensimplex/actions/workflows/test.yml/badge.svg)](https://github.com/O-X-L/opensimplex/actions/workflows/test.yml)

This repository contains a simple Python3-wrapper around the [opensimplex-go](https://github.com/ojrac/opensimplex-go) module.

It should be an alternative to the full [Python3-implementation of opensimplex](https://pypi.org/project/opensimplex/).

----

## Benchmarks

### 50 x 50

|Implementation|Time|
|---|---|
|[opensimplex-go CLI](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cli.py)|0.047|
|[opensimplex python](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_compare.py)|0.673|
|[opensimplex-go CGO](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cgo.py)|8.371|

### 200 x 200

|Implementation|Time|
|---|---|
|[opensimplex-go CLI](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cli.py)|0.209|
|[opensimplex python](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_compare.py)|10.808|
|[opensimplex-go CGO](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cgo.py)|139.539|

### 1000 x 1000

|Implementation|Time|
|---|---|
|[opensimplex-go CLI](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cli.py)|3.535|
|[opensimplex python](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_compare.py)|248.498|
|[opensimplex-go CGO](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cgo.py)|LOOONG...|

![Example Map](https://raw.githubusercontent.com/O-X-L/opensimplex/refs/heads/latest/examples/map_1000x1000.webp)

----

## Usage

You first need to either [download](https://github.com/O-X-L/opensimplex/releases) or build the golang binaries.

### Build

1.  [Golang download/install](https://go.dev/doc/install)

2. Build them: `bash scripts/build_cli.sh` and/or `bash scripts/build_cgo.sh`

----

### CLI Implementation

1. Install example requirements: `pip install -r examples/requirements.txt`

2. Test it: `python3 examples/generate_map_cli.py`

3. How to use it: [Example](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cli.py) | [Practical Example of Terrain-Generation](https://github.com/superstes/strategy-browser-game/tree/main/src/backend/map_generator)

This way it basically calls the standalone golang binary in a subprocess and loads the resulting data from a temporary file.

It currently only supports generating whole **2D** noise-maps.

#### Raw CLI Usage

Export data example:

```json
{
  "data": [0, 0, 43.49935, 0, 1, 39.84343],  // x, y, height
  "max": 43.49935,
  "min": 39.84343
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
        Seed
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
  -no-coords
        If enabled the coords will be omitted from the data-export
  -sink
        If the whole noise-map should be sunk-down so the lowest point is 0
  -lower float
        Lower each height by this value - negatives are clamped to 0
  -mirror string
        To mirror the values set this to one of: 'x', 'y', 'xy', 'reverse'
  -rotate string
        To rotate the values set this to one of: '90cw', '90ccw', '180'
```

----

### CGO Implementation

1. Install example requirements: `pip install -r examples/requirements.txt`

2. Test it: `python3 examples/minimal_cgo.py` or `python3 examples/generate_map_cgo.py`

3. How to use it: [Example](https://github.com/O-X-L/opensimplex/blob/latest/examples/generate_map_cgo.py)

The CGO implementation is very slow. Not yet sure why that is..

----

## Credits

Thanks to [@ojrac for the golang module](https://github.com/ojrac/opensimplex-go), to [@KdotJPG for the original OpenSimplex](https://github.com/KdotJPG) and to [@simondevyoutube for the implementation-example](https://github.com/simondevyoutube/ProceduralTerrain_Part10).

## License

MIT
