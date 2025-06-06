#!/usr/bin/env bash

config() {
  # set default config
  idle_timeout=300  # Timeout in Seconds
  notify_mod=6  # modulo for notify timeout
  lockscreen=1  # enable lockscreen if 1
  # Load User config
  USER_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config/i3/idle_lockerrc}"
  if [ -e $USER_CONFIG ]; then
    source "$USER_CONFIG"
  fi
  # Set idle_timeout to milliseconds
  idle_timeout=$((idle_timeout * 1000))
}

is_lockscreen_running() {
  # Exit if lockscreen is already displayed
  if [[ $(ps -ao command | grep -E "^i3lock") != "" ]]; then
    exit 0
  fi
}

is_lockscreen_enabled() {
  # Exit if lockscreen is turned off
  if [ $lockscreen -eq 0 ]; then
    exit 0
  fi
}

does_counter_exist() {
  # Make sure notify counter file exist
  if [ ! -e /tmp/idle_locker.counter ]; then
    echo "0" > /tmp/idle_locker.counter
  fi
}

# exit if lockscreen is already running
is_lockscreen_running

# Load Config
config

# Exit if lockscreen is diabled
is_lockscreen_enabled

# Make sure counter file exists
does_counter_exist

# Get Idle time
idle_time=$(xprintidle)

if [ $idle_time -ge $idle_timeout ]; then
  # Check if max idle time is reached
  if [ $(playerctl status) = "Playing" ]; then
    # Stop Audio if lock the screen
    playerctl play-pause
  fi
  betterlockscreen -l dimblur --span --show-layout
elif [ $idle_time -ge $(echo "scale=0;$idle_timeout / 1.1"|bc) ]; then
  notify-send --urgency="critical" "IDLE" \
    "You have been idling for $((idle_time / 1000)) of $((idle_timeout / 1000)) seconds"
elif [ $idle_time -ge $((idle_timeout / 2)) ]; then
  if [ $(( $(cat /tmp/idle_locker.counter) % $notify_mod)) -eq 0 ]; then
    # Send a normal Notify
    notify-send "IDLE" \
      "You have been idling for $((idle_time / 1000)) of $((idle_timeout / 1000)) seconds"
  fi
  echo "$(($(cat /tmp/idle_locker.counter) + 1))" > /tmp/idle_locker.counter
else
  # Reset notify counter
  echo "0" > /tmp/idle_locker.counter
fi
