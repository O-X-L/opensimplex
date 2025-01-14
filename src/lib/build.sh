#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

go build -buildmode=c-shared -o noise_cgo.so noise_cgo.go
mv noise_cgo.h ../../
mv noise_cgo.so ../../
