#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/../src/lib"

PATH_OUT="$(pwd)/../.."

go build -buildmode=c-shared -o "${PATH_OUT}/noise_cgo.so" noise_cgo.go
