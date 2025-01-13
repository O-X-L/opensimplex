# OpenSimplex Noise

[![Lint](https://github.com/O-X-L/python-opensimplex/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/python-opensimplex/actions/workflows/lint.yml)
[![Test](https://github.com/O-X-L/python-opensimplex/actions/workflows/test.yml/badge.svg)](https://github.com/O-X-L/python-opensimplex/actions/workflows/test.yml)

This repository contains a simple Python3-wrapper around the [opensimplex-go](https://github.com/ojrac/opensimplex-go) module.

It should be an alternative to the full [Python3-implementation of opensimplex](https://pypi.org/project/opensimplex/).

----

## Usage

You first need to install Go to compile the C-library: [Golang download/install](https://go.dev/doc/install)

Compile: `go build -buildmode=c-shared -o noise.so noise.go`

Test it: `python3 examples/minimal.py`

For more information see: [Examples](https://github.com/O-X-L/python-opensimplex/blob/latest/examples)

----

## Performance

It is still pretty slow for now..

> tbc


----

## Credits

Thanks to [@ojrac for the golang module](https://github.com/ojrac/opensimplex-go) and of course to [@KdotJPG for the original OpenSimplex](https://github.com/KdotJPG).

## License

MIT
