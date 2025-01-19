#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
PATH_SRC="$(pwd)"
PATH_BUILD="${PATH_SRC}/../build"
mkdir -p "$PATH_BUILD"
rm -f "${PATH_BUILD}/"*

echo "### BUILDING CGO LIB ###"
NAME_OUT_LIB="noise_cgo_debian_amd64"
PATH_OUT_LIB="${PATH_BUILD}/${NAME_OUT_LIB}"
go build -buildmode=c-shared -o "${PATH_OUT_LIB}.so" "${PATH_SRC}/lib/noise_cgo.go"


echo "### BUILDING CLI ###"
NAME_OUT_CLI="noise_cli_linux_amd64"
go build -o "${PATH_BUILD}/${NAME_OUT_CLI}" "${PATH_SRC}/cmd/noise_cli.go"

echo "### CREATING ARCHIVES ###"
cd "$PATH_BUILD"
zip "${NAME_OUT_LIB}.zip" "$NAME_OUT_LIB"*
zip "${NAME_OUT_CLI}.zip" "$NAME_OUT_CLI"

ls -l "$PATH_BUILD"
