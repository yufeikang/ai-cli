#!/usr/bin/env bash

set -o errexit
set -o pipefail

if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo 'Usage: ./run_build.sh

Builds this project as a standalone executable.

'
    exit
fi

cd "$(dirname "$0")"

main() {
    if [[ -n "$VIRTUAL_ENV" ]]
	then
		deactivate
	fi
	if [ -d "$(pwd)/.venv" ]
	then
		echo "removing current .venv"
		rm -rf .venv
	fi
	python3 -m venv .venv
	source .venv/bin/activate
	pdm install
    pdm plugin add pdm-packer
    pdm pack --exe
}

main "$@"
