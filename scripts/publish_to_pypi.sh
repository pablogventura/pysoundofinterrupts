#!/usr/bin/env bash
# Publish the package to PyPI.
# Requires: pip install build twine
# Config: ~/.pypirc or TWINE_USERNAME / TWINE_PASSWORD (PyPI token)

set -e
cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "Project directory: $ROOT"
echo "Version in pyproject.toml: $(grep '^version' pyproject.toml | cut -d'"' -f2)"
echo ""

if ! python3 -c "import build" 2>/dev/null; then
    echo "Install build: pip install build"
    exit 1
fi
if ! python3 -c "import twine" 2>/dev/null; then
    echo "Install twine: pip install twine"
    exit 1
fi

rm -rf "${ROOT}/dist"
python3 -m build
twine upload dist/*

echo ""
echo "Published. Check: https://pypi.org/project/pysoundofinterrupts/"
