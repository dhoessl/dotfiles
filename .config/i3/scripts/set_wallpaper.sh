#!/usr/bin/env bash

WALLPAPER_PATH="/home/dhoessl/wallpaper/3840x2160"
WALLPAPER_NAME=$(ls $WALLPAPER_PATH | sort -R | head -n1)

feh --no-fehbg --bg-fill $WALLPAPER_PATH/$WALLPAPER_NAME
