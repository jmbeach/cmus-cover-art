#!/bin/sh

CURRENT_DIR="$HOME/.config/cmus/cmus-cover-art"
COVERS_DIR="$CURRENT_DIR/.cover"

PREVIOUS=""
CURRENT=""

IMAGE_VIEWER="$HOME/.local/bin/kitty +kitten icat"

clear
while (true)
do
  if test -f "$COVERS_DIR/current.txt"; then
    CURRENT=`cat $COVERS_DIR/current.txt`
    if [ "$CURRENT" != "$PREVIOUS" ]
    then 
      pkill -TERM -P $$
      clear
      if [ "$CURRENT" != "" ]
      then
        PREVIOUS=$CURRENT
        $IMAGE_VIEWER "$CURRENT" &
      else
        echo "::: NO COVER ART :::" 
        PREVIOUS=""
      fi
    fi
  fi

  sleep 1
done

