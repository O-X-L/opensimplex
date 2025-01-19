#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")../src/cmd"

PATH_OUT="$(pwd)/../.."

go build -o "${PATH_OUT}/noise_cli" noise_cli.go
