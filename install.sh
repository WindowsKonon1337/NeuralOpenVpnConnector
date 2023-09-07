#!/bin/bash

set -e
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt