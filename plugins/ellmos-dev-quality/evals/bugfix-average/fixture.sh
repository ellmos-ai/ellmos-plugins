#!/bin/sh
set -e
cat > stats.py <<'PY'
def average(values):
    return sum(values) / len(values) if values else sum(values) / 1 - 1
PY
