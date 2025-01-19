#!/usr/bin/env bash

set -uo pipefail

cd "$(dirname "$0")/../src"
PATH_SRC="$(pwd)"
PATH_BUILD="${PATH_SRC}/../build"
mkdir -p "$PATH_BUILD"
rm -f "${PATH_BUILD}/"*

function compile() {
  os="$1" arch="$2"
  echo "COMPILING BINARIES FOR ${os}-${arch}"

  cd "$PATH_SRC"
  name_out_lib="noise_cgo_${os}_${arch}"
  path_out_lib="${PATH_BUILD}/${name_out_lib}"
  GOOS="$os" GOARCH="$arch" go build -buildmode=c-shared -o "${path_out_lib}.so" "${PATH_SRC}/lib/noise_cgo.go"

  name_out_cli="noise_cli_${os}_${arch}"
  GOOS="$os" GOARCH="$arch" go build -o "${PATH_BUILD}/${name_out_cli}" "${PATH_SRC}/cmd/noise_cli.go"
  GOOS="$os" GOARCH="$arch" CGO_ENABLED=0 go build -o "${PATH_BUILD}/${name_out_cli}-CGO0" "${PATH_SRC}/cmd/noise_cli.go"

  cd "$PATH_BUILD"
  if [[ "$os" == "windows" ]]
  then
      if [ -f "${name_out_lib}.so" ]
      then
        zip "${name_out_lib}.zip" "${name_out_lib}"*
      fi
      zip "${name_out_cli}.zip" "${name_out_cli}"
      zip "${name_out_cli}-CGO0.zip" "${name_out_cli}-CGO0"
  else
      if [ -f "${name_out_lib}.so" ]
      then
        tar -czf "${name_out_lib}.tar.gz" "${name_out_lib}"*
      fi
      tar -czf "${name_out_cli}.tar.gz" "${name_out_cli}"
      tar -czf "${name_out_cli}-CGO0.tar.gz" "${name_out_cli}-CGO0"
  fi
}

compile "linux" "amd64"

# untested:
compile "linux" "386"
compile "linux" "arm"
compile "linux" "arm64"

compile "freebsd" "386"
compile "freebsd" "amd64"
compile "freebsd" "arm"

compile "openbsd" "386"
compile "openbsd" "amd64"
compile "openbsd" "arm"

compile "darwin" "amd64"
compile "darwin" "arm64"

compile "windows" "386"
compile "windows" "amd64"

ls -l "$PATH_BUILD"
