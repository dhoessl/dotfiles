#!/usr/bin/env python3

from subprocess import Popen

LOCKSCREEN_LOCATION = "/tmp/lockscreen.png"

if __name__ == "__main__":
    scrot = Popen(["scrot", LOCKSCREEN_LOCATION])
    scrot.wait()
    update_cache = Popen([
        "betterlockscreen",
        "-u", LOCKSCREEN_LOCATION,
        "--fx", "dimblur"
    ])
    update_cache.wait()
