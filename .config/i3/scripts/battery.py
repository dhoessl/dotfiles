#!/usr/bin/env python3

import psutil
from subprocess import run as srun
from time import sleep


class Notifier:
    def __init__(self) -> None:
        self.urgencies = {
            'low': 500,
            'normal': 1000,
            'critical': 5000
        }
        self.level = None
        self.state = None

    def notify(self, urgency) -> None:
        srun([
            'notify-send',
            '-u', self.urgency,
            '-t', self.urgencies[urgency],
            'BATTERY INFORMATION',
            'Battery is at level {}'.format(int(self.level))
        ])

    def change_level(self, level) -> None:
        self.level = level

    def change_state(self, state) -> None:
        if self.state != state:
            self.state = state


def run() -> None:
    notifier = Notifier()
    while True:
        notifier.change_level(psutil.sensors_battery().percent)
        notifier.change_state(psutil.sensors_battery().power_plugged)
        if notifier.level < 15 and not notifier.state:
            notifier.notify('critical')
        elif notifier.level < 30 and not notifier.state:
            notifier.notify('normal')
        elif notifier.level < 50 and not notifier.state:
            notifier.notify('low')
        sleep(300)


if __name__ == '__main__':
    run()
