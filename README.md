# OpenSimplex Noise

This repository contains a simple Python3-wrapper around the [opensimplex-go](https://github.com/ojrac/opensimplex-go) module.

It is faster than the full [Python3 opensimplex](https://pypi.org/project/opensimplex/) package as the actual noise calculations are offloaded to C.

## Usage

You first need to install Go to compile the C-library: [Golang download/install](https://go.dev/doc/install)

Compile: `go build -buildmode=c-shared -o noise.so noise.go`

Test it: `python3 example.py`


## Credits

Thanks to [@ojrac for the golang module](https://github.com/ojrac/opensimplex-go) and of course to [@KdotJPG for the original OpenSimplex](https://github.com/KdotJPG).

## License

MIT
