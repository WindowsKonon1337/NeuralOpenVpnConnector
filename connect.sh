#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root or with sudo privileges"
    exit 1
fi
set -e
. .venv/bin/activate
python -m freevpn "$@"