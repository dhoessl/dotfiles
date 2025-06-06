#!/usr/bin/env bash

v4l2-ctl -d /dev/video2 --set-ctrl=brightness=210
v4l2-ctl -d /dev/video2 --set-ctrl=saturation=100
v4l2-ctl -d /dev/video2 --set-ctrl=gamma=53
v4l2-ctl -d /dev/video2 --set-ctrl=zoom_absolute=100

# v4l2-ctl -d /dev/video2 --set-ctrl=brightness=160
v4l2-ctl -d /dev/video2 --set-ctrl=saturation=100
v4l2-ctl -d /dev/video2 --set-ctrl=gamma=60
v4l2-ctl -d /dev/video2 --set-ctrl=zoom_absolute=135

