#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
PY="$VENV_DIR/bin/python"

if [[ ! -x "$PY" ]]; then
	echo "Python venv not found at $PY" >&2
	exit 1
fi

TOPIC=${TOPIC:-"Actu du jour"}
SLIDES=${SLIDES:-5}
OUT_DIR=${OUT_DIR:-"$SCRIPT_DIR/output"}
BASENAME=${BASENAME:-"daily_video"}

cd "$SCRIPT_DIR"
"$PY" "$SCRIPT_DIR/main.py" --topic "$TOPIC" --slides "$SLIDES" --out "$OUT_DIR" --basename "$BASENAME"