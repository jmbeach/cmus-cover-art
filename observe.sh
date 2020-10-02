#!/bin/sh

CURRENT_DIR="$HOME/.config/cmus/cmus-cover-art"
COVERS_DIR="$CURRENT_DIR/.cover"

status=$2
file_path=$(echo "$@" | grep -o  "file .*\...." | sed s/file\ //)
timestamp=`date +%s`
python3 "$CURRENT_DIR/observe.py" "$COVERS_DIR" "$1" "$2" "$@"