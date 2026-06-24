#!/usr/bin/env bash
# Install/manage hermes-plugin-dremio
set -euo pipefail
~/.hermes/hermes-agent/venv/bin/python3 "$(dirname "$0")/setup.py" "$@"
