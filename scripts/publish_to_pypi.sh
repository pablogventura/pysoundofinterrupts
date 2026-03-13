#!/usr/bin/env bash
# Publica el paquete en PyPI.
# Requiere: pip install build twine
# Configuración: ~/.pypirc o TWINE_USERNAME / TWINE_PASSWORD (token PyPI)

set -e
cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "Directorio del proyecto: $ROOT"
echo "Versión en pyproject.toml: $(grep '^version' pyproject.toml | cut -d'"' -f2)"
echo ""

if ! python3 -c "import build" 2>/dev/null; then
    echo "Instala build: pip install build"
    exit 1
fi
if ! python3 -c "import twine" 2>/dev/null; then
    echo "Instala twine: pip install twine"
    exit 1
fi

rm -rf "${ROOT}/dist"
python3 -m build
twine upload dist/*

echo ""
echo "Publicado. Comprueba: https://pypi.org/project/pysoundofinterrupts/"
