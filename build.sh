#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

go build -buildmode=c-shared -o noise.so noise.go
